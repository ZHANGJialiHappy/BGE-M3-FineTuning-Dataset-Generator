import numpy as np
import json
import random
from typing import List
from queries import get_query_pos_embedding_nth, get_query_pos_embedding_sparse_nth, query_data_by_embedding, query_data_by_embedding_sparse, query_one_gabagy_by_embedding,query_one_gabagy_by_embedding_sparse
# from invoke_claude import filter_data
from data_utils import execute_query, fetch_random_data, get_clean_data, rank_embeddings_by_cosine_with_texts, rank_embeddings_by_dot_product_with_texts

def get_closest_embeddings_text_by_cosine(embedding_in_json_string: str,  closest_n: int = 15) -> List[str]:
    clean_data = get_clean_data()
    
    ranked_data = rank_embeddings_by_cosine_with_texts(embedding_in_json_string, clean_data)

    closest_embeddings_texts = [text for _, _, text in ranked_data[10:closest_n+10]]

    return closest_embeddings_texts


def get_random_embeddings_text_by_cosine(embedding_in_json_string: str,  random_n: int = 15 ) -> List[str]:
    clean_data=get_clean_data()
    
    ranked_distances = rank_embeddings_by_cosine_with_texts(embedding_in_json_string, clean_data)

    intercepted_distances = ranked_distances[10:210]

    random_data=random.sample(intercepted_distances, random_n)
    print(len(random_data))

    return random_data


def get_closest_embeddings_sparse_text(embedding_sparse_string, closest_n=5):
    clean_data = get_clean_data()
    
    ranked_data = rank_embeddings_by_dot_product_with_texts(embedding_sparse_string, clean_data)

    closest_embeddings_texts = [text for _, _, text in ranked_data[10:closest_n+10]]

    return closest_embeddings_texts


if __name__ == "__main__":
    # result = execute_query(get_query_pos_embedding_nth(1), single_item=True)
    # if result:
    #     embedding_json_string = result[0]
    #     get_closest_embeddings_text_by_cosine(embedding_json_string)
    # else:
    #     print("No data found")

    result = execute_query(get_query_pos_embedding_nth(1), single_item=True)
    if result:
        embedding_json_string = result[0]
        get_random_embeddings_text_by_cosine(embedding_json_string)
    else:
        print("No data found")

    # result = execute_query(get_query_pos_embedding_sparse_nth(1), single_item=True)
    # if result:
    #     embedding_sparse = result[0]
    #     get_closest_embeddings_sparse_text(embedding_sparse)
    # else:
    #     print("No data found")
    




















def get_furthest_embeddings_uclidean(embedding_string, furthest_n=5):
    random_data=fetch_random_data(query_data_by_embedding, 100)
    
    distances = []
    
    # Convert the input embedding to a numpy array
    input_embedding = np.array(json.loads(embedding_string), dtype=np.float64)
    
    for row in random_data:
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