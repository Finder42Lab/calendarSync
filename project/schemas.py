import datetime

from caldav.objects import Event
from pydantic import BaseModel, Field, AliasPath, ConfigDict, PrivateAttr
from pydantic.alias_generators import to_camel


def alias_generator(field_name: str) -> str:
    cameled = to_camel(field_name)

    return cameled[0].upper() + cameled[1:]


class OutlookCalendarEvent(BaseModel):
    id: str = Field(validation_alias=AliasPath("ItemId", "Id"))

    title: str = Field(validation_alias="Subject")
    description: str = Field(validation_alias="Preview")
    location: str = Field(validation_alias=AliasPath("Location", "DisplayName"))

    sensitivity: str
    importance: str

    start: datetime.datetime
    end: datetime.datetime

    modified: datetime.datetime = Field(validation_alias="LastModifiedTime")
    created: datetime.datetime = Field(validation_alias="DateTimeCreated")

    is_all_day_event: bool
    is_meeting: bool
    is_cancelled: bool

    author_name: str = Field(validation_alias=AliasPath("Organizer", "Mailbox", "Name"))

    model_config = ConfigDict(alias_generator=alias_generator)


class CalDavEvent(BaseModel):
    uid: str = Field(validation_alias=AliasPath("uid", "value"))
    description: str = Field(
        validation_alias=AliasPath("description", "value"),
        default="",
    )
    summary: str = Field(validation_alias=AliasPath("summary", "value"), default="")
    location: str = Field(validation_alias=AliasPath("location", "value"), default="")

    start: datetime.datetime = Field(
        validation_alias=AliasPath("dtstart", "value"),
        default="",
    )
    end: datetime.datetime = Field(
        validation_alias=AliasPath("dtend", "value"),
        default="",
    )

    created: datetime.datetime = Field(
        validation_alias=AliasPath("created", "value"),
        default="",
    )
    modified: datetime.datetime = Field(
        validation_alias=AliasPath("last-modified", "value"),
    )

    _instance: Event | None = PrivateAttr()

    model_config = ConfigDict(from_attributes=True)
