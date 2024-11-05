import requests
 
endpoint = "https://api.ttapi.io/luma/v1/generations"
 
headers = {
    "TT-API-KEY": "6e33cca4-b0e6-66d3-9069-1b2ae8629bd5"
}
data = {
    "userPrompt": "a cute cat",
    "enhancePrompt": True,
    "imageUrl": "",
    "hookUrl": ""
}
response = requests.post(endpoint, headers=headers, json=data)
print(response.status_code)
print(response.json())