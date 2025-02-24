from typing import Dict
import psycopg2
import numpy as np
import json
import random
# import jsonlines
# from psycopg2 import sql
from dotenv import load_dotenv
import os
import re
from typing import List
from sklearn.metrics.pairwise import cosine_similarity
import invoke_claude as ic

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

query_pos_embedding = """
SELECT embedding
FROM v9__chatbot_documents
WHERE source_uri like '%58548175-ccef-4d6a-987c-f597b7d4d225%'
LIMIT 1
"""

query_pos_embedding_sparse = """
SELECT embedding_sparse
FROM v9__chatbot_documents
WHERE source_uri like '%58548175-ccef-4d6a-987c-f597b7d4d225%'
LIMIT 1
"""

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

def get_furthest_embeddings_cosine(embedding_string: str, embedding_field: str = 'embedding', furthest_n: int = 5) -> List[str]:
    query = f"""
    SELECT {embedding_field}, embedding_text
    FROM v9__chatbot_documents
    WHERE source_uri like '%58548175-ccef-4d6a-987c-f597b7d4d225%'
    LIMIT 5
    """
    # data=execute_query(query)
    data = ic.filter_data(execute_query(query))
    
    if not data:
        return None
    
    distances = []
    
    # Convert the input embedding to a numpy array
    input_embedding = np.array(json.loads(embedding_string), dtype=np.float64).reshape(1, -1)
    
    for row in data:
        current_embedding = np.array(json.loads(row[0]), dtype=np.float64).reshape(1, -1)
        current_embedding_text = row[1]
        
        # Calculate the cosine similarity between the input embedding and the current embedding
        similarity = cosine_similarity(input_embedding, current_embedding)[0][0]
        
        # Convert similarity to distance (1 - similarity)
        distance = 1 - similarity
        
        distances.append((distance, current_embedding_text))
    
    # Sort the distances in descending order and get the top N
    distances.sort(reverse=True, key=lambda x: x[0])

    furthest_embeddings_texts = [text for _, text in distances[:furthest_n]]
    furthest_embeddings_distance = [distance for distance, _ in distances[:furthest_n]]
    print(furthest_embeddings_distance)
    
    return furthest_embeddings_texts

def get_furthest_embeddings_uclidean(embedding_string, embedding_field='embedding', furthest_n=5):
    query = f"""
    SELECT {embedding_field}, embedding_text
    FROM v9__chatbot_documents
    WHERE source_uri like '%58548175-ccef-4d6a-987c-f597b7d4d225%'
    """
    
    data = execute_query(query)
    
    if not data:
        return None
    
    distances = []
    
    # Convert the input embedding to a numpy array
    input_embedding = np.array(json.loads(embedding_string), dtype=np.float64)
    
    for row in data:
        current_embedding = np.array(json.loads(row[0]), dtype=np.float64)
        current_embedding_text = row[1]
        
        # Calculate the Euclidean distance between the input embedding and the current embedding
        distance = np.linalg.norm(input_embedding - current_embedding)
        
        distances.append((distance, current_embedding_text))
    
    # Sort the distances in descending order and get the top N
    distances.sort(reverse=True, key=lambda x: x[0])
    furthest_embeddings_texts = [text for _, text in distances[:furthest_n]]
    furthest_embeddings_distance = [distance for distance, _ in distances[:furthest_n]]
    print(furthest_embeddings_distance)
    return furthest_embeddings_texts

def get_furthest_embeddings_sparse(embedding_sparse_string, embedding_field='embedding_sparse', furthest_n=5):
    query = f"""
    SELECT {embedding_field}, embedding_text
    FROM v9__chatbot_documents
    WHERE source_uri like '%58548175-ccef-4d6a-987c-f597b7d4d225%'
    LIMIT 50
    """
    
    data = execute_query(query)
    
    if not data:
        return None
    
    distances = []

    embedding_sparse = re.sub(r'/\d+$', '', embedding_sparse_string)
    embedding_sparse_json_string = re.sub(r'(\d+):', r'"\1":', embedding_sparse)
    input_embedding_json = json.loads(embedding_sparse_json_string)
    
    for row in data:
        current_embedding_sparse = re.sub(r'/\d+$', '', row[0])
        current_embedding_sparse_json_string = re.sub(r'(\d+):', r'"\1":', current_embedding_sparse)
        current_embedding_json = json.loads(current_embedding_sparse_json_string)
        current_embedding_text = row[1]
        
        # Calculate the Euclidean distance between the input sparse embedding and the current sparse embedding
        distance = np.sqrt(_compute_single_lexical_matching_score(input_embedding_json, current_embedding_json))
        
        distances.append((distance, current_embedding_text))
    
    # Sort the distances in descending order and get the top N
    distances.sort(reverse=True, key=lambda x: x[0])
    furthest_embeddings_texts = [text for _, text in distances[:furthest_n]]
    
    return furthest_embeddings_texts

def _compute_single_lexical_matching_score(lw1: Dict[str, float], lw2: Dict[str, float]):
    scores = 0
    for token, weight in lw1.items():
        if token in lw2:
            scores += weight * lw2[token]
    return scores

def get_random_embeddings(embedding_string, random_n=5):
    # Query to get all embeddings and their corresponding embedding_text
    query = """
    SELECT embedding, embedding_text
    FROM v9__chatbot_documents
    WHERE source_uri like '%58548175-ccef-4d6a-987c-f597b7d4d225%'
    LIMIT 50
    """
    
    data = execute_query(query)
    
    if not data:
        return None
    
    input_embedding = np.array(json.loads(embedding_string), dtype=np.float64)
    
    # Filter out the input embedding from the data
    filtered_data = [row for row in data if not np.array_equal(np.array(json.loads(row[0]), dtype=np.float64), input_embedding)]
    
    # Get 5 random embeddings and their corresponding embedding_text
    random_samples = random.sample(filtered_data, random_n)
    random_text_samples = [row[1] for row in random_samples]
    
    return random_text_samples

# def save_to_jsonl(data, file_path):
#     with jsonlines.open(file_path, mode='w') as writer:
#         for row in data:
#             writer.write({
#                 "embedding": row[0],
#                 "embedding_sparse": row[1],
#                 "document_contents": row[2]
#             })

if __name__ == "__main__":
    result = execute_query(query_pos_embedding, single_item=True)
    if result:
        embedding_string = result[0]
        print(get_furthest_embeddings_cosine(embedding_string, embedding_field='embedding', furthest_n=1))
    else:
        print("No data found")

    # print(execute_query(query_pos_embedding, single_item=True))

    # embedding_sparse=re.sub(r'/\d+$', '', result[0])
    # embedding_sparse = re.sub(r'(\d+):', r'"\1":', embedding_sparse)
    # print(json.loads(embedding_sparse))
    # print(json.loads(re.sub(r'/\d+$', '', result[0])))
    
    # embedding_string = execute_query(query_pos_embedding, single_item=True)[0]
    # print(f"Type of embedding_string: {type(embedding_string)}")
    
        
    # if isinstance(embedding_string, str) and embedding_string.strip():
    #     try:
    #         # Decode the string using 'utf-8-sig' to handle the BOM
    #         embedding_string = embedding_string.encode('utf-8').decode('utf-8-sig')

    #         # Convert the string to a JSON object, then to a NumPy array
    #         embedding_array = np.array(json.loads(embedding_string), dtype=np.float64)
    #         print("Successfully converted embedding_string to numpy array.")
    #     except json.JSONDecodeError as e:
    #         print(f"Error decoding JSON: {e}")
    #     except ValueError as e:
    #         print(f"Error converting to numpy array: {e}")
    # else:
    #     print("embedding_string is not a valid JSON string or is empty.")

    # print(type(execute_query(query, single_item=True)[0]))

    # data = execute_query(query, single_item=True)
    # save_to_jsonl(data, 'output.jsonl')
    # print("Data has been saved to output.jsonl")