import csv
from datetime import datetime
from reservation_system.configuration import DATETIME_FORMAT
from reservation_system.reservation import Reservation


class ReservationCSVSerializer:
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name

    def save_reservations(self, reservations: list[Reservation]) -> None:
        with open(self.file_name, mode="w", newline="") as reservations_file:
            headers = ["name", "start_time", "end_time"]
            writer = csv.DictWriter(reservations_file, fieldnames=headers)
            writer.writeheader()
            for reservation in reservations:
                start_date = reservation.start_date
                writer.writerow(
                    {
                        "name": reservation.full_name,
                        "start_time": start_date.strftime(DATETIME_FORMAT),
                        "end_time": reservation.end_date.strftime(DATETIME_FORMAT),
                    }
                )

    def load_reservations(self) -> list[Reservation]:
        with open(self.file_name, newline="") as reservations_file:
            csv_reader = csv.DictReader(reservations_file)
            reservations = [
                Reservation(
                    full_name=row["name"],
                    start_date=datetime.strptime(row["start_time"], DATETIME_FORMAT),
                    end_date=datetime.strptime(row["end_time"], DATETIME_FORMAT),
                )
                for row in csv_reader
            ]
            return reservations
