import datetime
import json
import random
import urllib.parse

from httpx import Client

from schemas import OutlookCalendarEvent


def get_calendar_view_post_data():
    range_start = datetime.datetime.now().replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    range_end = range_start + datetime.timedelta(days=14)

    return {
        "__type": "GetCalendarViewJsonRequest:#Exchange",
        "Header": {
            "__type": "JsonRequestHeaders:#Exchange",
            "RequestServerVersion": "V2017_08_18",
            "TimeZoneContext": {
                "__type": "TimeZoneContext:#Exchange",
                "TimeZoneDefinition": {
                    "__type": "TimeZoneDefinitionType:#Exchange",
                    "Id": "Russian Standard Time",
                },
            },
        },
        "Body": {
            "__type": "GetCalendarViewRequest:#Exchange",
            "CalendarId": {
                "__type": "TargetFolderId:#Exchange",
                "BaseFolderId": {
                    "__type": "FolderId:#Exchange",
                    "Id": "AQMkADM5NWY2NWExLWQ3ZTMtNDBiYy04MGNiLWM5NTE4ZDQ5YzVmMwAuAAADsLeRxfyN90uhD9pAjyEfZQEAKfk6gsLXMEy20OOavE31pAAAAgENAAAA",
                    "ChangeKey": "AgAAAA==",
                },
            },
            "RangeStart": range_start.isoformat()[:23],
            "RangeEnd": range_end.isoformat()[:23],
        },
    }


class OutlookCalendar:
    def __init__(self, client: Client):
        self.client = client

    def get_events(self) -> list[OutlookCalendarEvent]:
        action_id = random.randint(-100, -1)

        post_data = get_calendar_view_post_data()
        post_data_encoded = urllib.parse.quote(json.dumps(post_data))

        response = self.client.post(
            "/owa/service.svc",
            params={
                "action": "GetCalendarView",
                "EP": "1",
                "ID": action_id,
                "AC": "1",
            },
            headers={
                "action": "GetCalendarView",
                "x-owa-urlpostdata": post_data_encoded,
                "x-owa-actionid": str(action_id),
                "x-owa-actionname": "GetCalendarViewAction_Month",
                "x-owa-canary": self.client.cookies.get("X-OWA-CANARY"),
                "x-owa-correlationid": self.client.cookies.get("ClientId"),
                "client-request-id": self.client.cookies.get("ClientId"),
            },
        )

        if response.status_code != 200:
            raise ConnectionError(response.text)

        events = response.json()["Body"]["Items"]

        return [OutlookCalendarEvent.model_validate(event) for event in events]
