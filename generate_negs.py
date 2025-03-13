import random
from typing import List
from data_utils import rank_embeddings_by_cosine_with_texts


# def get_100_random_embeddings_text_by_cosine(embedding_in_json_string: str,  clean_data, random_n: int = 15) -> List[str]:
#     ranked_data = rank_embeddings_by_cosine_with_texts(embedding_in_json_string, clean_data)
#     first_100_data = ranked_data[10:110]
#     random_data = random.sample(first_100_data, random_n)
#     random_embeddings_texts = [text for _, _, text, _ in random_data]

#     return random_embeddings_texts


# def get_100_random_embeddings_text_by_cosine(current_index,  clean_data, distance_matrix, random_n: int = 15) -> List[str]:
#     embedding_distances = []
#     for i, row in enumerate(clean_data):
#             embedding_text = row[2]
#             distance = distance_matrix[current_index, i].item()
#             embedding_distances.append((embedding_text, distance))
#     embedding_distances.sort(key=lambda x: x[1])
#     first_100_data = embedding_distances[10:110]
#     random_data = random.sample(first_100_data, random_n)
#     random_embeddings_texts = [text for text, _ in random_data] 

#     return random_embeddings_texts

def get_100_random_embeddings_text_by_cosine(current_index, clean_data, sorted_indices, random_n: int = 15) -> List[str]:
    # Get the sorted indices for the current embedding
    sorted_indices_for_current = sorted_indices[current_index]
    
    # Skip the first 10 closest embeddings and take the next 100
    selected_indices = sorted_indices_for_current.tolist()[10:110]
    
    # 从selected_indices范围内随机选择random_n个独一无二的索引
    random_indices = random.sample(selected_indices, random_n)
    
    # 提取随机选择的索引对应的嵌入文本
    random_embeddings_texts = [clean_data[i][2] for i in random_indices]
    
    return random_embeddings_texts