import numpy as np
import torch
import json
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

    
# def rank_embeddings_by_cosine_with_texts(embedding_in_json_string, data):
#     distances = []
#     input_embedding = torch.tensor(json.loads(embedding_in_json_string), dtype=torch.float64).reshape(1, -1).cuda()
    
#     # Prepare all embeddings in a batch
#     embeddings = [torch.tensor(json.loads(row[0]), dtype=torch.float64).reshape(1, -1) for row in data]
#     embeddings_batch = torch.cat(embeddings, dim=0).cuda()
    
#     # Calculate cosine similarities in batch
#     similarities = torch.mm(input_embedding, embeddings_batch.T).cpu().numpy().flatten()
    
#     # Convert similarities to distances (1 - similarity)
#     distances = [(data[i][0], data[i][1], data[i][2], 1 - similarities[i]) for i in range(len(data))]
    
#     distances.sort(key=lambda x: x[3])
        
#     return distances

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

# add new
def compute_sorted_distance_indices(clean_data):
    # Extract embeddings from clean_data
    embeddings = [json.loads(item[0]) for item in clean_data]
    
    # Convert embeddings to a PyTorch tensor
    embeddings_tensor = torch.tensor(embeddings, dtype=torch.float64)
    
    # Compute the cosine similarity matrix
    cosine_similarity_matrix = torch.matmul(embeddings_tensor, embeddings_tensor.T)
    
    # Convert the cosine similarity matrix to a distance matrix
    distance_matrix = 1 - cosine_similarity_matrix

    sorted_indices = torch.argsort(distance_matrix)
    
    return sorted_indices

def get_clean_data(csv_file_path, embedding_csv_file_path, garbage_n):
    # data = execute_query(query_all_data)
    df = pd.read_csv(csv_file_path)
    data = df.values.tolist()

    # embedding_in_json_string = execute_query(query_one_garbagy, single_item=True)[0]
    embedding_df = pd.read_csv(embedding_csv_file_path)
    embedding_in_json_string = embedding_df.iloc[0, 0]

    ranked_data = rank_embeddings_by_cosine_with_texts(embedding_in_json_string, data)

    clean_data = ranked_data[garbage_n:]

    return clean_data




