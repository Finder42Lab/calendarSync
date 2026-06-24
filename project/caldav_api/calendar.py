import datetime
from urllib.parse import urlsplit, urlunsplit

import caldav
import vobject
from requests.auth import HTTPBasicAuth

from caldav_api.schemas import CalDavEvent


class CalDavCalendar:
    def __init__(
        self, host: str, login: str, password: str, calendar_id: str | None = None
    ):
        self.client = caldav.DAVClient(
            url=self._discovery_url(host),
            auth=HTTPBasicAuth(login, password),
        )
        self.principal = self.client.principal()

        calendars = self.principal.calendars()

        if calendar_id is None:
            self.calendar = calendars[0]
        else:
            filtered_calendars = [
                cal for cal in calendars if str(cal.id) == calendar_id
            ]

            if not filtered_calendars:
                raise ValueError(f"No calendar found with id {calendar_id}")

            self.calendar = filtered_calendars[0]

    @staticmethod
    def _discovery_url(host: str) -> str:
        parsed = urlsplit(host)
        if parsed.path not in ("", "/"):
            return host

        return urlunsplit((parsed.scheme, parsed.netloc, "/dav/cal", parsed.query, ""))

    def events(
        self,
        period_start: datetime.datetime,
        period_end: datetime.datetime,
    ) -> list[CalDavEvent]:
        events = []

        for e in self._raw_events(period_start, period_end):
            event = CalDavEvent.model_validate(e.vobject_instance.vevent)
            event._instance = e
            events.append(event)

        return events

    def _raw_events(
        self,
        period_start: datetime.datetime,
        period_end: datetime.datetime,
    ):

        return self.calendar.date_search(start=period_start, end=period_end)

    def create_event(
        self,
        uid: str,
        summary: str,
        description: str,
        location: str,
        start: datetime.datetime,
        end: datetime.datetime,
    ):
        vcal = vobject.iCalendar()
        vevent = vcal.add("vevent")

        vevent.add("uid").value = uid
        vevent.add("summary").value = summary
        vevent.add("dtstart").value = start
        vevent.add("dtend").value = end
        vevent.add("description").value = description
        vevent.add("location").value = location

        ics_data = vcal.serialize()

        self.calendar.add_event(ics_data)
