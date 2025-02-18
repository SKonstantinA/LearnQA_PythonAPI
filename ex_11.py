import requests

class TestCookie:

    def test_cookie_text(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"

        response = requests.get(url)

        assert response.status_code == 200, "Wrong status code"
        cookies  = response.cookies

        assert cookies is not None, "Cookies for the method are empty"
        for cookie in cookies:
            print(f"Cookie name: {cookie.name}, Cookie value: {cookie.value}")
            expected_cookie_name = cookie.name
            expected_value = cookie.value

        assert expected_cookie_name in cookies, f"Cookie '{expected_cookie_name}' is not found"
        assert cookies[expected_cookie_name] == expected_value, f"Cookie '{expected_cookie_name}' has wrong value"