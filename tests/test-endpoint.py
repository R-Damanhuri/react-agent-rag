import sys
import os
import unittest
from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api
from flask_cors import CORS

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.generator.agent import Agent
from modules.vector_db.vector_store import DocumentRetriever
from endpoints.chat import Chat

load_dotenv()

retriever = DocumentRetriever(collection_name="test", store_path='tests/vector_store')
retriever_tool = retriever.as_tool()
agent = Agent(tools=[retriever_tool])

app = Flask(__name__)

debug = True
CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

api.add_resource(Chat, '/chat', resource_class_kwargs={'agent': agent})

if __name__ == '__main__':
    app.run(debug=debug, host='0.0.0.0')