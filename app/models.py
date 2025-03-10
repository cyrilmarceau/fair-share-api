from pydantic import BaseModel
from sqlmodel import Field
from datetime import datetime, timezone


class DispatchBase(BaseModel):
    class Config:
        orm_modefrom_attributes = True
        validate_assignment = True
        arbitrary_types_allowed = True
        str_strip_whitespace = True


class TimeStampMixin(object):
    """Timestamp mixin"""

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Creation time of the object ",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": datetime.now(timezone.utc)},
        description="Last updated time of the object (read-only)",
    )
