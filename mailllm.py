import requests
import json

# Call the LLM to get answers
class MailLLM():
    def __init__(self,url,api_key):
        # Dify API server url
        self.dify_url = url #"http://localhost/v1/chat-messages"
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

    # Get email classfication from Analysis LLM
    def ask_analysis_llm(self,question,sentiment):
        data = {
            "inputs": {},
            "query": f"{question}. To summarize the content of this sentence, please only choose one of {sentiment}.",
            "response_mode": "blocking",
            "conversation_id": "",
            "user": "auto"
        }
        # send POST request to the Dify app
        response = requests.post(self.dify_url, headers=self.headers, data=json.dumps(data))
        # get the answer
        if response.status_code == 200:
            answer = response.json().get("answer")
        else:
            answer = ""
            print(f"Error ask_analysis_llm: {response.status_code}, {response.text}")
        return answer

    # Get email classfication from Reply LLM
    def ask_reply_llm(self,question):
        data = {
            "inputs": {},
            "query": f"{question}?",
            "response_mode": "blocking",
            "conversation_id": "",
            "user": "auto"
        }
        # send POST request to the Dify app
        response = requests.post(self.dify_url, headers=self.headers, data=json.dumps(data))
        # get the answer
        if response.status_code == 200:
            answer = response.json().get("answer")
        else:
            answer = ""
            print(f"Error query_reply_llm: {response.status_code}, {response.text}")
        return answer