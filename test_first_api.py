import pytest
import requests

class TestFirstAPI:
    names = [
        ("Konstantin"),
        ("Tatiana"),
        ("")
    ]

#    def test_hello_call(self):
#        url = "https://playground.learnqa.ru/api/hello"
#        name = 'Konstantin'
#        data = {'name':name}
#
#        response = requests.get(url, params=data)
#
#        assert response.status_code == 200, "Wrong status code"
#
#        response_dict = response.json()
#        assert "answer", "There is no 'answer' field in the response"
#
#        expected_response_text = f"Hello, {name}"
#        actual_response_text = response_dict["answer"]
#        assert expected_response_text == actual_response_text, "Actual response text is not correct"

    @pytest.mark.parametrize('name', names)
    def test_hello_call(self, name):
        url = "https://playground.learnqa.ru/api/hello"
        data = {'name':name}

        response = requests.get(url, params=data)

        assert response.status_code == 200, "Wrong status code"

        response_dict = response.json()
        assert "answer" in response_dict, "There is no 'answer' field in the response"

        if len(name) == 0:
            expected_response_text = "Hello, someone"
        else:
            expected_response_text = f"Hello, {name}"

        actual_response_text = response_dict["answer"]
        assert expected_response_text == actual_response_text, "Actual response text is not correct"