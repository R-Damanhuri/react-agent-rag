from dotenv import load_dotenv
from langchain_chroma import Chroma
from chromadb import PersistentClient
from langchain.tools.retriever import create_retriever_tool
from modules.generator.llm import LLM

from langchain_experimental.text_splitter import SemanticChunker
from uuid import uuid4
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import Iterator

load_dotenv()

class VectoreStore:
    def __init__(self, collection_name: str, store_path: str):
        persistent_client = PersistentClient(store_path)
        self.embedding_function = LLM().embedding_model
        self.collection = persistent_client.get_or_create_collection(collection_name)
        self.vector_store = Chroma(
            client=persistent_client,
            collection_name=collection_name,
            embedding_function= self.embedding_function,
        )

class DocumentIndexer(VectoreStore):
    def __init__(self, collection_name: str, store_path: str):
        super().__init__(collection_name, store_path)

    def chunk_text(self, documents: Iterator[Document], number_of_chunks: int = 20, chunk_type: str= "default"):
        combined_page_content = []
        metadatas = []
        for doc in documents:
            combined_page_content.append(doc.page_content)
            metadatas.append(doc.metadata)
        
        if chunk_type == "semantic":
            splitter = SemanticChunker(
                self.embedding_function,
                number_of_chunks=number_of_chunks
            )
            chunks = splitter.create_documents(combined_page_content, metadatas)

        elif chunk_type == "eos":
            chunks = []
            for page_content, metadata in zip(combined_page_content, metadatas):
                inpage_chunks = page_content.split("</EOS>")
                for inpage_chunk in inpage_chunks:
                   chunks.append(Document(page_content=inpage_chunk, metadata=metadata))

        else:
            splitter = RecursiveCharacterTextSplitter()
            chunks = splitter.create_documents(combined_page_content, metadatas)

        return chunks

    def insert_documents(self, document_chunks):
        uuids = [str(uuid4()) for _ in range(len(document_chunks))]
        self.vector_store.add_documents(documents=document_chunks, ids=uuids)

class DocumentRetriever(VectoreStore):
    def __init__(self, collection_name: str, store_path: str):
        super().__init__(collection_name, store_path)
        self.retriever = self.vector_store.as_retriever()
    
    def as_tool(self):
        retriever_tool  = create_retriever_tool(
            self.retriever,
            "retriever_tool",
            "Retrieve documents from vectore store"
        )
        return retriever_tool