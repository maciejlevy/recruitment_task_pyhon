from datetime import timedelta, datetime
from typing import Optional, Union

from reservation_system.configuration import COURT_CLOSE, TIME_FORMAT, COURT_OPEN
from reservation_system.const import FileType
from reservation_system.errors import (
    SlotUnavailable,
    LessThanHour,
    CourtIsClosed,
    ReservationNoExist,
    TooManyReservations,
)
from reservation_system.reservation import Reservation
from reservation_system.reservation_csv_serializer import ReservationCSVSerializer
from reservation_system.reservation_json_serializer import ReservationJSONSerializer

Serializer = Union[ReservationCSVSerializer, ReservationJSONSerializer]


class ReservationManager:
    def __init__(self) -> None:
        self.reservations: list[Reservation] = []

    def make_a_reservation(
        self, full_name: str, start_date: datetime, duration: int
    ) -> None:
        end_date = start_date + timedelta(minutes=duration)
        current_time = datetime.today()
        open_time = datetime.strptime(COURT_OPEN, TIME_FORMAT).time()
        closed_time = datetime.strptime(COURT_CLOSE, TIME_FORMAT).time()

        present_day_weekday = datetime.today().weekday()
        monday = datetime.today() - timedelta(days=present_day_weekday)
        sunday = monday + timedelta(days=6)
        reservation_in_current_week = self.find_reservation_in_range(monday, sunday)

        how_many_reservations = 0
        for reservation in reservation_in_current_week:
            if reservation.full_name == full_name:
                how_many_reservations += 1
        court_available = self.is_court_available(start_date, end_date)
        if start_date.time() < open_time or end_date.time() > closed_time:
            raise CourtIsClosed()
        if start_date + timedelta(hours=1) <= current_time:
            raise LessThanHour()
        if how_many_reservations >= 2:
            raise TooManyReservations()
        if court_available is False:
            raise SlotUnavailable()
        reservation = Reservation(full_name, start_date, end_date)
        self.reservations.append(reservation)

    def delete_a_reservation(self, full_name: str, start_date: datetime) -> None:
        required_cancellation_time = datetime.today() + timedelta(hours=1)
        existing_reservation = self.find_client_reservation(full_name, start_date)
        if existing_reservation is None:
            raise ReservationNoExist()
        if required_cancellation_time > start_date:
            raise LessThanHour()
        self.reservations.remove(existing_reservation)

    def find_reservation(self, start_date: datetime) -> Optional[Reservation]:
        for reservation in self.reservations:
            if reservation.start_date == start_date:
                return reservation
        return None

    def find_client_reservation(
        self, full_name: str, start_date: datetime
    ) -> Optional[Reservation]:
        for reservation in self.reservations:
            if (
                reservation.full_name == full_name
                and reservation.start_date == start_date
            ):
                return reservation
        return None

    def is_court_available(self, start_date: datetime, end_date: datetime) -> bool:
        for reservation in self.reservations:
            if reservation.start_date < end_date and reservation.end_date > start_date:
                return False
        return True

    def find_reservation_in_range(
        self, start_date: datetime, end_date: datetime
    ) -> list[Reservation]:
        reservations_in_range = [
            reservation
            for reservation in self.reservations
            if reservation.start_date < end_date and reservation.end_date > start_date
        ]
        return reservations_in_range

    def find_nearest_available_slot(
        self, start_date: datetime, duration: int
    ) -> datetime:
        end_date = start_date + timedelta(minutes=duration)
        while True:
            list_of_reservation = self.find_reservation_in_range(start_date, end_date)
            if not list_of_reservation:
                return start_date
            list_of_reservation.sort(key=lambda reservation: reservation.start_date)
            last_reservation = list_of_reservation[-1]
            start_date = last_reservation.end_date
            end_date = start_date + timedelta(minutes=duration)

    @staticmethod
    def longest_slot_minutes_for_start_date(start_date: datetime) -> int:
        court_closing_datetime = datetime.strptime(COURT_CLOSE, TIME_FORMAT)
        start_datetime = court_closing_datetime.replace(
            hour=start_date.hour, minute=start_date.minute
        )
        available_slot = court_closing_datetime - start_datetime
        if available_slot.total_seconds() > 0:
            return int(available_slot.total_seconds() / 60)
        return 0

    def save_reservations_from_range(
        self,
        start_date: datetime,
        end_date: datetime,
        name_of_file: str,
        file_type: str,
    ) -> None:
        reservations_to_save = self.find_reservation_in_range(start_date, end_date)

        serializer: Serializer
        if file_type.upper() == FileType.JSON:
            serializer = ReservationJSONSerializer(file_name=name_of_file)
        elif file_type.upper() == FileType.CSV:
            serializer = ReservationCSVSerializer(file_name=name_of_file)
        else:
            raise ValueError(f"{file_type} is not supported.")
        serializer.save_reservations(reservations_to_save)

    def load_reservations_from_file(self, name_of_file: str, file_type: str) -> None:
        serializer: Serializer
        if file_type.upper() == FileType.JSON:
            serializer = ReservationJSONSerializer(file_name=name_of_file)
        elif file_type.upper() == FileType.CSV:
            serializer = ReservationCSVSerializer(file_name=name_of_file)
        else:
            raise ValueError(f"{file_type} is not supported.")
        self.reservations = serializer.load_reservations()
