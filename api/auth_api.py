import json


class AuthAPI:

    def __init__(self, context):

        self.context = context

    def login(self, login_url, username, password):

        response = self.context.request.post(
            login_url,
            data=json.dumps({
                "email": username,
                "password": password
            }),
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )

        return response