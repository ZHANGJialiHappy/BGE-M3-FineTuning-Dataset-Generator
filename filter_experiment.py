from typing import Dict
import numpy as np
import json
import random
import re
from typing import List
from sklearn.metrics.pairwise import cosine_similarity
from queries import get_query_pos_embedding_nth, get_query_pos_embedding_sparse_nth, query_one_uuid1_garbagy_by_embedding,query_uuid1_data_by_embedding,query_uuid1_data_by_embedding_sparse, query_one_uuid1_garbagy_by_embedding_sparse
from generate_negs import execute_query
from invoke_claude import generate_query, filter_data


def print_closest_and_furthest_embeddings_cosine(embedding_string: str,  closest_n:int, furthest_n: int) -> List[str]:
    data = execute_query(query_uuid1_data_by_embedding)
    
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

    # Sort the distances in ascending order and get the top N closest
    distances.sort(key=lambda x: x[0])
    print("Closest texts:")
    for d, text in distances[:closest_n]:
        print(d)
        print(text)
        print('*********************')

    print('******************************************************')

    # distances.sort(reverse=True, key=lambda x: x[0])    
    # print("Furthest texts:")
    # for d, text in distances[:furthest_n]:
    #     print(d)
    #     print(text)
    #     print('*********************')

def print_closest_embeddings_sparse(embedding_sparse_string, closest_n):
    data = execute_query(query_uuid1_data_by_embedding_sparse)
    
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
    print("Closest texts:")
    for d, text in distances[:closest_n]:
        print(d)
        print(text)
        print('*********************')

    print('******************************************************')

def _compute_single_lexical_matching_score(lw1: Dict[str, float], lw2: Dict[str, float]):
    scores = 0
    for token, weight in lw1.items():
        if token in lw2:
            scores += weight * lw2[token]
    return scores



if __name__ == "__main__":
    # tuple = execute_query(get_query_pos_embedding_nth(2), single_item=True)
    # embedding_string = tuple[0]
    # embedding_text = tuple[1]

    # query= generate_query(embedding_text)


    # print(query)
    # print('*********************************************')

    # print_closest_and_furthest_embeddings_cosine(embedding_string, 145, 30)


    # tuple = execute_query(get_query_pos_embedding_sparse_nth(135), single_item=True)
    # embedding_string = tuple[0]
    # embedding_text = tuple[1]

    # query= generate_query(embedding_text)


    # print(query)
    # print('*********************************************')

    # print_closest_embeddings_sparse(embedding_string, 20)

    # tuple = execute_query(query_one_uuid1_garbagy_by_embedding_sparse, single_item=True)
    # embedding_string = tuple[0]

    # print('*********************************************')

    # print_closest_embeddings_sparse(embedding_string, 300)

    # test gabage

    tuple = execute_query(query_one_uuid1_garbagy_by_embedding, single_item=True)
    embedding_string = tuple[0]

    print('*********************************************')

    print_closest_and_furthest_embeddings_cosine(embedding_string, 1000, 30)
