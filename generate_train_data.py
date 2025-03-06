import json
from data_utils import get_clean_data
from invoke_claude import generate_query
from generate_negs import get_random_closest_embeddings_text_by_cosine, get_hard_neg_embeddings_text_by_cosine, get_random_embeddings_text_by_cosine, get_random_closest_embeddings_sparse_text, get_100_random_embeddings_text_by_cosine

def generate_random_closest_train_data(output_file: str):
    clean_data = get_clean_data()
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for embedding, _, embedding_text, _ in clean_data[:2]:
            query = generate_query(embedding_text)
            pos = [embedding_text]
            neg = get_random_closest_embeddings_text_by_cosine(embedding, clean_data, closest_n=5)
            
            data = {
                "query": query,
                "pos": pos,
                "neg": neg
            }
            
            f.write(json.dumps(data) + '\n')

def generate_hard_neg_train_data(output_file: str):
    clean_data = get_clean_data()
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for embedding, _, embedding_text, _ in clean_data[:2]:
            query = generate_query(embedding_text)
            pos = [embedding_text]
            neg = get_hard_neg_embeddings_text_by_cosine(embedding, clean_data, closest_n=5)
            
            data = {
                "query": query,
                "pos": pos,
                "neg": neg
            }
            
            f.write(json.dumps(data) + '\n')

def generate_random_embeddings_train_data(output_file: str):
    clean_data = get_clean_data()
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for embedding, _, embedding_text, _ in clean_data[:2]:
            query = generate_query(embedding_text)
            pos = [embedding_text]
            neg = get_random_embeddings_text_by_cosine(embedding, clean_data, random_n=5)
            
            data = {
                "query": query,
                "pos": pos,
                "neg": neg
            }
            
            f.write(json.dumps(data) + '\n')

def generate_random_closest_embeddings_sparse_train_data(output_file: str):
    clean_data = get_clean_data()
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for _, embedding_sparse, embedding_text, _ in clean_data[:2]:
            query = generate_query(embedding_text)
            pos = [embedding_text]
            neg = get_random_closest_embeddings_sparse_text(embedding_sparse, clean_data, closest_n=5)
            
            data = {
                "query": query,
                "pos": pos,
                "neg": neg
            }
            
            f.write(json.dumps(data) + '\n')

def generate_100_random_embeddings_text_by_cosine(output_file: str):
    clean_data = get_clean_data()
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for embedding, _, embedding_text, _ in clean_data[:2]:
            query = generate_query(embedding_text)
            pos = [embedding_text]
            neg = get_100_random_embeddings_text_by_cosine(embedding, clean_data, closest_n=5)
            
            data = {
                "query": query,
                "pos": pos,
                "neg": neg
            }
            
            f.write(json.dumps(data) + '\n')

if __name__ == "__main__":
    # generate_random_closest_train_data("1_random_closest.jsonl")
    # generate_hard_neg_train_data("2_hard_neg.jsonl")
    # generate_random_embeddings_train_data("3_random_embeddings.jsonl")
    # generate_random_closest_embeddings_sparse_train_data("4_embeddings_sparse.jsonl")
    generate_random_closest_embeddings_sparse_train_data("5_100_random.jsonl")