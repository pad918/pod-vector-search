import os
from openai import OpenAI
from EmbeddingGenerator import EmbeddingGenerator

class OpenAIEmbeddingsGenerator(EmbeddingGenerator):
    def __init__(self, api_key_env_var_name):
        api_key = os.environ[api_key_env_var_name]
        self.client = OpenAI(api_key=api_key)

    def generate_embeddings(self, text:str):
        responce = self.client.embeddings.create(input=text, model="text-embedding-3-small")
        return responce.data[0].embedding
        