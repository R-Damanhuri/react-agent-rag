import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.vector_db.vector_store import DocumentIndexer
from modules.utils.loader import DoclingPDFLoader

class TestDocumentIndexer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.indexer = DocumentIndexer(collection_name="test", store_path='tests/vector_store')
        cls.loader = DoclingPDFLoader("D:/mtgrdama2455/Exploration/react-agent-rag/tests/data/input/document-with-table.pdf")  # Load the specified PDF
        cls.document = cls.loader.load()

    def test_chunk_documents_semantic(self):
        chunks = self.indexer.chunk_text(self.document, number_of_chunks=20, chunk_type='semantic')
        self.assertGreater(len(chunks), 0, "No chunks were created from the document.")

    def test_chunk_documents_eos(self):
        chunks = self.indexer.chunk_text(self.document, chunk_type='eos')
        self.assertGreater(len(chunks), 0, "No chunks were created from the document.")

    def test_chunk_documents_default(self):
        chunks = self.indexer.chunk_text(self.document)
        self.assertGreater(len(chunks), 0, "No chunks were created from the document.")

    def test_insert_documents(self):
        chunks = self.indexer.chunk_text(self.document, chunk_type='eos')
        initial_count = self.indexer.collection.count()  # Get the initial count of documents
        self.indexer.insert_documents(chunks)
        new_count = self.indexer.collection.count()
        self.assertGreater(new_count, initial_count, "Documents were not inserted successfully.")

if __name__ == '__main__':
    unittest.main()