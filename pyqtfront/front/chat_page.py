import os

from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFileDialog, QInputDialog, QListWidgetItem, QMessageBox
from websocket_client import WebSocketClient

from app.repositories.authRepo import UserRepository
from app.repositories.chats import ChatRepository
from app.services.chats import ChatService
from app.utils.settings import load_setting, save_setting
from pyqtfront.front.unless import UselessWindow


class ChatWindow(QtWidgets.QMainWindow):
    def __init__(self, session, current_user):
        super().__init__()
        self.session = session
        self.current_user = current_user
        self.current_chat_user = None

        ui_path = os.path.join(os.path.dirname(__file__), "../ui/homepage.ui")
        uic.loadUi(ui_path, self)

        self.addChatButton = QtWidgets.QPushButton("Добавить чат", self)
        self.addChatButton.setGeometry(10, 520, 200, 30)
        self.addChatButton.clicked.connect(self.add_chat_dialog)

        self.listWidget.itemClicked.connect(self.select_chat)
        self.pushButton.clicked.connect(self.send_message)
        self.bgButton = QtWidgets.QPushButton("Фон чата", self)
        self.bgButton.setGeometry(10, 560, 200, 30)
        self.bgButton.clicked.connect(self.choose_background)

        self.deleteChatButton = QtWidgets.QPushButton("Удалить чат", self)
        self.deleteChatButton.setGeometry(220, 520, 200, 30)
        self.deleteChatButton.clicked.connect(self.delete_chat_dialog)
        self.deleteChatButton.setGeometry(10, 480, 200, 30)

        self.uselessButton = QtWidgets.QPushButton("Бесполезные функции", self)
        self.uselessButton.setGeometry(10, 440, 200, 30)
        self.uselessButton.clicked.connect(self.open_useless_window)

        self.background_path = load_setting("background_path")
        if self.background_path:
            self._apply_background()

        self.lineEdit.returnPressed.connect(self.send_message)

        self.ws_client = WebSocketClient(self.current_user.id, self.on_message_received)

        self.load_chats()

    def _username_by_id(self, user_id: int) -> str:
        try:
            user = UserRepository.get_user_by_id(self.session, user_id)
            if user and getattr(user, "username", None):
                return user.username
        except Exception:
            pass
        return str(user_id)

    def load_chats(self):
        chats = ChatService.get_chats_for_user(self.session, self.current_user.id)
        self.listWidget.clear()
        for chat in chats:
            other_ids = [
                uid for uid in (chat.users or []) if uid != self.current_user.id
            ]
            user_id = (
                other_ids[0] if other_ids else (chat.users[0] if chat.users else None)
            )

            display = (
                self._username_by_id(user_id)
                if user_id is not None
                else "Чет не нашлось"
            )
            item = QListWidgetItem(display)
            item.setData(1, user_id)
            self.listWidget.addItem(item)

    def select_chat(self, item: QListWidgetItem):
        self.current_chat_user = item.data(1)
        self.load_messages()

    def load_messages(self):
        if not self.current_chat_user:
            return
        messages = ChatService.get_messages(
            self.session, self.current_user.id, self.current_chat_user
        )
        self.textBrowser.clear()
        for msg in messages:
            if msg.sender == self.current_user.id:
                sender = "Я"
            else:
                sender = self._username_by_id(msg.sender)
            self.textBrowser.append(f"{sender}: {msg.text}")

    def send_message(self):
        if not self.current_chat_user:
            return
        text = self.lineEdit.text().strip()
        if not text:
            return
        msg = ChatService.send_message(
            self.session, self.current_user.id, self.current_chat_user, text
        )
        msg_data = {
            "sender_id": str(self.current_user.id),
            "recipient_id": str(self.current_chat_user),
            "content": text,
        }
        self.ws_client.send_message(msg_data)
        self.textBrowser.append(f"Я: {text}")
        self.lineEdit.clear()

    def on_message_received(self, msg):
        sender_id = int(msg["sender_id"])
        if sender_id == self.current_chat_user:
            username = self._username_by_id(sender_id)
            self.textBrowser.append(f"{username}: {msg['content']}")

    def add_chat_dialog(self):
        username, ok = QInputDialog.getText(
            self, "Создать чат", "Введите username собеседника:"
        )

        if not ok or not username.strip():
            return

        username = username.strip()

        user = UserRepository.get_user_by_username(self.session, username)
        if not user:
            QMessageBox.warning(self, "Ошибка", "Пользователь не найден")
            return

        chat = ChatService.get_or_create_chat(
            self.session, self.current_user.id, user.id
        )

        self.load_chats()
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            if item.data(1) == user.id:
                self.listWidget.setCurrentItem(item)
                self.select_chat(item)
                break

    def choose_background(self):
        path = QFileDialog.getOpenFileName(self, "Выбрать картинку", "")[0]
        if not path:
            return

        save_setting("background_path", path)
        self.background_path = path
        self._apply_background()

    def _apply_background(self):
        if not self.background_path:
            return

        picture = QPixmap(self.background_path)  # это чтоб было)))
        self.textBrowser.setStyleSheet(
            f"""
            QTextBrowser {{
                background-image: url("{self.background_path}");
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            """
        )

    def delete_chat_dialog(self):
        if not self.current_chat_user:
            QMessageBox.warning(self, "Ошибка", "Выберите чат для удаления")
            return

        answer, ok_pressed = QInputDialog.getText(
            self,
            "Подтверждение",
            "Вы уверены, что хотите удалить чат? Введите 'да' для подтверждения:",
        )

        if not ok_pressed or answer.strip().lower() != "да":
            return

        ChatRepository.delete_chat(
            self.session, self.current_user.id, self.current_chat_user
        )

        self.load_chats()
        self.textBrowser.clear()
        self.current_chat_user = None

    def open_useless_window(self):
        self.useless_window = UselessWindow()
        self.useless_window.show()
