from manager.main_window_manager import MainWindowManager
from PySide6.QtWidgets import QApplication
import sys


def main() -> None:
    """
    Main method to run the application.

    Returns:
    :return: None
    """
    app = QApplication(sys.argv)
    manager = MainWindowManager()
    manager.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
