import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")

final_url = response.url
redirect_count = len(response.history)

print(f"Кол-во редиректов - {redirect_count}")
print(f"Последний URL - {final_url}")