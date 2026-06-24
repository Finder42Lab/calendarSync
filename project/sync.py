import sys

import datetime
import pytz
from caldav.objects import Event
from loguru import logger

from caldav_api import CalDavCalendar
from config import config
from outlook import OutlookCalendar, OutlookLogin


logger.remove()
logger.add(
    sys.stdout,
    format="[SYNC] {time:DD-MM-YYYY HH:mm:ss} | {level} | {message}",
    colorize=True,
)


@logger.catch
def sync():
    logger.info("Я проснулся")

    outlook_login = OutlookLogin(
        host=config.OUTLOOK_HOST,
        login=config.OUTLOOK_LOGIN,
        password=config.OUTLOOK_PASSWORD,
        ssl_verify=config.OUTLOOK_SSL_VERIFY,
    )

    outlook_client = outlook_login.get_client()

    outlook_calendar = OutlookCalendar(outlook_client)

    calendar = CalDavCalendar(
        host=config.CALDAV_HOST,
        login=config.CALDAV_LOGIN,
        password=config.CALDAV_PASSWORD,
        calendar_id=config.CALDAV_CALENDAR_ID,
    )

    period_start = datetime.datetime.now().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    period_end = period_start + datetime.timedelta(days=14)

    caldav_events_map = {e.uid: e for e in calendar.events(period_start, period_end)}

    tz = pytz.timezone(config.TZ)

    for outlook_event in outlook_calendar.get_events():
        if outlook_event.id not in caldav_events_map and not outlook_event.is_cancelled:
            logger.info(
                f"Создаю новое событие ({outlook_event.start}-{outlook_event.end})"
                f"{outlook_event.title} - {outlook_event.description}",
            )
            calendar.create_event(
                uid=outlook_event.id,
                summary=outlook_event.title,
                description=outlook_event.description,
                location=outlook_event.location,
                start=outlook_event.start.astimezone(tz),
                end=outlook_event.end.astimezone(tz),
            )
            continue

        caldav_event = caldav_events_map.get(outlook_event.id)

        if outlook_event.is_cancelled and caldav_event:
            logger.info(f"Удаляю отмененное событие {outlook_event.title}")
            caldav_event._instance.delete()
            continue

        if not caldav_event:
            continue

        if (
            outlook_event.title != caldav_event.summary
            or outlook_event.start != caldav_event.start
            or outlook_event.end != caldav_event.end
            or outlook_event.location != caldav_event.location
        ) and caldav_event._instance is not None:
            logger.info(
                f"Обновляю событие ({outlook_event.start}-{outlook_event.end})"
                f"{outlook_event.title} - {outlook_event.description}",
            )
            event: Event = caldav_event._instance
            vevent = event.vobject_instance.vevent

            vevent.summary.value = outlook_event.title
            vevent.add("location").value = outlook_event.location
            try:
                if hasattr(vevent, "description"):
                    vevent.description.value = outlook_event.description
                else:
                    vevent.add("description").value = outlook_event.description
            except AttributeError as e:
                logger.error(f"Ошибка обновления описания: {e}")

            vevent.dtstart.value = outlook_event.start.astimezone(tz)
            vevent.dtend.value = outlook_event.end.astimezone(tz)

            event.vobject_instance.serialize()

            event.save()

    logger.info("Закончил работу")


if __name__ == "__main__":
    sync()
