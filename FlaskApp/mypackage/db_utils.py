from configparser import ConfigParser
import psycopg2
from flask_login import UserMixin

urlconf  = 'config/config.ini'
config =ConfigParser()
config.read(urlconf)
user_db = config['login_db']['user_db']
password_db = config['login_db']['password_db']
name_db = config['login_db']['database_name']

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database=name_db,
                            user=user_db,
                            password=password_db)
    return conn

def get_class_id_by_teacher_name(fio):
    conn = get_db_connection()
    cur = conn.cursor()
    if len(fio) > 2:
        name = fio[1]
        lastname = fio[0]
        middlename = fio[2]
        cur.execute(f"SELECT * FROM get_class_id_by_teacher_name('{name}','{lastname}','{middlename}')")
    if len(fio) == 2:
        name = fio[1]
        lastname = fio[0]
        cur.execute(f"SELECT * FROM get_class_id_by_teacher_name('{name}','{lastname}')")
    if cur.rowcount == 0:
        result = 404
    else:
        result = cur.fetchone()
    cur.close()
    conn.close()
    return result


def get_class_list_by_classid(classid):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f'''SELECT
                s.firstname,
                s.middlename,
                s.lastname,
                CAST(s.BirthDate AS TEXT),
                s.Gender,
                s.Address,
                s.PhoneNumber,
                s.Email,
                c.ClassName
            FROM
                Student s
            JOIN
                Class c ON s.ClassID = c.ClassID
            WHERE
                s.CLASSID={classid}''')
    result = cur.fetchall()
    headers = tuple([i[0] for i in cur.description])
    result.insert(0, headers)
    cur.close()
    conn.close()
    return result


def get_subjects_by_teacher(fio):
    conn = get_db_connection()
    cur = conn.cursor()
    if len(fio) > 2:
        middlename = fio[2]
        query = f"and middlename='{middlename}'"
    if len(fio) >= 2:
        name = fio[1]
        lastname = fio[0]
        query = ""
        cur.execute(f"""SELECT subjectname FROM subject
                 WHERE subjectid IN
                 (SELECT subjectid FROM teachersubject
                 WHERE  teacherid=(SELECT teacherid FROM teacher
                 WHERE firstname='{name}' and lastname='{lastname}' {query}))""")
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result


def get_grades_by_teacher(fio):
    conn = get_db_connection()
    cur = conn.cursor()
    if len(fio) > 2:
        middlename = fio[2]
        query = f"and middlename='{middlename}'"
    if len(fio) >= 2:
        name = fio[1]
        lastname = fio[0]
        query = ""
        cur.execute(f"""SELECT
               (SELECT CONCAT_WS(' ', firstname, lastname, middlename)
               FROM student WHERE studentid = G.studentid) as studentname,
               (SELECT classname FROM class
               WHERE classid=(SELECT classid FROM student WHERE studentid=G.studentid)) as classname,
               (SELECT subjectname FROM subject where subjectid=G.subjectid) as subject,
               G.grade,
               G.date
               FROM grade G
               WHERE teacherid = (SELECT teacherid FROM teacher
               WHERE firstname='{name}' and lastname='{lastname}' {query})""")
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

# def Add_grade(json_data):
#     conn = get_db_connection()
#     cur = conn.cursor()
#     cur.execute(f"""INSERT INTO grade (studentid, subjectid, date, grade, teacherid)
#     VALUES (
#     (SELECT studentid FROM student
#     WHERE firstname='Carol' and middlename='C.' and lastname='Davis' LIMIT 1),
#     (SELECT subjectid FROM subject
#     WHERE subjectname='History' LIMIT 1),
#     CURRENT_DATE,
#     5,
#     (SELECT teacherid FROM teacher
#     WHERE firstname='John'
#     and lastname='Doe'
#     and middlename='A.'))""")
#     cur.close()
#     conn.close()
#     return 1

class User(UserMixin):
    def __init__(self, id_, login, user_type):
        self.id = id_
        self.login = login
        self.user_type = user_type

    def get_user(login, password, user_type):
        conn = get_db_connection()
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
        conn = get_db_connection()
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