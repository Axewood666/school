import random
import string

def random_alphanumeric_string(length):
    return ''.join(
        random.choices(
            string.ascii_letters + string.digits,
            k=length
        )
    )
def generate_profile(user_lastname, id):
    login = user_lastname + f'{id}'
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randrange(6,10)))
    return login, password



