import os
from typing import List
from openai import OpenAI
from EmbeddingGenerator import EmbeddingGenerator

class OpenAIEmbeddingsGenerator(EmbeddingGenerator):
    def __init__(self, api_key_env_var_name):
        api_key = os.environ[api_key_env_var_name]
        self.client = OpenAI(api_key=api_key)

    def generate_single_embedding(self, text:str):
        responce = self.client.embeddings.create(input=text, model="text-embedding-3-small")
        return responce.data[0].embedding
    
    def generate_batch_embedding(self, texts:List[str]):
        responce = self.client.embeddings.create(input=texts, model="text-embedding-3-small")
        return [r.embedding for r in responce.data]
    
        