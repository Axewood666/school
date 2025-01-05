import random
import string

from FlaskApp.app import schoolDB, login_manager
from FlaskApp.db_package.model import User

@login_manager.user_loader
def load_user(user_id):
   try:
       user_type, id_ = user_id.split('_')
       user = User.get_user_by_id(id_, user_type, schoolDB)
       return user
   except:
       return None

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

