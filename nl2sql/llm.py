import openai
import requests

def req_call(nl_query: str, schema: str, query_type: str):
    prompt = f"""
    Convert this NL statement into a {query_type} query:
    NL: {nl_query}.
    Schema:
    {schema}.
    RULES:
    ONLY return the raw query/code.
    Do NOT include markdown formatting (no ```sql, ```python, or backticks).
    Do NOT include explanations, comments, or extra text.
    Output must start directly
    Format the query/statement with proper next line
    """
    

    url = "https://apifreellm.com/api/chat"   
    
    payload = {
        "message": prompt
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    
    return response.json()["response"],  response.json()["usage"]["input_tokens"],response.json()["usage"]["output_tokens"]

        
class OpenAI:
    def __init__(self, api_key="", base_url=None, model="gpt-3.5-turbo"):
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url=base_url,
        )
        self.model = model

    def nl_to_query(self, nl_query: str, schema: str, query_type: str) -> tuple[str, dict]:
        prompt = f"""
        Convert this NL statement into a {query_type} query:
        NL: {nl_query}.
        Schema:
        {schema}.
        RULES:
        ONLY return the raw query/code.
        Do NOT include markdown formatting (no ```sql, ```python, or backticks).
        Do NOT include explanations, comments, or extra text.
        Output must start directly
        Format the query/statement with proper next line
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that converts natural language queries to SQL."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response.choices[0].message.content.strip(), response.usage.model_dump()
    
    
