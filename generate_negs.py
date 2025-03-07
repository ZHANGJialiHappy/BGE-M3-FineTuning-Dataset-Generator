import random
from typing import List
from data_utils import rank_embeddings_by_cosine_with_texts


def get_100_random_embeddings_text_by_cosine(embedding_in_json_string: str,  clean_data, random_n: int = 15) -> List[str]:
    ranked_data = rank_embeddings_by_cosine_with_texts(embedding_in_json_string, clean_data)
    first_100_data = ranked_data[10:110]
    random_data = random.sample(first_100_data, random_n)
    random_embeddings_texts = [text for _, _, text, _ in random_data]

    return random_embeddings_texts