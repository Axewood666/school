import json

import requests
from flask import Blueprint, request
from flask_login import current_user, login_required

import FlaskApp.db_package as db

if __name__ == '__main__':
    from requireds import teacher_required, staff_required, student_required, employee_required
else:
    from .requireds import teacher_required, staff_required, student_required, employee_required

api = Blueprint('api', __name__)


@login_required
@staff_required
@api.route("/teacher/students", methods=['POST'])
def list_of_students():
    fio = request.form.get('fio')
    result = db.db_utils.get_class_id_by_teacher_name(fio.split())
    if not result:
        return [{'error': 'Преподавателя с таким фио не существует, либо у него нет класса'}], 404
    else:
        result = db.db_utils.get_class_list_by_classid(result[0])
        new_result = []
        [new_result.append(el[:-1]) for el in result]
        new_result.append(result[1][-1])
        return new_result


@login_required
@staff_required
@api.route("/teacher/subjects", methods=['POST'])
def list_of_subjects():
    json_fio = request.get_json()
    fio = json_fio['fio']
    result = db.db_utils.get_subjects_by_teacher(fio.split())
    if not result:
        return {"error": "Преподавателя с таким фио не существует, либо он не ведёт предметы"}, 404
    subjects = [row[0] for row in result]
    json_res = {'subjects': subjects}
    return json.dumps(json_res)


@login_required
@staff_required
@api.route("/teacher/grades", methods=['POST'])
def list_of_grades():
    json_fio = request.get_json()
    fio = json_fio['fio']
    result = db.db_utils.get_grades_by_teacher(fio.split())
    if not result:
        return {"error": "Преподавателя с таким фио не существует, либо он не выставлял оценки"}, 404
    fields = ['name', 'classname', 'subject', 'grade', 'date']
    dicts_data = [dict(zip(fields, values)) for values in result]
    for i in range(len(dicts_data)):
        dicts_data[i]['date'] = dicts_data[i]['date'].isoformat()
    json_data = json.dumps(dicts_data)
    return json_data


@login_required
@teacher_required
@api.route("/profile/teacher/add-grade", methods=['POST'])
def add_grade():
    json_data = request.get_json()
    teacher_id = current_user.id.split('_')[1]
    teacher_fio = db.db_utils.get_teacher_fio(teacher_id)
    error = db.db_utils.Add_grade(json_data, teacher_id, teacher_fio)
    if error:
        json_res = [{'error': str(error)}]
    else:
        result = db.db_utils.get_grades_by_teacher(teacher_fio)
        fields = ['name', 'classname', 'subject', 'grade', 'date']
        dicts_data = [dict(zip(fields, values)) for values in result]
        for i in range(len(dicts_data)):
            dicts_data[i]['date'] = dicts_data[i]['date'].isoformat()
        dicts_data.append({'error': 0})
        json_res = dicts_data
    return json.dumps(json_res)


@login_required
@student_required
@api.route("/profile/student/class", methods=['GET'])
def list_of_classmates():
    classmates = db.db_utils.get_student_classmates(current_user.id.split('_')[1])
    if not classmates:
        return {'error': "Возникла ошибка"}
    fields = ['Имя', 'Отчество', 'Фамилия', 'Номер телефона', 'Электронная почта']
    dicts_data = [dict(zip(fields, values)) for values in classmates]
    json_classmates = json.dumps(dicts_data)
    return json_classmates
@login_required
@student_required
@api.route("/profile/student/grades", methods=['GET'])
def list_of_student_grades():
    grades = db.db_utils.get_student_grades(current_user.id.split('_')[1])
    if not grades:
        return {'error': "Возникла ошибка"}
    fields = ['Предмет', 'Оценка', 'Преподаватель', 'Дата']
    dicts_data = [dict(zip(fields, values)) for values in grades]
    for i in range(len(dicts_data)):
        dicts_data[i]['Дата'] = dicts_data[i]['Дата'].isoformat()
    json_grades = json.dumps(dicts_data)
    return json_grades