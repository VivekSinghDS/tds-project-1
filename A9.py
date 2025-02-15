from sklearn.metrics.pairwise import cosine_similarity
from typing import Optional, List 
import requests 
import numpy as np 
import os
from dotenv import load_dotenv 

load_dotenv()
AIPROXY_TOKEN = os.environ.get('AIPROXY_TOKEN')
def get_embeddings(texts: List[str]):

    response =  requests.post(
            'https://aiproxy.sanand.workers.dev/openai/v1/embeddings',
            headers={"Authorization": f"Bearer {AIPROXY_TOKEN}"},
            json={"model": "text-embedding-3-small", "input": texts},
        )
    embeddings = np.array([emb["embedding"] for emb in response.json()["data"]])

    return embeddings

def run_a9(input_file: str, output_file: str, no_of_similar_texts: str):
    def is_allowed_path(file_path: str) -> bool:
        abs_path = os.path.abspath(file_path)
        return abs_path.startswith("/data/")
            
    if not is_allowed_path(input_file) or not is_allowed_path(output_file):
        raise PermissionError(f"Access outside /data/ is not allowed: {input_file} or {output_file}")

    no_of_similar_texts = int(no_of_similar_texts)
    import numpy as np
    # Load comments from the file
    with open(input_file, "r") as file:
        documents = file.readlines()
    
    # Remove newline characters
    documents = [comment.strip() for comment in documents]
    
    # Load a pre-trained sentence transformer model
    line_embeddings = get_embeddings(documents)
    
    
    # Compute pairwise cosine similarity
    similarity_matrix = cosine_similarity(line_embeddings)
    
    # Find the most similar pair (excluding self-similarity)
    np.fill_diagonal(similarity_matrix, -1)  # Ignore self-similarity
    most_similar_indices = np.unravel_index(np.argmax(similarity_matrix), similarity_matrix.shape)
    # print(most_similar_indices, ' is this one')
    # Get the most n similar texts
    similar_texts = []
    for i in range(no_of_similar_texts * 2):
        similar_texts.append(documents[most_similar_indices[i]])
    # print(similar_texts, ' is the similar texts')
    # Write the them to the output file
    with open(output_file, "w") as file:
        for text in similar_texts:
            print('number ', text)
            file.write(text + "\n")


# run_a9('./data/comments.txt', './data/comments-similar.txt', '1')