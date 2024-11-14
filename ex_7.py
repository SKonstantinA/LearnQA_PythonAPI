import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

# Задача 1.

print("Задача 1. Делает http-запрос любого типа без параметра method.")

get_response = requests.get(url)
print("GET Response:", get_response.text)

post_response = requests.post(url)
print("POST Response:", post_response.text)

put_response = requests.put(url)
print("PUT Response:", put_response.text)

delete_response = requests.delete(url)
print("DELETE Response:", delete_response.text)

# Задача 2.

print("Задача 2. Делает http-запрос не из списка. Например, HEAD.")

head_response = requests.head(url)
# Добавил проверку кода ответа, потому что сам ответ пустой
if not head_response.text:
    print(f"Response is empty. Status code: {head_response.status_code}")
else:
    print(f"Response: {head_response.text}")

# Задача 3.

print("Задача 3. Делает запрос с правильным значением method.")

get_response = requests.get(url, params={"method": "GET"})
print("GET Response:", get_response.text)

post_response = requests.post(url, data={"method": "POST"})
print("POST Response:", post_response.text)

put_response = requests.put(url, data={"method": "PUT"})
print("PUT Response:", put_response.text)

delete_response = requests.delete(url, data={"method": "DELETE"})
print("DELETE Response:", delete_response.text)

# Задача 4.

print("Задача 4. Проверяет все возможные сочетания реальных типов запроса и значений параметра method.")

methods = ['GET', 'POST', 'PUT', 'DELETE']

# Перебираем все методы
for real_method in methods:
    for method_value in methods:
        if real_method == 'GET':
            response = requests.get(url, params={"method": method_value})
        else:
            response = requests.request(real_method, url, data={"method": method_value})

        # Проверяю результат
        expected_response = '{"success":"!"}' if real_method == method_value else 'Wrong method provided'

        if response.text == expected_response:
            print(f"Real Method: {real_method}, Method Value: {method_value}, Результат: {response.text}. Ожидаемый.")
        else:
            print(
                f"Real Method: {real_method}, Method Value: {method_value}. Ожидаемый результат не совпадает с фактическим. Ожидаемый: {expected_response}, фактический: {response.text}. ")