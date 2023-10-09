import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QListWidget


class Candidate:
    def __init__(self, first_name: str, last_name: str, email: str, phone: int):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone


class CandidateManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Candidate List Manager")
        self.setGeometry(100, 100, 400, 400)

        self.conn = sqlite3.connect("candidates.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS candidates (first_name TEXT, last_name TEXT, email TEXT, phone TEXT)")
        self.conn.commit()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.first_name_input = QLineEdit(self)
        self.last_name_input = QLineEdit(self)
        self.email_input = QLineEdit(self)
        self.phone_input = QLineEdit(self)

        self.add_button = QPushButton("Add Candidate", self)
        self.add_button.clicked.connect(self.add_candidate)

        self.candidate_list = QListWidget(self)

        self.layout.addWidget(self.first_name_input)
        self.first_name_input.setPlaceholderText("First Name")

        self.layout.addWidget(self.last_name_input)
        self.last_name_input.setPlaceholderText("Last Name")

        self.layout.addWidget(self.email_input)
        self.email_input.setPlaceholderText("Email")

        self.layout.addWidget(self.phone_input)
        self.phone_input.setPlaceholderText("Phone Number")

        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.candidate_list)

        self.central_widget.setLayout(self.layout)

    def add_candidate(self):
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        email = self.email_input.text()
        phone = self.phone_input.text()

        candidate = Candidate(first_name, last_name, email, phone)

        self.cursor.execute("INSERT INTO candidates VALUES (?, ?, ?, ?)",
                            (candidate.first_name, candidate.last_name, candidate.email, candidate.phone))

        self.conn.commit()

        self.first_name_input.clear()
        self.last_name_input.clear()
        self.email_input.clear()
        self.phone_input.clear()

        self.display_candidates()

    def display_candidates(self):
        self.candidate_list.clear()

        self.cursor.execute('SELECT * FROM candidates')
        candidates = self.cursor.fetchall()

        for candidate in candidates:
            self.candidate_list.addItem(f"{candidate[0]} {candidate[1]} ({candidate[2]}) - {candidate[3]}")


def main():
    app = QApplication(sys.argv)
    window = CandidateManager()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
