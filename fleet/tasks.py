from celery import shared_task
import time


@shared_task
def send_notification(message):
    # Имитируем долгую работу (например, отправку СМС или письма)
    print(f"Начинаю отправку уведомления: {message}")
    time.sleep(5)  # Ждем 5 секунд (как будто СМС отправляется)
    print(f"Уведомление успешно отправлено: {message}")
    return "Успех"
