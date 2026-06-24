import datetime

from caldav_api import CalDavCalendar
from config import config

calendar = CalDavCalendar(
        host=config.CALDAV_HOST,
        login=config.CALDAV_LOGIN,
        password=config.CALDAV_PASSWORD,
        calendar_id=config.CALDAV_CALENDAR_ID,
    )

period_start = datetime.datetime(2026, 6, 24, 0, 0, 0, 0)
period_end = period_start + datetime.timedelta(days=1)

events = calendar.events(period_start, period_end)

print(period_start, period_end)
print(events)