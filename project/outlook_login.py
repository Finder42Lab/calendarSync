import datetime

from httpx import Client


class OutlookLogin:
    def __init__(self, host: str, login: str, password: str):
        self.host = host
        self.login = login
        self.password = password

        self.client = Client(
            base_url=self.host,
            headers={
                "accept-encoding": "gzip, deflate, br, zstd",
                "accept-language": "ru,en;q=0.9",
                "origin": host,
                "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "YaBrowser";v="25.2", "Yowser";v="2.5"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "Linux",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 YaBrowser/25.2.0.0 Safari/537.36",
                "x-owa-attempt": "1",
                "x-owa-clientbegin": (
                    datetime.datetime.now() - datetime.timedelta(hours=3)
                ).isoformat(),
                "x-owa-clientbuildversion": "15.2.1544.27",
                "x-requested-with": "XMLHttpRequest",
            },
        )

    def _send_form_data(self):
        form_data = {
            "destination": f"{self.host}/owa/",
            "flags": "4",
            "forcedownlevel": "0",
            "username": self.login,
            "password": self.password,
            "passwordText": "",
            "isUtf8": "1",
        }

        response = self.client.post(
            "/owa/auth.owa",
            data=form_data,
        )

        if response.status_code != 302:
            raise ConnectionError(response.text)

    def _process_login(self):
        response = self.client.get("/owa/")

        if response.status_code != 200:
            raise ConnectionError(response.text)

    def _check_session_data(self):
        response = self.client.post(
            "/owa/sessiondata.ashx",
            params={"appcacheclient": 0},
        )

        if response.status_code != 200:
            raise ConnectionError(response.text)

    def get_client(self):
        self._send_form_data()
        self._process_login()
        self._check_session_data()

        return self.client
