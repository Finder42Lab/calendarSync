import datetime

from caldav.objects import Event
from pydantic import AliasPath, BaseModel, ConfigDict, Field, PrivateAttr


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

    created: datetime.datetime | None = Field(
        validation_alias=AliasPath("created", "value"),
        default=None,
    )
    modified: datetime.datetime | None = Field(
        validation_alias=AliasPath("last-modified", "value"),
        default=None,
    )

    _instance: Event | None = PrivateAttr()

    model_config = ConfigDict(from_attributes=True)
