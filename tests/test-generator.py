import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.vector_db.vector_store import DocumentRetriever
from modules.generator.agent import Agent

class TestAgent(unittest.TestCase):
    def setUp(self):
        self.retriever = DocumentRetriever(collection_name="test", store_path='tests/vector_store')
        self.retriever_tool = self.retriever.as_tool()
        self.responser = Agent(tools=[self.retriever_tool])

    def test_generate_response(self):
        response = self.responser.generate_response("apa yang menyebabkan kepesertaan berakhir?")
        self.assertIsNotNone(response)
        self.assertIn("berakhir", response)  # Adjust this assertion based on expected response content

if __name__ == '__main__':
    unittest.main()