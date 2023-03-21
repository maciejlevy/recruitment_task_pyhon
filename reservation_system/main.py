from reservation_system.reservation_manager import ReservationManager
from reservation_system.user_interface import UserInterface


def run() -> None:
    reservation_manager = ReservationManager()
    user_interface = UserInterface(reservation_manager)
    user_interface.main_menu()


if __name__ == "__main__":
    run()
