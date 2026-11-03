import random
import string


def generate_random_string(length=10):
    """Генерирует случайную строку для email, пароля или имени."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def generate_random_email():
    """Генерирует уникальный email."""
    return f"{generate_random_string()}@test.ru"