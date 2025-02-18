import requests

class TestHeader:

    def test_header_values(self):
        url = "https://playground.learnqa.ru/api/homework_header"

        response = requests.get(url)

        assert response.status_code == 200, "Wrong status code"
        headers = response.headers

        assert headers is not None, "Headers for the method are empty"
        for header_name, header_value in headers.items():
            print(f"Header name: {header_name}, Header value: {header_value}")
            expected_header_name = header_name
            expected_value = header_value

            assert expected_header_name in headers, f"Header '{expected_header_name}' is not found"
            assert headers[expected_header_name] == expected_value, f"Header '{expected_header_name}' has wrong value"