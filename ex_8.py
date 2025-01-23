import requests
import time

url = "https://playground.learnqa.ru/ajax/api/longtime_job"

# 1. Создаем задачу. Вводим token и seconds
response = requests.get(url)
response_json = response.json()

token = response_json['token']
seconds = response_json['seconds']

print(f"Token: {token}")
print(f"Seconds: {seconds}")

# 2. Сразу же делаем GET-запрос с token до того, как задача готова
get_response_before_end = requests.get(url, params={"token": token})
get_response_before_end_json = get_response_before_end.json()

print(f"Status before waiting: {get_response_before_end_json['status']}")
if get_response_before_end_json['status'] != "Job is NOT ready":
    print("Ошибка: Задача должна быть не выполнена")
    exit(1)

# 3. Ждем нужное количество секунд
time.sleep(seconds)

# 4. Делаем еще один GET-запрос с token после того, как задача готова
get_response_after_end = requests.get(url, params={"token": token})
get_response_after_end_json = get_response_after_end.json()

print(f"Status after waiting: {get_response_after_end_json['status']}")
if get_response_after_end_json['status'] != "Job is ready":
    print("Ошибка: Задача должна быть готова")
    exit(1)

if 'result' not in get_response_after_end_json:
    print("Ошибка: Результат должен быть в ответе")
    exit(1)

print(f"Result: {get_response_after_end_json['result']}")