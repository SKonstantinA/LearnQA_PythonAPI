from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import pytest
import allure

@allure.epic("Registration tests")
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

    @allure.description("This test creates a new user and checks if it is successfully")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.description("This test tries to create a new user using existing email")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", \
            f"Unexpected response content '{response.content}'"

    @allure.description("This test creates a new user using wrong email without @")
    def test_create_user_with_wrong_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format", f"Unexpected response content '{response.content}'"

    @allure.description("This test tries to create a user w/o one of required fields")
    @pytest.mark.parametrize('condition', exclude_params)
    def test_user_registration_without_parameter(self, condition):
        data = self.prepare_registration_data()

        del data[condition]

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {condition}", \
            f"Unexpected response content '{response.content}'"

    @allure.description("This test creates a user with short (one character) first or last name")
    @pytest.mark.parametrize('name', names)
    def test_create_user_with_short_name(self, name):
        data = self.prepare_registration_data()
        data[name] = 'A'

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode("utf-8") == f"The value of '{name}' field is too short", \
            f"Unexpected response content '{response.content}'"

    @allure.description("This test creates a user with long (more than 250 chars) first or last name")
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