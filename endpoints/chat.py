from flask import request
from flask_restful import Resource
import json
from datetime import datetime

class Chat(Resource):
    def __init__(self, agent):
        self.agent = agent
    
    def post(self):
        start = datetime.now()
        try:
            payload = json.loads(request.data.decode('utf-8'))
            question = payload['prompt'].lower()

    
            response = self.agent.generate_response(question)
            # response_tokens = response.response_metadata["token_usage"]["total_tokens"]

            return {
                "success": True,
                "output": response,
                # "token_consumed": response_tokens + extract_tokens,
                "response_time": str(datetime.now() - start)
            }
        
        except Exception as e:
            return {"success": False, "message": str(e)}