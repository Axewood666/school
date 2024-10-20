import psycopg2
from flask_login import UserMixin
from . import db_utils


class SchoolDB:
    def __init__(self, db_name, user, password, host='localhost'):
        self.conn = psycopg2.connect(host=host,
                                     database=db_name,
                                     user=user,
                                     password=password)
        self.cur = self.conn.cursor()

    def close_connection(self):
        self.cur.close()
        self.conn.close()

    def find_fio(self, lastname, firstname, middlename):
        if lastname and not firstname:
            lastname = f"lastname LIKE '{lastname}%'"
        elif firstname and not middlename:
            lastname = f"lastname='{lastname}'"
            firstname = f"and firstname LIKE '{firstname}%'"
        elif middlename:
            lastname = f"lastname='{lastname}'"
            firstname = f"and firstname='{firstname}'"
            middlename = f"and middlename LIKE '{middlename}%'"
        try:
            self.cur.execute(
                f"""SELECT lastname, firstname, middlename FROM teacher WHERE {lastname} {firstname} {middlename}""")
            teachers_fio = self.cur.fetchall()
        except:
            return []
        return teachers_fio

    def get_class_id_by_teacher_name(self, fio):
        if len(fio) > 2:
            middlename = f",'{fio[2]}'"
        else:
            middlename = ''
        if len(fio) >= 2:
            try:
                name = fio[1]
                lastname = fio[0]
                self.cur.execute(f"SELECT * FROM get_class_id_by_teacher_name('{name}','{lastname}'{middlename})")
                class_id = self.cur.fetchone()
                return class_id
            except:
                pass
        return None

    def get_class_list_by_classid(self, classid):
        try:
            self.cur.execute(f'''SELECT
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
            class_tuple = self.cur.fetchall()
            if (len(class_tuple) != 0):
                headers = tuple([i[0] for i in self.cur.description])
                class_tuple.insert(0, headers)
                return class_tuple
            else:
                return None
        except:
            return None

    def get_subjects_by_teacher(self, fio):
        if len(fio) > 2:
            middlename = fio[2]
            query = f"and middlename='{middlename}'"
        else:
            query = ""
        if len(fio) >= 2:
            name = fio[1]
            lastname = fio[0]
            try:
                self.cur.execute(f"""SELECT subjectname FROM subject
                         WHERE subjectid IN
                         (SELECT subjectid FROM teachersubject
                         WHERE  teacherid=(SELECT teacherid FROM teacher
                         WHERE firstname='{name}' and lastname='{lastname}' {query}))""")
                subjects = self.cur.fetchall()
                return subjects
            except:
                pass
        return None

    def get_grades_by_teacher(self, fio):
        if len(fio) > 2:
            middlename = fio[2]
            query = f"and middlename='{middlename}'"
        else:
            query = ""
        if len(fio) >= 2:
            name = fio[1]
            lastname = fio[0]
            try:
                self.cur.execute(f"""SELECT
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
                grades = self.cur.fetchall()
                return grades
            except:
                pass
        return None

    def get_teacher_fio(self, id):
        self.cur.execute(f"""SELECT lastname, firstname, middlename FROM teacher WHERE teacherid={id}""")
        fio = self.cur.fetchone()
        return fio

    def Add_grade(self, json_data, teacherid, teacher_fio):
        fio = json_data['fio'].split()
        error = 0
        if len(fio) > 2:
            middlename = f"and middlename='{fio[2]}'"
        else:
            middlename = ""
        if len(fio) >= 2:
            subjects = [row[0] for row in self.get_subjects_by_teacher(teacher_fio)]
            if json_data['subject'] in subjects:
                try:
                    self.cur.execute(f"""INSERT INTO grade (studentid, subjectid, date, grade, teacherid)
                    VALUES (
                    (SELECT studentid FROM student
                    WHERE firstname='{fio[1]}' {middlename} and lastname='{fio[0]}'
                     and classid=(SELECT classid FROM class WHERE classname='{json_data['classname']}' LIMIT 1) LIMIT 1),
                    (SELECT subjectid FROM subject
                    WHERE subjectname='{json_data['subject']}' LIMIT 1),
                    CURRENT_DATE,
                    {json_data['grade']}, {teacherid})""")
                    self.conn.commit()
                except Exception as e:
                    error = e
                return error
            else:
                error = f"Вы не преподаёте {json_data['subject']}"
        else:
            error = f"Ученик {json_data['fio']} не найден"
        return error

    def find_classname(self, classname):
        try:
            self.cur.execute(
                f"""SELECT classname FROM class WHERE classname LIKE '{classname}%'""")
            classnames = self.cur.fetchall()
            return classnames
        except:
            return []

    def get_student_info(self, student_id):
        try:
            self.cur.execute(f"""SELECT S.firstname, S.middlename, S.lastname, S.birthdate, 
                S.gender, S.address, S.phonenumber, S.email, 
                (SELECT classname FROM class WHERE classid=S.classid),
                    (SELECT CONCAT_WS(' ', firstname, lastname, middlename)
                    FROM teacher
                    WHERE teacherid=(SELECT teacherid FROM class WHERE classid=S.classid))
            FROM student S WHERE studentid={student_id}""")
            student = self.cur.fetchone()
            return student
        except:
            return None

    def get_student_classmates(self, student_id):
        try:
            self.cur.execute(f"""SELECT firstname, middlename, lastname, phonenumber, email
             FROM student WHERE classid=(SELECT classid FROM student WHERE studentid={student_id})""")
            classmates = self.cur.fetchall()
            return classmates
        except:
            return None

    def get_student_grades(self, student_id):
        try:
            self.cur.execute(f"""SELECT
               G.grade,
               (SELECT subjectname FROM subject where subjectid=G.subjectid) as subject,
               (SELECT CONCAT_WS(' ', firstname, lastname, middlename)
               FROM teacher WHERE teacherid = G.teacherid) as teachername,
               G.date
               FROM grade G
               WHERE studentid={student_id}""")
            grades = self.cur.fetchall()
            return grades
        except:
            return None

    def get_class_by_class_name(self, class_name):
        try:
            self.cur.execute(f"""SELECT firstname, middlename, lastname, phonenumber, email 
                FROM student 
                WHERE classid=(SELECT classid FROM class WHERE classname='{class_name}')""")
            class_tuple = self.cur.fetchall()
            return class_tuple
        except:
            return None

    def get_student_grades_by_fio(self, fio):
        grades = 0
        if len(fio) > 2:
            middlename = fio['middlename']
            query = f"and middlename='{middlename}'"
        else:
            query = ""
        if len(fio) >= 2:
            try:
                name = fio['firstname']
                lastname = fio['lastname']
                self.cur.execute(f"""SELECT studentid FROM student WHERE firstname='{name}'
                 and lastname='{lastname}' {query}""")
                student_id = self.cur.fetchone()
                grades = self.get_student_grades(student_id[0])
                return grades
            except:
                return None


class User(UserMixin):
    def __init__(self, id_, login, user_type):
        self.id = id_
        self.login = login
        self.user_type = user_type

    def get_user(login, password, user_type, db):
        table, id_column = User.get_user_profile_table_and_id_column(user_type)
        if table and id_column:
            try:
                db.cur.execute(f"""
                    SELECT {id_column}, login FROM {table}
                    WHERE login = %s AND (SELECT(password=crypt(%s, password)) from {table})
                """, (login, password))
                user_data = db.cur.fetchone()
                if user_data:
                    return User(id_=f"{user_type}_{user_data[0]}", login=user_data[1], user_type=user_type)
            except:
                return None
        return None

    def get_user_by_id(id_, user_type, db):
        table, id_column = User.get_user_profile_table_and_id_column(user_type)
        if table and id_column:
            try:
                db.cur.execute(f"""
                    SELECT {id_column}, login FROM {table}
                    WHERE {id_column} = %s
                """, (id_,))
                user_data = db.cur.fetchone()
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
            return None, None
