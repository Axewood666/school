import json

from flask import Blueprint, request
from flask_login import current_user, login_required

import FlaskApp.db_package as db

if __name__ == '__main__':
    from requireds import teacher_required, staff_required, student_required, employee_required
else:
    from .requireds import teacher_required, staff_required, student_required, employee_required

api = Blueprint('api', __name__)


@api.route("/teacher/input-autocomplete", methods=['GET'])
@login_required
@staff_required
def teacher_autocomplete():
    fio = request.args.get('term')
    fio = fio.split()
    fio.extend(['', ''])
    teachers_arr = []
    if 1 <= len(fio) <= 5:
        teachers_arr = db.schoolDB.find_fio(fio[0], fio[1], fio[2])
        teachers_arr = \
            [' '.join(list(fio if fio[2] else fio[:2])) for fio in teachers_arr]
    return json.dumps(teachers_arr)


@api.route("/teacher/students", methods=['POST'])
@login_required
@staff_required
def list_of_students():
    fio = request.form.get('fio')
    class_id_tuple = db.schoolDB.get_class_id_by_teacher_name(fio.split())
    if not class_id_tuple:
        return [{'error': 'Преподавателя с таким фио не существует, либо у него нет класса'}], 404
    else:
        class_tuple = db.schoolDB.get_class_list_by_classid(class_id_tuple[0])
        class_list = []
        [class_list.append(el[:-1]) for el in class_tuple]
        class_list.append(class_tuple[1][-1])
        return class_list


@api.route("/teacher/subjects", methods=['POST'])
@login_required
@staff_required
def list_of_subjects():
    json_fio = request.get_json()
    fio = json_fio['fio']
    subjects_tuple = db.schoolDB.get_subjects_by_teacher(fio.split())
    if not subjects_tuple:
        return {"error": "Преподавателя с таким фио не существует, либо он не ведёт предметы"}, 404
    subjects_list = [row[0] for row in subjects_tuple]
    json_res = {'subjects': subjects_list}
    return json.dumps(json_res)


@api.route("/teacher/grades", methods=['POST'])
@login_required
@staff_required
def list_of_grades():
    json_fio = request.get_json()
    fio = json_fio['fio']
    grades_tuple = db.schoolDB.get_grades_by_teacher(fio.split())
    if not grades_tuple:
        return {"error": "Преподавателя с таким фио не существует, либо он не выставлял оценки"}, 404
    fields = ['name', 'classname', 'subject', 'grade', 'date']
    dicts_data = [dict(zip(fields, values)) for values in grades_tuple]
    for i in range(len(dicts_data)):
        dicts_data[i]['date'] = dicts_data[i]['date'].isoformat()
    json_grades = json.dumps(dicts_data)
    return json_grades


@api.route("/profile/teacher/add-grade", methods=['POST'])
@login_required
@teacher_required
def add_grade():
    json_data = request.get_json()
    teacher_id = current_user.id.split('_')[1]
    teacher_fio = db.schoolDB.get_teacher_fio(teacher_id)
    error = db.schoolDB.Add_grade(json_data, teacher_id, teacher_fio)
    if error:
        return {'error': str(error)}, 404
    else:
        arr_fio = json_data['fio'].split()
        dict_fio = {'firstname': arr_fio[1], 'lastname': arr_fio[0]}
        if len(arr_fio) > 2:
            dict_fio['middlename'] = arr_fio[2]
        grades_tuple = db.schoolDB.get_student_grades_by_fio(dict_fio)
        if grades_tuple:
            fields = ['grade', 'subject', 'teacherfio', 'date']
            dicts_grades = [dict(zip(fields, values)) for values in grades_tuple]
            for i in range(len(dicts_grades)):
                dicts_grades[i]['date'] = dicts_grades[i]['date'].isoformat()
            dicts_grades.append({'error': 0})
            json_res = dicts_grades
        else:
            return {'error': 'Не удалось получить оценки студента'}, 404
        return json.dumps(json_res)


@api.route("/student/input-autocomplete", methods=['GET'])
@login_required
@employee_required
def classname_autocomplete():
    classname = request.args.get('term')
    classname_tuple = db.schoolDB.find_classname(classname)
    classname_arr = [str(el[0]) for el in classname_tuple]
    return json.dumps(classname_arr)


@api.route("/student/class-list", methods=['POST'])
@login_required
@employee_required
def class_list_by_classname():
    json_data = request.get_json()
    class_name = json_data['className']
    class_list = db.schoolDB.get_class_by_class_name(class_name)
    if class_list:
        json_class_list = [dict()]
        if current_user.user_type == "teacher":
            fields = ['firstname', 'middlename', 'lastname', 'phone number', 'email']
            dicts_data = [dict(zip(fields, values)) for values in class_list[:5]]
            json_class_list = json.dumps(dicts_data)
        elif current_user.user_type == "staff":
            fields = ['firstname', 'middlename', 'lastname', 'phone number', 'email', 'address', 'birthdate']
            dicts_data = [dict(zip(fields, values)) for values in class_list]
            for i in range(len(dicts_data)):
                dicts_data[i]['birthdate'] = dicts_data[i]['birthdate'].isoformat()
            json_class_list = json.dumps(dicts_data)
        return json_class_list
    return {'error': 'Не найти класс'}, 404


@api.route("/student/student-grades", methods=['POST'])
@login_required
@employee_required
def class_list_by_student_fio():
    json_fio = request.get_json()
    grades_tuple = db.schoolDB.get_student_grades_by_fio(json_fio)
    if not grades_tuple or len(grades_tuple) == 0:
        return {'error': "У ученика нет оценок"}
    fields = ['Предмет', 'Оценка', 'Преподаватель', 'Дата']
    dicts_data = [dict(zip(fields, values)) for values in grades_tuple]
    for i in range(len(dicts_data)):
        dicts_data[i]['Дата'] = dicts_data[i]['Дата'].isoformat()
    json_grades = json.dumps(dicts_data)
    return json_grades


@api.route("/profile/student/class", methods=['GET'])
@login_required
@student_required
def list_of_classmates():
    classmates = db.schoolDB.get_student_classmates(current_user.id.split('_')[1])
    if not classmates:
        return {'error': "Возникла ошибка"}, 404
    fields = ['Имя', 'Отчество', 'Фамилия', 'Номер телефона', 'Электронная почта']
    dicts_data = [dict(zip(fields, values)) for values in classmates]
    json_classmates = json.dumps(dicts_data)
    return json_classmates


@api.route("/profile/student/grades", methods=['GET'])
@login_required
@student_required
def list_of_student_grades():
    grades = db.schoolDB.get_student_grades(current_user.id.split('_')[1])
    if not grades:
        return {'error': "Возникла ошибка"}
    fields = ['Предмет', 'Оценка', 'Преподаватель', 'Дата']
    dicts_data = [dict(zip(fields, values)) for values in grades]
    for i in range(len(dicts_data)):
        dicts_data[i]['Дата'] = dicts_data[i]['Дата'].isoformat()
    json_grades = json.dumps(dicts_data)
    return json_grades
