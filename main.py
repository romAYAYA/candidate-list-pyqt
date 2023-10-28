import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QListWidget, \
    QDialog, QTextEdit
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Candidate:
    def __init__(self, first_name: str, last_name: str, email: str, phone: int):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone


class CandidateDatabase:
    def __init__(self):
        self.conn = sqlite3.connect("candidates.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS candidates (first_name TEXT, last_name TEXT, email TEXT, phone TEXT)")
        self.conn.commit()

    def add_candidate(self, candidate):
        self.cursor.execute("INSERT INTO candidates VALUES (?, ?, ?, ?)",
                            (candidate.first_name, candidate.last_name, candidate.email, candidate.phone))
        self.conn.commit()

    def get_candidates(self):
        self.cursor.execute('SELECT * FROM candidates')
        candidates = self.cursor.fetchall()
        return candidates


class CandidateManagerUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Candidate List Manager")
        self.setGeometry(100, 100, 400, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.first_name_input = QLineEdit(self)
        self.last_name_input = QLineEdit(self)
        self.email_input = QLineEdit(self)
        self.phone_input = QLineEdit(self)

        self.add_button = QPushButton("Add Candidate", self)
        self.add_button.clicked.connect(self.add_candidate)
        self.send_email_button = QPushButton("Send Email to All", self)
        self.send_email_button.clicked.connect(self.open_send_email_dialog)

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

        self.layout.addWidget(self.send_email_button)
        self.central_widget.setLayout(self.layout)

        self.db = CandidateDatabase()
        self.display_candidates()

    def add_candidate(self):
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        email = self.email_input.text()
        phone = self.phone_input.text()

        candidate = Candidate(first_name, last_name, email, phone)

        self.db.add_candidate(candidate)

        self.first_name_input.clear()
        self.last_name_input.clear()
        self.email_input.clear()
        self.phone_input.clear()

        self.display_candidates()

    def display_candidates(self):
        self.candidate_list.clear()
        candidates = self.db.get_candidates()

        for candidate in candidates:
            self.candidate_list.addItem(f"{candidate[0]} {candidate[1]} ({candidate[2]}) - {candidate[3]}")

    def open_send_email_dialog(self):
        dialog = SendEmailDialog()
        dialog.exec()


class SendEmailDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Send Email to All Candidates")
        self.setGeometry(200, 200, 400, 200)

        self.layout = QVBoxLayout()

        self.email_text = QTextEdit(self)
        self.email_text.setPlaceholderText("Enter your email text here")

        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(self.send_email)

        self.layout.addWidget(self.email_text)
        self.layout.addWidget(self.send_button)

        self.setLayout(self.layout)

    def send_email(self):
        email_text = self.email_text.toPlainText()

        db = CandidateDatabase()
        candidates = db.get_candidates()

        for candidate in candidates:
            email = candidate[2]
            self.send_individual_email(email, email_text)

        self.accept()

    def send_individual_email(self, to_email, email_text):
        try:
            msg = MIMEMultipart()
            msg['From'] = 'testemailsenderpy366@gmail.com'
            msg['Subject'] = 'Your Subject Here'
            msg['To'] = to_email

            msg.attach(MIMEText(email_text, 'plain'))

            smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp_server.login('testemailsenderpy366@gmail.com',
                              'ioqw rtxi vudc qtda')

            smtp_server.sendmail('testemailsenderpy366@gmail.com', to_email, msg.as_string())

            smtp_server.quit()
            print(f"Email sent successfully to {to_email}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")


def main():
    app = QApplication(sys.argv)
    window = CandidateManagerUI()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
