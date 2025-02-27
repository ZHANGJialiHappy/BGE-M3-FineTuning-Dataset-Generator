from typing import Dict
import re
import psycopg2
import numpy as np
import json
import random
from dotenv import load_dotenv
import os
from sklearn.metrics.pairwise import cosine_similarity
from queries import query_all_data, query_one_gabagy_by_embedding
# from invoke_claude import filter_data


# Load environment variables from .env file
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

def fetch_random_data(query, random_n):
    data = execute_query(query)
    
    if not data:
        return None

    return random.sample(data, random_n)
    

def rank_embeddings_by_cosine_with_texts(embedding_in_json_string, data):
    distances = []
    input_embedding = np.array(json.loads(embedding_in_json_string), dtype=np.float64).reshape(1, -1)
    
    for row in data:
        current_embedding = np.array(json.loads(row[0]), dtype=np.float64).reshape(1, -1)
        
        # Calculate the cosine similarity between the input embedding and the current embedding
        similarity = cosine_similarity(input_embedding, current_embedding)[0][0]
        
        # Convert similarity to distance (1 - similarity)
        distance = 1 - similarity
        
        distances.append((distance, row))
    
    distances.sort(key=lambda x: x[0])
    for d, _ in distances[:5]:
        print(d)
    ranked_data = [row for _, row in distances]
    return ranked_data

def rank_embeddings_by_dot_product_with_texts(embedding_sparse, data):
    distances = []

    input_embedding_sparse = re.sub(r'/\d+$', '', embedding_sparse)
    input_embedding_sparse_in_json_string = re.sub(r'(\d+):', r'"\1":', input_embedding_sparse)
    input_embedding_sparse__json = json.loads(input_embedding_sparse_in_json_string)
    
    for row in data:
        current_embedding_sparse = re.sub(r'/\d+$', '', row[1])
        current_embedding_sparse_json_string = re.sub(r'(\d+):', r'"\1":', current_embedding_sparse)
        current_embedding_json = json.loads(current_embedding_sparse_json_string)

        distance = np.sqrt(_compute_single_lexical_matching_score(input_embedding_sparse__json, current_embedding_json))
        
        distances.append((distance, row))
    
    distances.sort(reverse=True, key=lambda x: x[0])
    for d, _ in distances[:5]:
        print(d)
        print('*********************')
    ranked_data = [row for _, row in distances]
    return ranked_data

def _compute_single_lexical_matching_score(lw1: Dict[str, float], lw2: Dict[str, float]):
    scores = 0
    for token, weight in lw1.items():
        if token in lw2:
            scores += weight * lw2[token]
    return scores

def get_clean_data():
    data = execute_query(query_all_data)

    embedding_in_json_string = execute_query(query_one_gabagy_by_embedding, single_item=True)[0]

    return rank_embeddings_by_cosine_with_texts(embedding_in_json_string, data)[139:]