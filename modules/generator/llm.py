from dotenv import load_dotenv
import os
from langchain_openai import AzureOpenAIEmbeddings
from langchain_openai import AzureChatOpenAI

load_dotenv()

class LLM:
    def __init__(self):
        self.embedding_model = AzureOpenAIEmbeddings(
            model=os.environ["OPENAI_API_EMBEDDINGS_MODEL"],
            api_version=os.environ["OPENAI_API_VERSION"],
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=os.environ["OPENAI_API_AZURE_KEY"]
        )
        self.chat_model = AzureChatOpenAI(
            model=os.environ["OPENAI_AZURE_MODEL"],
            api_version=os.environ["OPENAI_API_VERSION"],
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=os.environ["OPENAI_API_AZURE_KEY"],
            temperature=0,
        )
    
    def get_embedding(self, query):
        return self.embedding_model.embed_query(query)