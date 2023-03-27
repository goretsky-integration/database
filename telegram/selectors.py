from django.db.models import QuerySet

from core.exceptions import NotFoundError
from telegram.models import TelegramChat


def get_telegram_chats(*, limit: int, offset: int) -> QuerySet[TelegramChat]:
    return TelegramChat.objects.all()[offset:offset + limit]


def get_telegram_chats_by_chat_id(chat_id: int) -> QuerySet[TelegramChat]:
    return TelegramChat.objects.filter(chat_id=chat_id)


def get_telegram_chat_by_chat_id(chat_id: int) -> TelegramChat:
    try:
        return TelegramChat.objects.get(chat_id=chat_id)
    except TelegramChat.DoesNotExist:
        raise NotFoundError('Chat by chat ID is not found')
