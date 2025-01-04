import requests
endpoint = "https://api.ttapi.io/luma/v1/fetch"
headers = {
    "TT-API-KEY": "6e33cca4-b0e6-66d3-9069-1b2ae8629bd5"
}
data = {
    "jobId": "22539de4-9127-4433-a58f-ac91ea6378eb",
}
response = requests.post(endpoint, headers=headers, json=data)
print(response.status_code)
print(response.json()) 