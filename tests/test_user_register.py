from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import pytest

class TestUserRegister(BaseCase):
    exclude_params = [
        'password',
        'username',
        'firstName',
        'lastName',
        'email'
    ]

    names = [
        'firstName',
        'lastName'
    ]

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content '{response.content}'"

    def test_create_user_with_wrong_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format", f"Unexpected response content '{response.content}'"

    @pytest.mark.parametrize('condition', exclude_params)
    def test_user_registration_without_parameter(self, condition):
        data = self.prepare_registration_data()

        del data[condition]

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {condition}", \
            f"Unexpected response content '{response.content}'"

    @pytest.mark.parametrize('name', names)
    def test_create_user_with_short_name(self, name):
        data = self.prepare_registration_data()
        data[name] = 'A'

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"The value of '{name}' field is too short", \
            f"Unexpected response content '{response.content}'"

    @pytest.mark.parametrize('name', names)
    def test_create_user_with_long_name(self, name):
        data = self.prepare_registration_data()
        data[name] = ('Loremipsumdolorsitametconsecteturadipiscingelitseddoeiusmodtemporincididuntutlaboreetdoloremagnaa'
                      'liquaUtenimadminimveniamquisnostrudexercitationullamcolaborisnisualiquipexeacommodoconsequatDuisa'
                      'uteiruredolorinreprehenderitinvoluptatevelitessecillumdol')

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"The value of '{name}' field is too long", \
            f"Unexpected response content '{response.content}'"