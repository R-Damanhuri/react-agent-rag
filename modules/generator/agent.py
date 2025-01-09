from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from modules.generator.llm import LLM

load_dotenv()

class Agent:
    def __init__(self, tools, prompt = hub.pull("hwchase17/react")):
        self.llm = LLM().chat_model
        self.prompt = prompt
        self.tools = tools

    def generate_response(self, question):
        agent = create_react_agent(self.llm, self.tools, self.prompt)
        agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)
        result = agent_executor.invoke({"input": question})
        return result["output"]
