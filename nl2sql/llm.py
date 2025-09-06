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

def retry_req_call(rec_q: str, rec_o,  schema: str, query_type: str, reason="unknown"):
    prompt=f"""
    The given schea is : {schema}
    and you converted a NL command {rec_q} to database comand of query type {query_type} 
    your answer {rec_o}
    which is incorrect as {reason}
    now debug this and give a perfect answer now : 
    
    
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

def req_explain(rec_q,rec_o,schema,query_type):
    prompt=f"""
    The schema of the databse is {schema} of the type {query_type}
    explain in few lines how query line {rec_o} does {rec_q} and how it works
    
    rules:
        Do NOT include markdown formatting (no ```sql, ```python, or backticks).
        Output must start directly
        give only explnation, thats it nothing else.
    
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
                    "content": "You are a helpful assistant that converts natural language queries to SQL or anyother databse type queries which ever asked"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response.choices[0].message.content.strip(), response.usage.model_dump()
    
    def retrying(self,schema,query_type ,rec_q,rec_o, reason="unknown"):
        prompt=f"""
        The given schea is : {schema}
        and you converted a NL command {rec_q} to database comand of query type {query_type} 
        your answer {rec_o}
        generate another as {reason}
        now debug this and give a perfect answer now : 
        
        
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
                    "content": "You are a helpful assistant that converts natural language queries to SQL or any other database query type ."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response.choices[0].message.content.strip(), response.usage.model_dump()
    
    def explaining(self,schema,query_type, rec_q , rec_o):
        prompt=f"""
        The schema of the databse is {schema} of the type {query_type}
        explain in few lines how query line {rec_o} does {rec_q} and how it works
        
        rules:
            Do NOT include markdown formatting (no ```sql, ```python, or backticks).
            Output must start directly
            give only explnation, thats it nothing else.
        
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that converts natural language queries to SQL or any other database query type ."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response.choices[0].message.content.strip(), response.usage.model_dump()