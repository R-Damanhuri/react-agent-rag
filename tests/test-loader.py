import unittest
import sys
import os

# Tambahkan folder utama "react-agent-rag" ke sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.utils.loader import DoclingPDFLoader

class TestDoclingPDFLoader(unittest.TestCase):

    def test_load_document(self):
        input_file = "D:/mtgrdama2455/Exploration/react-agent-rag/tests/data/input/document-with-table.pdf"
        loader = DoclingPDFLoader(input_file)
        document = loader.load()
        self.assertIsNotNone(document)  # Check that document is not None
        self.assertTrue(len(document) > 0)  # Ensure that the document has content

if __name__ == '__main__':
    unittest.main()