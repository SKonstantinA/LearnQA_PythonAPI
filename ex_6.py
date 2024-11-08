import requests

response = requests.post("https://playground.learnqa.ru/api/long_redirect")

last_response = response.history[-1]
redirect_count = len(response.history)

print(redirect_count)
print(last_response.url)