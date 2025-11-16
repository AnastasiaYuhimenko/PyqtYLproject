import os
import sys

from pyqtfront.front.chat_page import ChatWindow

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox
from sqlalchemy.orm import Session

from app.schemas.users import UserGet
from app.services.user_service import UserService


class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self, session: Session):
        super().__init__()
        self.session = session

        ui_path = os.path.join(os.path.dirname(__file__), "../ui/login.ui")
        uic.loadUi(ui_path, self)

        self.username_input = self.textEdit
        self.password_input = self.textEdit_2
        self.pushButton.setText("Войти")
        self.pushButton.clicked.connect(self.handle_login)

    def handle_login(self):
        username = self.username_input.toPlainText().strip()
        password = self.password_input.toPlainText().strip()

        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль")
            return

        user_login = UserGet(username=username, password=password)
        user, success = UserService.login(self.session, user_login)
        if not success:
            QMessageBox.warning(self, "Ошибка", "Неправильный логин или пароль")
            return

        QMessageBox.information(self, "Успех", "Вы вошли в аккаунт")
        self.username_input.clear()
        self.password_input.clear()

        self.hide()
        self.win = ChatWindow(self.session, user)
        self.win.show()
        self.win.show()
        self.username_input.clear()
        self.password_input.clear()
