import unittest
import sys
import os

# Tambahkan folder utama "react-agent-rag" ke sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.vector_db.vector_store import DocumentRetriever

class TestDocumentRetriever(unittest.TestCase):

    def setUp(self):
        self.retriever = DocumentRetriever(collection_name="test", store_path='tests/vector_store')

    def test_get_retriever_tool(self):
        self.assertIsNotNone(self.retriever.as_tool())

if __name__ == '__main__':
    unittest.main()