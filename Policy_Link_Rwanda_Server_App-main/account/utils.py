# utils.py
import random
import string

def generate_otp():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))