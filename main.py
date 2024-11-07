import requests

# payload = {"name": "User"}
# response = requests.get("https://playground.learnqa.ru/api/hello", params=payload)
# print(response.text)

response = requests.get("https://playground.learnqa.ru/api/hello", params={"name": "User"})
parsed_response_text = response.json()
print(parsed_response_text["answer"])