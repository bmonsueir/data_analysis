import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    # Create application instance
    app = QApplication(sys.argv)
    app.setApplicationName("Data Analyzer")

    # Load main window
    window = MainWindow()
    window.show()

    # Start the event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
