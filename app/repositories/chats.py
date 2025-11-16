from sqlalchemy import select
from sqlmodel import Session

from app.models.chats import Chat, Message


class ChatRepository:
    @staticmethod
    def create_chat(session: Session, users: list[int]) -> Chat:
        chat = Chat(users=users)
        session.add(chat)
        session.commit()
        session.refresh(chat)
        return chat

    @staticmethod
    def get_or_create_chat(session: Session, user1_id: int, user2_id: int):
        users_list = sorted([user1_id, user2_id])
        stmt = select(Chat).where(Chat.users == users_list)
        chat = session.scalars(stmt).first()
        if chat:
            return chat
        chat_db = Chat(users=users_list)
        session.add(chat_db)
        session.commit()
        session.refresh(chat_db)
        return chat_db

    @staticmethod
    def get_chats_for_user(session: Session, user_id: int) -> list[Chat]:
        chats = session.query(Chat).all()
        return [c for c in chats if user_id in (c.users or [])]

    @staticmethod
    def get_messages(session: Session, user1_id: int, user2_id: int):
        stmt = (
            select(Message)
            .where(
                ((Message.sender == user1_id) & (Message.user2 == user2_id))
                | ((Message.sender == user2_id) & (Message.user2 == user1_id))  # type: ignore
            )
            .order_by(Message.send_time)  # type: ignore
        )
        return session.scalars(stmt).all()

    @staticmethod
    def save_message(
        session: Session, sender_id: int, recipient_id: int, text: str, img: str = None
    ):
        msg = Message(sender=sender_id, user2=recipient_id, text=text, img=img)
        session.add(msg)
        session.commit()
        session.refresh(msg)
        return msg

    @staticmethod
    def add_user_to_chat(session: Session, chat_id: int, user_id: int) -> Chat:
        chat = session.get(Chat, chat_id)
        if not chat:
            raise ValueError("Неть чатика")
        users = chat.users or []
        if user_id not in users:
            users.append(user_id)
            chat.users = users
            session.add(chat)
            session.commit()
            session.refresh(chat)
        return chat

    @staticmethod
    def remove_user_from_chat(session: Session, chat_id: int, user_id: int) -> Chat:
        chat = session.get(Chat, chat_id)
        if not chat:
            raise ValueError("Неть чатика")
        users = chat.users or []
        if user_id in users:
            users.remove(user_id)
            chat.users = users
            session.add(chat)
            session.commit()
            session.refresh(chat)
        return chat

    @staticmethod
    def delete_chat(session: Session, user1_id: int, user2_id: int):
        stmt = select(Chat)
        chats = session.scalars(stmt).all()

        for chat in chats:
            users = chat.users or []
            if set(users) == {user1_id, user2_id}:
                session.delete(chat)
                session.commit()
                return True
        return False

    @staticmethod
    def edit_message(session: Session, message_id: int, new_text: str) -> Message:
        msg = session.get(Message, message_id)
        if not msg:
            raise ValueError("Сообщение не найдено")
        msg.text = new_text
        session.add(msg)
        session.commit()
        session.refresh(msg)
        return msg
