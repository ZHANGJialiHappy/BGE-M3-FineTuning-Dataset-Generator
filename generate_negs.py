import random
from typing import List
# from queries import get_query_pos_embedding_nth, get_query_pos_embedding_sparse_nth, query_uuid1_data_by_embedding, query_uuid1_data_by_embedding_sparse, query_one_uuid1_garbagy_by_embedding,query_one_uuid1_garbagy_by_embedding_sparse
from data_utils import execute_query, get_clean_data, rank_embeddings_by_cosine_with_texts, rank_embeddings_by_dot_product_with_texts
import time

def get_random_closest_embeddings_text_by_cosine(embedding_in_json_string: str, clean_data, closest_n: int = 15) -> List[str]:
    # clean_data = get_clean_data()
    
    # start_time = time.time()
    random_200_data=random.sample(clean_data, 200)
    ranked_data = rank_embeddings_by_cosine_with_texts(embedding_in_json_string, random_200_data)
    closest_embeddings_texts = [text for _, _, text, _ in ranked_data[10:closest_n+10]]
    print("generate_random_closest_train_data")
    for _, _, _, distance in ranked_data[10:closest_n+10]:
        print(distance)
    print('******************************************************')
    # end_time = time.time()
    # print(f"Time taken: {end_time - start_time} seconds")

    return closest_embeddings_texts

def get_hard_neg_embeddings_text_by_cosine(embedding_in_json_string: str,  clean_data, closest_n: int = 15) -> List[str]:

    ranked_data = rank_embeddings_by_cosine_with_texts(embedding_in_json_string, clean_data)
    closest_embeddings_texts = [text for _, _, text, _  in ranked_data[10:closest_n+10]]
    print("generate_hard_neg_train_data")
    for _, _, _, distance in ranked_data[10:closest_n+10]:
        print(distance)
    print('******************************************************')

    return closest_embeddings_texts

def get_random_embeddings_text_by_cosine(embedding_in_json_string: str, clean_data, random_n: int = 15 ) -> List[str]:
    
    ranked_data = rank_embeddings_by_cosine_with_texts(embedding_in_json_string, clean_data)

    intercepted_data= ranked_data[10:]

    random_data=random.sample(intercepted_data, random_n)

    random_embeddings_texts = [text for _, _, text, _ in random_data]

    print("generate_random_embeddings_train_data")
    for _, _, _, distance in random_data:
        print(distance)
    print('******************************************************')

    return random_embeddings_texts


def get_random_closest_embeddings_sparse_text(embedding_sparse_string, clean_data, closest_n=15):


    random_200_data=random.sample(clean_data, 200)
    
    ranked_data = rank_embeddings_by_dot_product_with_texts(embedding_sparse_string, random_200_data)

    closest_embeddings_texts = [text for _, _, text, _  in ranked_data[10:closest_n+10]]

    print("generate_random_closest_embeddings_sparse_train_data")
    for _, _, _, distance in ranked_data[10:closest_n+10]:
        print(distance)
    print('******************************************************')

    return closest_embeddings_texts

def get_100_random_embeddings_text_by_cosine(embedding_in_json_string: str,  clean_data, random_n: int = 15) -> List[str]:
    ranked_data = rank_embeddings_by_cosine_with_texts(embedding_in_json_string, clean_data)
    first_100_data = ranked_data[10:110]
    random_data = random.sample(first_100_data, random_n)
    random_embeddings_texts = [text for _, _, text, _ in random_data]

    return random_embeddings_texts


# if __name__ == "__main__":
    # result = execute_query(get_query_pos_embedding_nth(1), single_item=True)
    # if result:
    #     embedding_json_string = result[0]
    #     get_random_closest_embeddings_text_by_cosine(embedding_json_string)
    # else:
    #     print("No data found")

    # result = execute_query(get_query_pos_embedding_nth(1), single_item=True)
    # if result:
    #     embedding_json_string = result[0]
    #     get_hard_neg_embeddings_text_by_cosine(embedding_json_string)
    # else:
    #     print("No data found")

    # result = execute_query(get_query_pos_embedding_sparse_nth(1), single_item=True)
    # if result:
    #     embedding_sparse = result[0]
    #     get_random_closest_embeddings_sparse_text(embedding_sparse)
    # else:
    #     print("No data found")
    




















# def get_furthest_embeddings_uclidean(embedding_string, furthest_n=5):
#     random_data=random.sample(query_uuid1_data_by_embedding, 100)
    
#     distances = []
    
#     # Convert the input embedding to a numpy array
#     input_embedding = np.array(json.loads(embedding_string), dtype=np.float64)
    
#     for row in random_data:
#         current_embedding = np.array(json.loads(row[0]), dtype=np.float64)
#         current_embedding_text = row[1]
        
#         # Calculate the Euclidean distance between the input embedding and the current embedding
#         distance = np.linalg.norm(input_embedding - current_embedding)
        
#         distances.append((distance, current_embedding_text))
    
#     # Sort the distances in descending order and get the top N
#     distances.sort(reverse=True, key=lambda x: x[0])
#     furthest_embeddings_texts = [text for _, text in distances[:furthest_n]]
#     furthest_embeddings_distance = [distance for distance, _ in distances[:furthest_n]]
#     print(furthest_embeddings_distance)
#     return furthest_embeddings_texts


# def get_random_embeddings(embedding_string, random_n=5):
#     # Query to get all embeddings and their corresponding embedding_text
#     query = """
#     SELECT embedding, embedding_text
#     FROM v9__chatbot_documents
#     WHERE source_uri like '%58548175-ccef-4d6a-987c-f597b7d4d225%'
#     LIMIT 50
#     """
    
#     data = execute_query(query)
    
#     if not data:
#         return None
    
#     input_embedding = np.array(json.loads(embedding_string), dtype=np.float64)
    
#     # Filter out the input embedding from the data
#     filtered_data = [row for row in data if not np.array_equal(np.array(json.loads(row[0]), dtype=np.float64), input_embedding)]
    
#     # Get 5 random embeddings and their corresponding embedding_text
#     random_samples = random.sample(filtered_data, random_n)
#     random_text_samples = [row[1] for row in random_samples]
    
#     return random_text_samples