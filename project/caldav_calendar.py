import datetime

import caldav
import vobject

from schemas import CalDavEvent


class CalDavCalendar:
    def __init__(
        self, host: str, login: str, password: str, calendar_id: str | None = None
    ):
        self.client = caldav.DAVClient(url=host, username=login, password=password)
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

    def events(self) -> list[CalDavEvent]:
        events = []

        for e in self._raw_events():
            event = CalDavEvent.model_validate(e.vobject_instance.vevent)
            event._instance = e
            events.append(event)

        return events

    def _raw_events(self):
        range_start = datetime.datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        range_end = range_start + datetime.timedelta(days=14)

        return self.calendar.date_search(start=range_start, end=range_end)

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
        vevent = vcal.add('vevent')

        vevent.add('uid').value = uid
        vevent.add('summary').value = summary
        vevent.add('dtstart').value = start
        vevent.add('dtend').value = end
        vevent.add('description').value = description
        vevent.add('location').value = location

        ics_data = vcal.serialize()

        self.calendar.add_event(ics_data)