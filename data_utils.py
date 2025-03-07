import psycopg2
import numpy as np
import json
from dotenv import load_dotenv
import os
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

driver = os.getenv("DRIVER")
host = os.getenv("HOST")
port = os.getenv("PORT")
database = os.getenv("DATABASE")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

connection_params = {
    'dbname': database,
    'user': username,
    'password': password,
    'host': host,
    'port': port,
}


def execute_query(query, single_item = False):
    response = None
    try:
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()
        cursor.execute(query)
    
        if single_item:
            response = cursor.fetchone()
        else:
            response = cursor.fetchall()
    
    except Exception as e:
        print(f"Error connecting to the PostgreSQL database: {e}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return response
    

def rank_embeddings_by_cosine_with_texts(embedding_in_json_string, data):
    distances = []
    input_embedding = np.array(json.loads(embedding_in_json_string), dtype=np.float64).reshape(1, -1)
    
    for row in data:
        current_embedding = np.array(json.loads(row[0]), dtype=np.float64).reshape(1, -1)
        
        # Calculate the cosine similarity between the input embedding and the current embedding
        similarity = cosine_similarity(input_embedding, current_embedding)[0][0]
        
        # Convert similarity to distance (1 - similarity)
        distance = 1 - similarity

        distances.append((row[0],row[1],row[2],distance))

    distances.sort(key=lambda x: x[3])
        
    return distances


def get_clean_data(query_all_data, query_one_garbagy, garbage_n):
    data = execute_query(query_all_data)

    embedding_in_json_string = execute_query(query_one_garbagy, single_item=True)[0]

    ranked_data = rank_embeddings_by_cosine_with_texts(embedding_in_json_string, data)

    clean_data = ranked_data[garbage_n:]

    return clean_data





