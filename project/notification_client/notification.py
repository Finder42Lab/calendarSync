from httpx import Client


class NotificationClient:
    def __init__(self, host: str, token: str):
        self.host = host
        self.token = token

        self._client = Client(base_url=self.host, headers={"Authorization": token})

    def send_notification(self, text: str):
        self._client.post(
            '/',
            json={
                'text': text,
            }
        )


