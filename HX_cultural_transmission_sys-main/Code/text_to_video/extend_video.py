import requests
endpoint = "https://api.ttapi.io/luma/v1/extend"
headers = {
    "TT-API-KEY": "6e33cca4-b0e6-66d3-9069-1b2ae8629bd5"
}
data = {
    "jobId": "ed1a1b01-7d64-4c8a-acaa-71185d23a2f3",
    "userPrompt": "a red car driving on a road",
}
response = requests.post(endpoint, headers=headers, json=data)
print(response.status_code)
print(response.json())