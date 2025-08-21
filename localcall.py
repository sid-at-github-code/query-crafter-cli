import requests
import pyperclip

def nl_to_query_ollama(nl_query: str, schema: str, query_type: str, model: str = "llama3") -> str:
    
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": model,
        "prompt": f"""
        Convert this NL statement into a {query_type} query:

        NL: {nl_query}
        Schema:
        {schema}

        RULES:
        ONLY return the raw query/code.
        Do NOT include markdown formatting (no ```sql, ```python, or backticks).
        Do NOT include explanations, comments, or extra text.
        Output must start directly with the query/statement.
        Format the query/statement with proper new line .
        """,
        "stream": False
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        query = data.get("response", "").strip()
        
        # Copy to clipboard
        pyperclip.copy(query)
        
        print("\n--- Generated Query ---")
        print(query)
        return query
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")


# Example usage
if __name__ == "__main__":
    schema = """CREATE TABLE orders (
        order_id INT PRIMARY KEY,
        customer_id INT NOT NULL,
        order_date DATE NOT NULL,
        total_amount DECIMAL(10,2) NOT NULL,
        status VARCHAR(20) CHECK (status IN ('Pending','Shipped','Delivered','Cancelled')),
        payment_method VARCHAR(20) CHECK (payment_method IN ('Card','UPI','COD','NetBanking')),
        shipping_address TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )"""
    
    model = "llama3"
    query_type = "sqlite"
    nl_query = "Show me the total sales amount grouped by payment method, but only for orders that are already delivered."

    nl_to_query_ollama(nl_query, schema, query_type, model)
