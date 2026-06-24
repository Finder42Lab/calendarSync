import datetime

from pydantic import AliasPath, BaseModel, ConfigDict, Field
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
