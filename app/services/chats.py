from sqlmodel import Session

from app.repositories.chats import ChatRepository


class ChatService:
    @staticmethod
    def get_or_create_chat(session: Session, user1_id: int, user2_id: int):
        return ChatRepository.get_or_create_chat(session, user1_id, user2_id)

    @staticmethod
    def get_chats_for_user(session: Session, user_id: int):
        return ChatRepository.get_chats_for_user(session, user_id)

    @staticmethod
    def get_messages(session: Session, user1_id: int, user2_id: int):
        return ChatRepository.get_messages(session, user1_id, user2_id)

    @staticmethod
    def send_message(
        session: Session, sender_id: int, recipient_id: int, text: str, img: str = None
    ):
        return ChatRepository.save_message(session, sender_id, recipient_id, text, img)
