import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from login import LoginWindow
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox
from sqlalchemy.orm import Session, sessionmaker
from sqlmodel import create_engine

from app.schemas.users import UserCreate
from app.services.user_service import UserService


class RegisterWindow(QtWidgets.QMainWindow):
    def __init__(self, session: Session):
        super().__init__()
        self.session = session

        ui_path = os.path.join(os.path.dirname(__file__), "../ui/register.ui")
        uic.loadUi(ui_path, self)

        self.username_input = self.textEdit
        self.password_input = self.textEdit_2
        self.pushButton.clicked.connect(self.handle_register)
        self.login_redirect_btn = self.pushButton_2
        self.login_redirect_btn.clicked.connect(self.redirect_to_login)

    def handle_register(self):
        username = self.username_input.toPlainText().strip()
        password = self.password_input.toPlainText().strip()

        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль")
            return

        user_add = UserCreate(username=username, password=password)
        user, success = UserService.register(self.session, user_add)
        if not success:
            QMessageBox.information(
                self,
                "Не успех",
                f"Пользователь с таким логином уже существует",
            )
        QMessageBox.information(self, "Успех", f"Пользователь создан")
        self.hide()
        self.login_window = LoginWindow(self.session)
        self.login_window.show()
        self.username_input.clear()
        self.password_input.clear()

    def redirect_to_login(self):
        self.hide()
        self.login_window = LoginWindow(self.session)
        self.login_window.show()


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DB_PATH = os.path.join(BASE_DIR, "../messenger.db")

    engine = create_engine(f"sqlite:///{DB_PATH}", echo=True)

    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    app = QtWidgets.QApplication(sys.argv)
    win = RegisterWindow(session)
    win.show()
    sys.exit(app.exec())
