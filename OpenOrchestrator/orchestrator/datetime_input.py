
from datetime import datetime
from typing import Callable

from nicegui import ui


# pylint: disable-next=too-few-public-methods
class DatetimeInput():
    """A datetime input with a button to show a date and time picker dialog."""
    def __init__(self, label: str) -> None:
        date_str = datetime.now().strftime("%d-%m-%Y %H:%M")

        # Define dialog
        with ui.dialog() as self._dialog, ui.card():
            self._date_input = ui.date(value=date_str, mask="DD-MM-YYYY", on_change=self._save).props("today-btn first-day-of-week=1")
            self._time_input = ui.time(value=date_str[11:], mask="HH:mm", on_change=self._save).props("format24h")
            ui.button("Close", on_click=self._dialog.close)

        # Define input
        with ui.input(label, value=date_str, validation=self._validation()) as self._input:
            ui.button(icon="event", on_click=self._dialog.open).props("flat")

    def _save(self):
        """Save the selected date and time and close the dialog."""
        self._input.value = f"{self._date_input.value} {self._time_input.value}"

    def get_datetime(self) -> datetime | None:
        """Get the text from the input as a datetime object, if
        the current text in the input is valid else None.

        Returns:
            datetime: The value as a datetime object if valid.
        """
        try:
            return datetime.strptime(self._input.value,  "%d-%m-%Y %H:%M")
        except ValueError:
            return None

    def _validation(self) -> dict[str, Callable]:
        def validate(_):
            return self.get_datetime() is not None

        return {"Invalid date: DD-MM-YYYY HH:mm": validate}
