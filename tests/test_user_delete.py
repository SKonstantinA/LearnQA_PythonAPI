from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import time

class TestUserDelete(BaseCase):
    def test_delete_user_two(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.delete(
            f"/user/{user_id_from_auth_method}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_status_code(response2, 400)
        assert response2.json() == {'error': 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.'}, \
            f"Unexpected response content '{response2.content}'"

    def test_delete_just_created_user(self):
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        response2 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_status_code(response2, 200)
        assert response2.json() == {'success': '!'}, f"Unexpected response content '{response2.content}'"

        response3 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_status_code(response3, 404)
        assert response3.content.decode("utf-8") == "User not found", f"Unexpected response content '{response2.content}'"

    def test_delete_user_when_auth_as_another_user(self):
        # REGISTER USER 1
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")

        time.sleep(1)

        # REGISTER USER 2
        register_data = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_status_code(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        email2 = register_data['email']
        password2 = register_data['password']

        login_data = {
            'email': email2,
            'password': password2
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        response2 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        if response2.status_code == 200:
            response3= MyRequests.get(
                f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid}
            )

            # Check if User 1 still exists
            Assertions.assert_json_has_key(response3, 'username')
        else:
            Assertions.assert_status_code(response2, 400)
            assert response2.json() != {'success': '!'}, f"Unexpected response content '{response2.content}'"