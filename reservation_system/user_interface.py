import calendar

from reservation_system.reservation_manager import ReservationManager
from reservation_system.configuration import (
    DATETIME_FORMAT,
    MAX_SESSION_DURATION,
    MIN_SESSION_DURATION,
    DATE_FORMAT,
)
from reservation_system.const import UserChoice, YesNoUserChoice
from reservation_system.errors import (
    SlotUnavailable,
    LessThanHour,
    ReservationNoExist,
    CourtIsClosed,
    TooManyReservations,
)
from reservation_system.reservation import Reservation
from datetime import datetime, timedelta


class UserInterface:
    def __init__(self, reservation_manager: ReservationManager) -> None:
        self.reservation_manager = reservation_manager

    def main_menu(self) -> None:
        while True:
            print("\nWELCOME IN TENNIS COURT RESERVATION SYSTEM")
            print("SYSTEM MENU:")
            print("1) MAKE A RESERVATION")
            print("2) CANCEL A RESERVATION")
            print("3) PRINT SCHEDULE")
            print("4) SAVE SCHEDULE TO FILE")
            print("5) EXIT")
            print("6) LOAD RESERVATIONS FROM FILE")
            user_choice = input("What do you want to do: ")
            if user_choice.upper() in UserChoice.EXIT:
                print("Thank you for your attention! Have a nice day!")
                break
            self.handle_user_choice(user_choice)

    def handle_user_choice(self, user_choice: str) -> None:
        if user_choice.upper() in UserChoice.MAKE_RESERVATIONS:
            return self.make_reservation()
        elif user_choice.upper() in UserChoice.CANCEL_A_RESERVATION:
            return self.cancel_reservation()
        elif user_choice.upper() in UserChoice.PRINT_SCHEDULE:
            return self.print_schedule()
        elif user_choice.upper() in UserChoice.SAVE_SCHEDULE_TO_FILE:
            return self.save_schedule_to_file()
        elif user_choice.upper() in UserChoice.LOAD_RESERVATIONS_FROM_FILE:
            return self.load_reservation_from_file()
        else:
            print(f"Unknown command {user_choice}. Try again")

    def make_reservation(self) -> None:
        name = input("What's your Name? ")
        continue_search = True
        while continue_search:
            date_from_user = self.load_date_from_user("When would you like to book")
            open_court_minutes = (
                self.reservation_manager.longest_slot_minutes_for_start_date(
                    date_from_user
                )
            )
            duration_slots = self.open_court_minutes_to_duration_slots(
                open_court_minutes
            )
            if not duration_slots:
                print("There is no available slot for reservation today.")
                continue
            duration_time = self.load_duration_from_user(duration_slots)
            try:
                self.reservation_manager.make_a_reservation(
                    name, date_from_user, duration_time
                )
                print(f"Your reservation has been done and added to schedule.")
                return
            except CourtIsClosed:
                print("Sorry Court is open from 8:00 to 18:00.")
            except LessThanHour:
                print(
                    "Sorry, you cannot make a reservation if there is less than an hour left before it starts."
                )
                return
            except TooManyReservations:
                print(
                    "Sorry, you cannot make a reservation because you have 2 active reservations per week."
                )
                return
            except SlotUnavailable:
                continue_search = self.search_for_alternative_slot(
                    name, date_from_user, duration_time
                )

    def search_for_alternative_slot(
        self, name: str, date_from_user: datetime, duration_time: int
    ) -> bool:
        possible_reservation = self.reservation_manager.find_nearest_available_slot(
            date_from_user, duration_time
        )
        while True:
            proposal_next_available_date = input(
                f"The time you chose is unavailable, would you like to make a "
                f"reservation for {possible_reservation} instead? YES/NO: "
            )
            if proposal_next_available_date in [
                YesNoUserChoice.YES,
                YesNoUserChoice.NO,
            ]:
                break
            print("Wrong answer, Please make sure you entered YES or NO: ")
        if proposal_next_available_date == YesNoUserChoice.NO:
            return True
        try:
            self.reservation_manager.make_a_reservation(
                name, possible_reservation, duration_time
            )
            print(f"Your reservation has been done and added to schedule.")
            return True
        except SlotUnavailable:
            print("Sorry but this time is not available.")
        return False

    def cancel_reservation(self) -> None:
        name = input("Please enter your full name: ")
        while True:
            date_input = self.load_date_from_user("Please enter your reservation date.")
            try:
                self.reservation_manager.delete_a_reservation(name, date_input)
                print("Your reservation has been deleted.")
                return
            except ReservationNoExist:
                print("Sorry but this reservation is not exists.")
                return
            except LessThanHour:
                print(
                    "Sorry, you cannot cancel a reservation if there is less than an hour left before it starts."
                )
                return

    def print_schedule(self) -> None:
        print("Time range you want to see")
        start_date = self.load_date_from_user("From date")
        end_date = self.load_date_from_user("To date")
        schedule = self.reservation_manager.find_reservation_in_range(
            start_date, end_date
        )
        self.show_user_reservations(schedule)

    def save_schedule_to_file(self) -> None:
        start_date = self.load_date_from_user("From date")
        end_date = self.load_date_from_user("To date")
        name_of_file = input(f"Enter the name of save file: ")
        type_of_file = input(f"Choose a file format: JSON or CSV: ")
        try:
            self.reservation_manager.save_reservations_from_range(
                start_date, end_date, name_of_file, type_of_file
            )
        except ValueError as error:
            print(error)
        else:
            print(f"The Schedule has been saved to {name_of_file} file")

    def load_reservation_from_file(self) -> None:
        name_of_file = input(f"Enter the name of file: ")
        type_of_file = input(f"Choose a file format: JSON or CSV: ")
        try:
            self.reservation_manager.load_reservations_from_file(
                name_of_file, type_of_file
            )
        except ValueError as error:
            print(error)
        except FileNotFoundError:
            print(f"The file {name_of_file} does not exist")
        else:
            print(f"Reservations have been loaded from {name_of_file} file")

    @staticmethod
    def load_date_from_user(message: str) -> datetime:
        while True:
            date_input = input(f"{message} DD.MM.YYYY HH:MM ")
            try:
                correct_date = datetime.strptime(date_input, DATETIME_FORMAT)
                return correct_date
            except ValueError:
                print(
                    "Wrong data format. Please make sure you entered correctly. Example: 07.03.2023 10:00 "
                )

    @staticmethod
    def load_duration_from_user(duration_slots: list[int]) -> int:
        while True:
            print("How long would you like to book court?")
            for index, duration_slot in enumerate(duration_slots):
                print(index + 1, f" - {duration_slot} minutes")

            duration_option_from_user = input("Enter your option: ")
            try:
                duration_option = int(duration_option_from_user)
            except ValueError:
                print("Wrong choice. Please make sure you entered correctly option.")
                continue
            slot_index = duration_option - 1
            if slot_index < 0 or slot_index >= len(duration_slots):
                print("Wrong choice. Please make sure you entered correctly option.")
                continue
            return duration_slots[slot_index]

    @staticmethod
    def open_court_minutes_to_duration_slots(open_court_minutes: int) -> list[int]:
        if open_court_minutes > MAX_SESSION_DURATION:
            open_court_minutes = MAX_SESSION_DURATION

        number_of_small_slots = int(open_court_minutes / MIN_SESSION_DURATION)

        return [
            index * MIN_SESSION_DURATION
            for index in range(1, number_of_small_slots + 1)
        ]

    @staticmethod
    def show_user_reservations(reservations: list[Reservation]) -> None:
        reservations.sort(key=lambda r: r.start_date)
        headers_day = None
        present_day = datetime.today()
        for reservation in reservations:
            if reservation.start_date.date() != headers_day:
                headers_day = reservation.start_date.date()
                if headers_day == present_day.date() - timedelta(days=1):
                    print("\nYesterday:")
                elif headers_day == present_day.date():
                    print("\nToday:")
                elif headers_day == present_day.date() + timedelta(days=1):
                    print("\nTomorrow:")
                else:
                    print(
                        f"\n{calendar.day_name[headers_day.weekday()]} {headers_day.strftime(DATE_FORMAT)}:"
                    )
            print(reservation)
