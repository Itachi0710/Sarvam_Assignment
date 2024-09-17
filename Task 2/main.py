#importing all lib's
from fastapi import FastAPI
from pydantic import BaseModel
import openai
from datetime import datetime

app = FastAPI()

def get_weather_info(location: str):
    return f"Weather in {location}: Sunny, 25°C"

def get_latest_news_summary(keyword: str):
    return f"Latest news about {keyword}: Tech company launches new product."


# Agent decision making section this hlpes agent to decide which action to perfoem
class Agent:
    def __init__(self):
        pass

    def decide_action(self, query: str):

        vectordb_keywords = ["information", "search", "lookup", "find"]
        weather_keywords = ["weather", "forecast"]

        if query.lower() in ["hello", "hi", "hey"]:
            return "greet"
        elif any(keyword in query.lower() for keyword in vectordb_keywords):
            return "vectordb"
        elif "time" in query.lower():
            return "time"
        elif any(keyword in query.lower() for keyword in weather_keywords):
            return "weather"
        elif "news" in query.lower():
            return "news"
        else:
            return "unknown"

    def perform_action(self, action: str, query: str):
        if action == "greet":
            return {"response": "Hello! How can I assist you today?"}
        elif action == "vectordb":

            return {"response": "Fetching information from VectorDB..."}
        elif action == "time":
            return {"response": f"The current time is {datetime.now().strftime('%H:%M:%S')}"}
        elif action == "weather":
            location = "New York"
            return {"response": get_weather_info(location)}
        elif action == "news":
            keyword = "tech"
            return {"response": get_latest_news_summary(keyword)}
        else:
            return {"response": "I'm not sure how to help with that."}


class QueryRequest(BaseModel):
    query: str


agent = Agent()


@app.post("/agent")
async def handle_agent(request: QueryRequest):
    query = request.query
    action = agent.decide_action(query)
    response = agent.perform_action(action, query)

    return response
