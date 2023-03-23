import random
import string

def generate_random_string():
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(16))

def custom_generate_random_string(value):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(value))