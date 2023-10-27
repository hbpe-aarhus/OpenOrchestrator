"""This module defines ORM classes for triggers."""

from datetime import datetime
import enum
from typing import Optional
import uuid

from sqlalchemy import String, ForeignKey, Engine
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column

# All classes in this module are effectively dataclasses without methods.
# pylint: disable=too-few-public-methods


class Status(enum.Enum):
    """An enum representing the status of trigger processes."""
    IDLE = "Idle"
    RUNNING = "Running"
    FAILED = "Failed"
    DONE = "Done"
    PAUSED = "Paused"


class Type(enum.Enum):
    """An enum representing the type of triggers."""
    SINGLE = "Single"
    SCHEDULED = "Scheduled"
    QUEUE = "Queue"


class Base(DeclarativeBase):
    """SqlAlchemy base class for all ORM classes in this module."""


class Trigger(Base):
    """A base class for all triggers in the ORM."""
    __tablename__ = "Triggers"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    trigger_name: Mapped[str] = mapped_column(String(100))
    process_name: Mapped[str] = mapped_column(String(100))
    last_run: Mapped[Optional[datetime]]
    process_path: Mapped[str] = mapped_column(String(250))
    process_args: Mapped[Optional[str]] = mapped_column(String(1000))
    process_status: Mapped[Status] = mapped_column(default=Status.IDLE)
    is_git_repo: Mapped[bool]
    blocking: Mapped[bool]
    type: Mapped[Type]

    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_abstract": True
    }

    def __repr__(self) -> str:
        return f"{self.trigger_name}: {self.type.value}"


class SingleTrigger(Trigger):
    """A class representing single trigger objects in the ORM."""
    __tablename__ = "Single_Triggers"

    id: Mapped[uuid.UUID] = mapped_column(ForeignKey("Triggers.id"), primary_key=True)
    next_run: Mapped[datetime]

    __mapper_args__ = {"polymorphic_identity": Type.SINGLE}


class ScheduledTrigger(Trigger):
    """A class representing scheduled trigger objects in the ORM."""
    __tablename__ = "Scheduled_Triggers"

    id: Mapped[uuid.UUID] = mapped_column(ForeignKey("Triggers.id"), primary_key=True)
    cron_expr: Mapped[str] = mapped_column(String(200))
    next_run: Mapped[datetime]

    __mapper_args__ = {"polymorphic_identity": Type.SCHEDULED}


class QueueTrigger(Trigger):
    """A class representing queue trigger objects in the ORM."""
    __tablename__ = "Queue_Triggers"

    id: Mapped[uuid.UUID] = mapped_column(ForeignKey("Triggers.id"), primary_key=True)
    queue_name: Mapped[str] = mapped_column(String(200))
    min_batch_size: Mapped[Optional[int]]
    max_batch_size: Mapped[Optional[int]]

    __mapper_args__ = {"polymorphic_identity": Type.QUEUE}


def create_tables(engine: Engine):
    """Create all SQL tables related to ORM classes in this module.

    Args:
        engine: The SqlAlchemy connection engine used to create the tables.
    """
    Base.metadata.create_all(engine)
