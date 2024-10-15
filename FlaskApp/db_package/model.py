from flask_login import UserMixin
from . import db_utils
class User(UserMixin):
    def __init__(self, id_, login, user_type):
        self.id = id_
        self.login = login
        self.user_type = user_type

    def get_user(login, password, user_type):
        conn = db_utils.get_db_connection()
        cur = conn.cursor()

        table = 'studentprofile' if user_type == 'student' else 'teacherprofile'
        id_column = 'studentid' if user_type == 'student' else 'teacherid'

        cur.execute(f"""
            SELECT {id_column}, login FROM {table}
            WHERE login = %s AND (SELECT(password=crypt(%s, password)) from {table})
        """, (login, password))
        user_data = cur.fetchone()
        cur.close()
        conn.close()
        if user_data:
            return User(id_=f"{user_type}_{user_data[0]}", login=user_data[1], user_type=user_type)
        return None

    def get_user_by_id(id_, user_type):
        conn = db_utils.get_db_connection()
        cur = conn.cursor()

        # Determine the table and id column based on user type
        table = 'studentprofile' if user_type == 'student' else 'teacherprofile'
        id_column = 'studentid' if user_type == 'student' else 'teacherid'

        # Query the database for the user's data based on their id
        cur.execute(f"""
            SELECT {id_column}, login FROM {table}
            WHERE {id_column} = %s
        """, (id_,))

        user_data = cur.fetchone()
        cur.close()
        conn.close()
        if user_data:
            return User(id_=f"{user_type}_{user_data[0]}", login=user_data[1], user_type=user_type)
        return None