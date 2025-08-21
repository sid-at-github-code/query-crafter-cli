import requests
import pyperclip

def nl_to_sql(nl_query: str, schema: str, type) -> str:
    """
    Convert natural language query to SQL using apifreellm.com API.
    
    Args:
        nl_query (str): Natural language query (example: "Show me total sales grouped by payment method").
        schema (str): Database schema to guide SQL generation.
    
    Returns:
        str: Generated SQL query (also copied to clipboard).
    """
    
    url = "https://apifreellm.com/api/chat"
    
    payload ={
    "message": f"""
    Convert this NL statement into a {type} query:
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
}
    
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()  # raises error if request failed
    
    sql_query = response.json().get("response", "").strip()
    
    # Copy to clipboard
    pyperclip.copy(sql_query)
    
    print( sql_query)
    
    return sql_query


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
    type="sqlite"
    nl_query = "Show me the total sales amount grouped by payment method, but only for orders that are already delivered."
    nl_to_sql(nl_query, schema,type)
