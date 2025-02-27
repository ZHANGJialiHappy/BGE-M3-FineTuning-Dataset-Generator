def get_query_pos_embedding_nth(n: int) -> str:
    return f"""
    SELECT embedding, embedding_text
    FROM v9__chatbot_documents
    WHERE source_uri like '%58548175-ccef-4d6a-987c-f597b7d4d225%'
    OFFSET {n - 1}
    LIMIT 1
    """

def get_query_pos_embedding_sparse_nth(n: int) -> str:
    return f"""
    SELECT embedding_sparse, embedding_text
    FROM v9__chatbot_documents
    WHERE source_uri like '%58548175-ccef-4d6a-987c-f597b7d4d225%'
    OFFSET {n - 1}
    LIMIT 1
    """
query_all_data = """
SELECT embedding, embedding_sparse, embedding_text
FROM v9__chatbot_documents
WHERE source_uri like '%58548175-ccef-4d6a-987c-f597b7d4d225%'
"""

query_data_by_embedding = """
SELECT embedding, embedding_text
FROM v9__chatbot_documents
WHERE source_uri like '%58548175-ccef-4d6a-987c-f597b7d4d225%'
"""

query_data_by_embedding_sparse = """
SELECT embedding_sparse, embedding_text
FROM v9__chatbot_documents
WHERE source_uri like '%58548175-ccef-4d6a-987c-f597b7d4d225%'
"""

query_alarm_data = """
SELECT embedding, embedding_text
FROM v9__chatbot_documents
WHERE source_uri like '%me_c_mk2%'
"""

query_one_gabagy_by_embedding = """
SELECT embedding
FROM v9__chatbot_documents
WHERE source_uri like '%58548175-ccef-4d6a-987c-f597b7d4d225%' 
AND embedding_text LIKE '%###

Copyright © 2023 MAN Energy Solutions%'
LIMIT 1
"""

query_one_gabagy_by_embedding_sparse = """
SELECT embedding_sparse
FROM v9__chatbot_documents
WHERE source_uri like '%58548175-ccef-4d6a-987c-f597b7d4d225%' 
AND embedding_text LIKE '%###

Copyright © 2023 MAN Energy Solutions%'
LIMIT 1
"""