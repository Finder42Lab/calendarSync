import sys

import datetime
import logging
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


def format_events(events: list[CalDavEvent], header: str):
    txt = f'**{header}** \n'

    for event in events:
        txt += format_event(event)
        txt += '\n\n'

    return txt


def get_hourly_events(calendar: CalDavCalendar):
    period_start = datetime.datetime.now().replace(minute=0, second=0, microsecond=0) + datetime.timedelta(hours=1)
    period_end = period_start + datetime.timedelta(minutes=1)

    logging.info(f'{period_start} - {period_end}')


    events = calendar.events(period_start, period_end)

    return events


def get_now_events(calendar: CalDavCalendar):
    period_start = datetime.datetime.now().replace(minute=0, second=0, microsecond=0) + datetime.timedelta(minutes=2)
    period_end = period_start + datetime.timedelta(minutes=1)

    logging.info(f'{period_start} - {period_end}')

    events = calendar.events(period_start, period_end)

    return events


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

    logger.info('Получаю события, которые будут сейчас')

    now_events = get_now_events(calendar)
    logger.info(f'Событий: {len(now_events)}')

    if now_events:
        notificator.send_notification(format_events(now_events, '🚨 Конференции уже сейчас:'))

    logger.info('Получаю события, которые будут через час')
    events = get_hourly_events(calendar)

    logger.info(f'Событий: {len(events)}')

    if events:
        notificator.send_notification(format_events(events, '🔔 Конференции через час'))


if __name__ == '__main__':
    notify()
