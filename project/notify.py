import sys

import datetime
from loguru import logger

from caldav_api import CalDavCalendar, CalDavEvent
from config import config
from notification_client.notification import NotificationClient


logger.remove()
logger.add(
    sys.stdout,
    format="[NOTIFY] {time:DD-MM-YYYY HH:mm:ss} | {level} | {message}",
    colorize=True,
)

def format_event(event: CalDavEvent):
    start_formatted = event.start.strftime('%H:%M')
    end_formatted = event.end.strftime('%H:%m')

    txt = f'📢 *{event.summary} ({start_formatted} - {end_formatted})*'

    if event.description:
        txt += f'\n✉{event.description}'

    if event.location:
        txt += f'\n☎{event.location}'

    return txt


def get_today_events(calendar: CalDavCalendar):
    period_start = datetime.datetime.today().replace(second=0, microsecond=0, minute=0, hour=0)
    period_end = period_start + datetime.timedelta(days=1)

    return calendar.events(period_start, period_end)



def format_events(events: list[CalDavEvent], header: str):
    txt = f'**{header}** \n'

    for event in events:
        txt += format_event(event)
        txt += '\n\n'

    return txt


def get_hourly_events(events: list[CalDavEvent]):
    max_dt = datetime.datetime.now().replace(second=0, microsecond=0) + datetime.timedelta(hours=1)

    return [e for e in events if e.start == max_dt]


def get_now_events(events: list[CalDavEvent]):
    max_dt = datetime.datetime.now().replace(second=0, microsecond=0) + datetime.timedelta(minutes=3)

    return [e for e in events if e.start == max_dt]


def notify():
    calendar = CalDavCalendar(
        host=config.CALDAV_HOST,
        login=config.CALDAV_LOGIN,
        password=config.CALDAV_PASSWORD,
        calendar_id=config.CALDAV_CALENDAR_ID,
    )

    notificator = NotificationClient(
        host=config.NOTIFICATION_URL,
        token=config.NOTIFICATION_TOKEN,
    )
    logger.info('Получаю события, которые на сегодня')
    events = get_today_events(calendar)

    logger.info(f'Событий: {len(events)}')

    logger.info('Получаю события, которые будут сейчас')

    now_events = get_now_events(events)
    logger.info(f'Событий: {len(now_events)}')

    if now_events:
        notificator.send_notification(format_events(now_events, '🚨 Конференции уже сейчас:'))

    logger.info('Получаю события, которые будут через час')
    hourly_events = get_hourly_events(events)

    logger.info(f'Событий: {len(hourly_events)}')

    if hourly_events:
        notificator.send_notification(format_events(events, '🔔 Конференции через час'))


if __name__ == '__main__':
    notify()
