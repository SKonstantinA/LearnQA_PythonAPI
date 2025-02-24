from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import time


class TestUserEdit(BaseCase):
     def setup_method(self):
         # REGISTER
         register_data = self.prepare_registration_data()
         response1 = MyRequests.post("/user/", data=register_data)

         Assertions.assert_status_code(response1, 200)
         Assertions.assert_json_has_key(response1, "id")

         self.email = register_data['email']
         self.password = register_data['password']
         self.first_name = register_data['firstName']
         self.user_id = self.get_json_value(response1, "id")

     def test_edit_just_created_user(self):
         # LOGIN
         login_data = {
             'email': self.email,
             'password': self.password
         }
         response2 = MyRequests.post("/user/login", data=login_data)

         auth_sid = self.get_cookie(response2, "auth_sid")
         token = self.get_header(response2, "x-csrf-token")

         # EDIT
         new_name = "Changed Name"

         response3 = MyRequests.put(
             f"/user/{self.user_id}",
             headers={"x-csrf-token": token},
             cookies={"auth_sid": auth_sid},
             data={"firstName": new_name}
         )

         Assertions.assert_status_code(response3, 200)

         # GET
         response4 = MyRequests.get(
             f"/user/{self.user_id}",
             headers={"x-csrf-token": token},
             cookies={"auth_sid": auth_sid}
         )

         Assertions.assert_json_value_by_name(
             response4,
             "firstName",
             new_name,
             "Wrong name of the user after edit"
         )

     def test_edit_user_without_auth(self):
         # EDIT
         new_name = "Changed Name"

         response2 = MyRequests.put(
             f"/user/{self.user_id}",
             data={"firstName": new_name}
         )

         Assertions.assert_status_code(response2, 400)
         assert response2.json() == {"error":"Auth token not supplied"}, f"Unexpected response content '{response2.content}'"

     def test_edit_user_four_auth_as_another_user(self):
         # LOGIN
         login_data = {
             'email': self.email,
             'password': self.password
         }
         response2 = MyRequests.post("/user/login", data=login_data)

         auth_sid = self.get_cookie(response2, "auth_sid")
         token = self.get_header(response2, "x-csrf-token")

         # EDIT
         new_name = "Changed Name"

         response3 = MyRequests.put(
             f"/user/4",
             headers={"x-csrf-token": token},
             cookies={"auth_sid": auth_sid},
             data={"firstName": new_name}
         )

         Assertions.assert_status_code(response3, 400)
         assert response3.json() == {"error":"Please, do not edit test users with ID 1, 2, 3, 4 or 5."}, \
             f"Unexpected response content '{response2.content}'"

     def test_edit_another_user_auth_as_newly_created_user(self):
         print(f"User 1 ID: {self.user_id}")
         time.sleep(1)

         # REGISTER USER 2
         register_data = self.prepare_registration_data()
         response2 = MyRequests.post("/user/", data=register_data)

         Assertions.assert_status_code(response2, 200)
         Assertions.assert_json_has_key(response2, "id")

         email2 = register_data['email']
         password2 = register_data['password']
         user_id2 = self.get_json_value(response2, "id")

         assert self.user_id != user_id2, " User 1 has the same ID as User 2"
         print(f"User 2 ID: {user_id2}")

         # LOGIN AS USER 2
         login_data = {
             'email': email2,
             'password': password2
         }
         response3 = MyRequests.post("/user/login", data=login_data)

         auth_sid2 = self.get_cookie(response3, "auth_sid")
         token2 = self.get_header(response3, "x-csrf-token")

         # EDIT
         new_name = "Changed Name"

         response4 = MyRequests.put(
             f"/user/{self.user_id}",
             headers={"x-csrf-token": token2},
             cookies={"auth_sid": auth_sid2},
             data={"firstName": new_name}
         )
         print(f"response4: {response4.json()}")

         if response4.status_code == 200:
         # LOGIN AS USER 1
             login_data = {
                 'email': self.email,
                 'password': self.password
             }
             response5 = MyRequests.post("/user/login", data=login_data)

             auth_sid1 = self.get_cookie(response5, "auth_sid")
             token1 = self.get_header(response5, "x-csrf-token")

             # GET
             response6 = MyRequests.get(
                 f"/user/{self.user_id}",
                 headers={"x-csrf-token": token1},
                 cookies={"auth_sid": auth_sid1}
             )

             print(f"response6: {response6.json()}")

             Assertions.assert_json_value_by_name(
                 response6,
                 "firstName",
                 self.first_name,
                 "Changes was applied to User 1 when authorised as User 2"
             )
         else:
             print("Something else")

     def test_substitute_user_email_with_wrong_one(self):
         # LOGIN
         login_data = {
             'email': self.email,
             'password': self.password
         }
         response2 = MyRequests.post("/user/login", data=login_data)

         auth_sid = self.get_cookie(response2, "auth_sid")
         token = self.get_header(response2, "x-csrf-token")

         # EDIT
         new_email = "vinkotovexample.com"

         response3 = MyRequests.put(
             f"/user/{self.user_id}",
             headers={"x-csrf-token": token},
             cookies={"auth_sid": auth_sid},
             data={"email": new_email}
         )

         Assertions.assert_status_code(response3, 400)
         assert response3.json() == {'error': 'Invalid email format'}, \
             f"Unexpected response content '{response3.content}'"

     def test_change_just_created_user_name_to_short(self):
         # LOGIN
         login_data = {
             'email': self.email,
             'password': self.password
         }
         response2 = MyRequests.post("/user/login", data=login_data)

         auth_sid = self.get_cookie(response2, "auth_sid")
         token = self.get_header(response2, "x-csrf-token")

         # EDIT
         new_name = "a"

         response3 = MyRequests.put(
             f"/user/{self.user_id}",
             headers={"x-csrf-token": token},
             cookies={"auth_sid": auth_sid},
             data={"firstName": new_name}
         )

         Assertions.assert_status_code(response3, 400)
         assert response3.json() == {'error': 'The value for field `firstName` is too short'}, \
             f"Unexpected response content '{response3.content}'"