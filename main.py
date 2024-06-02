from manager import Manager
from PySide6.QtWidgets import QApplication
import sys


def main():
    app = QApplication(sys.argv)
    manager = Manager()
    manager.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
