"""Test GigaChat credentials from .env using GigaChatSession."""

from gigachat_client import GigaChatSession


if __name__ == "__main__":
    session = GigaChatSession()
    answer = session.send_message("Ответь кратко: соединение с GigaChat успешно!")
    print(answer)
