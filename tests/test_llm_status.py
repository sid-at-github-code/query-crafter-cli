import requests

url = "https://apifreellm.com/api/chat"   # guessing endpoint from SDK usage
payload = {
    "message": "write a para about harvy spector"
}
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
    print(response.json()["response"], response.json()["usage"]["input_tokens"],response.json()["usage"]["output_tokens"])
else:
    print( response.status_code, response.text)