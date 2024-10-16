from configparser import ConfigParser
import psycopg2

urlconf = 'config/config.ini'
config = ConfigParser()
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
        middlename = f",'{fio[2]}'"
    else:
        middlename = ''
    if len(fio) >= 2:
        name = fio[1]
        lastname = fio[0]
        cur.execute(f"SELECT * FROM get_class_id_by_teacher_name('{name}','{lastname}'{middlename})")
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


def get_teacher_fio(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f"""SELECT lastname, firstname, middlename FROM teacher WHERE teacherid={id}""")
    fio = cur.fetchone()
    cur.close()
    conn.close()
    return fio


def Add_grade(json_data, teacherid, teacher_fio):
    fio = json_data['fio'].split()
    error = 0
    if len(fio) > 2:
        middlename = f"and middlename='{fio[2]}'"
    else:
        middlename = ""
    if len(fio) >= 2:
        subjects = [row[0] for row in get_subjects_by_teacher(teacher_fio)]
        if json_data['subject'] in subjects:
            conn = get_db_connection()
            cur = conn.cursor()
            try:
                cur.execute(f"""INSERT INTO grade (studentid, subjectid, date, grade, teacherid)
                VALUES (
                (SELECT studentid FROM student
                WHERE firstname='{fio[1]}' {middlename} and lastname='{fio[0]}'
                 and classid=(SELECT classid FROM class WHERE classname='{json_data['classname']}' LIMIT 1) LIMIT 1),
                (SELECT subjectid FROM subject
                WHERE subjectname='{json_data['subject']}' LIMIT 1),
                CURRENT_DATE,
                {json_data['grade']}, {teacherid})""")
                conn.commit()
            except Exception as e:
                error = e
            cur.close()
            conn.close()
            return error
        else:
            error = f"Вы не преподаёте {json_data['subject']}"
    else:
        error = f"Ученик {json_data['fio']} не найден"
    return error
