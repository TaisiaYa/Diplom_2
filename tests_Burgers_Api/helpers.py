import random
import string

def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def generate_user_data():
    email = f"{generate_random_string(5)}@yandex.ru"
    password = generate_random_string(8)
    name = generate_random_string(6)
    return {
        "email": email,
        "password": password,
        "name": name
    }