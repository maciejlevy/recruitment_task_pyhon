import json
from datetime import datetime

from reservation_system.configuration import DATETIME_FORMAT
from reservation_system.reservation import Reservation


class ReservationJSONSerializer:
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name

    def save_reservations(self, reservations: list[Reservation]) -> None:
        reservations_data = {
            "reservations": [
                {
                    "name": reservation.full_name,
                    "start_time": reservation.start_date.strftime(DATETIME_FORMAT),
                    "end_time": reservation.end_date.strftime(DATETIME_FORMAT),
                }
                for reservation in reservations
            ]
        }
        with open(self.file_name, mode="w", encoding="utf8") as reservations_file:
            json.dump(
                reservations_data, reservations_file, ensure_ascii=False, indent=3
            )

    def load_reservations(self) -> list[Reservation]:
        with open(self.file_name, mode="r") as reservations_file:
            reservations_data = json.load(reservations_file).get("reservations", [])
            reservations = [
                Reservation(
                    full_name=row["name"],
                    start_date=datetime.strptime(row["start_time"], DATETIME_FORMAT),
                    end_date=datetime.strptime(row["end_time"], DATETIME_FORMAT),
                )
                for row in reservations_data
            ]
            return reservations
