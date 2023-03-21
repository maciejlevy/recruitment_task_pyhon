from datetime import datetime

from reservation_system.configuration import DATETIME_FORMAT


class Reservation:
    def __init__(
        self, full_name: str, start_date: datetime, end_date: datetime
    ) -> None:
        self.full_name = full_name
        self.start_date = start_date
        self.end_date = end_date

    def __str__(self) -> str:
        return (
            f"* {self.full_name} "
            f"{self.start_date.strftime(DATETIME_FORMAT)} - "
            f"{self.end_date.strftime(DATETIME_FORMAT)} "
        )
