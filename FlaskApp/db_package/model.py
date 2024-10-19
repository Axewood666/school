from flask_login import UserMixin
from . import db_utils


class User(UserMixin):
    def __init__(self, id_, login, user_type):
        self.id = id_
        self.login = login
        self.user_type = user_type

    def get_user(login, password, user_type):
        table, id_column = User.get_user_profile_table_and_id_column(user_type)
        if table and id_column:
            try:
                conn = db_utils.get_db_connection()
                cur = conn.cursor()
                cur.execute(f"""
                    SELECT {id_column}, login FROM {table}
                    WHERE login = %s AND (SELECT(password=crypt(%s, password)) from {table})
                """, (login, password))
                user_data = cur.fetchone()
                cur.close()
                conn.close()
                if user_data:
                    return User(id_=f"{user_type}_{user_data[0]}", login=user_data[1], user_type=user_type)
            except:
                return None
        return None

    def get_user_by_id(id_, user_type):
        table, id_column = User.get_user_profile_table_and_id_column(user_type)
        if table and id_column:
            try:
                conn = db_utils.get_db_connection()
                cur = conn.cursor()
                cur.execute(f"""
                    SELECT {id_column}, login FROM {table}
                    WHERE {id_column} = %s
                """, (id_,))
                user_data = cur.fetchone()
                cur.close()
                conn.close()
                if user_data:
                    return User(id_=f"{user_type}_{user_data[0]}", login=user_data[1], user_type=user_type)
            except:
                return None
        return None

    def get_user_profile_table_and_id_column(user_type):
        user_profile_mapping = {
            'student': ('studentprofile', 'studentid'),
            'teacher': ('teacherprofile', 'teacherid'),
            'staff': ('staffprofile', 'staffid')
        }

        if user_type in user_profile_mapping:
            return user_profile_mapping[user_type]
        else:
            return (None, None)
