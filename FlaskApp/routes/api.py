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
@api.route("/teacher/input-autocomplete", methods=['GET'])
def teacher_autocomplete():
    fio = request.args.get('term')
    fio = fio.split()
    fio.extend(['', ''])
    teachers_arr = []
    if 1 <= len(fio) <= 5:
        teachers_arr = db.db_utils.find_fio(fio[0], fio[1], fio[2])
        teachers_arr = \
            [' '.join(list(fio if fio[2] else fio[:2])) for fio in teachers_arr]
        print(teachers_arr)
    return json.dumps(teachers_arr)


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
        return {'error': str(error)}, 404
    else:
        arr_fio = json_data['fio'].split()
        dict_fio = {'firstname': arr_fio[1], 'lastname': arr_fio[0]}
        if len(arr_fio) > 2:
            dict_fio['middlename'] = arr_fio[2]
        result = db.db_utils.get_student_grades_by_fio(dict_fio)
        if result:
            fields = ['grade', 'subject', 'teacherfio', 'date']
            dicts_data = [dict(zip(fields, values)) for values in result]
            print(dicts_data)
            for i in range(len(dicts_data)):
                dicts_data[i]['date'] = dicts_data[i]['date'].isoformat()
            dicts_data.append({'error': 0})
            json_res = dicts_data
        else:
            return {'error': 'Не удалось получить оценки студента'}, 404
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


@login_required
@teacher_required
@api.route("/student/input-autocomplete", methods=['GET'])
def classname_autocomplete():
    classname = request.args.get('term')
    classname_arr = db.db_utils.find_classname(classname)
    classname_arr = [str(el[0]) for el in classname_arr]
    return json.dumps(classname_arr)

@login_required
@teacher_required
@api.route("/student/class-list", methods=['POST'])
def class_list_by_name():
    json_data = request.get_json()
    class_name = json_data['className']
    class_list = db.db_utils.get_class_by_class_name(class_name)
    fields = ['firstname', 'middlename', 'lastname', 'phone number', 'email']
    dicts_data = [dict(zip(fields, values)) for values in class_list]
    json_class_list = json.dumps(dicts_data)
    return json_class_list


@login_required
@teacher_required
@api.route("/student/student-grades", methods=['POST'])
def class_list_by_student_fio():
    json_fio = request.get_json()
    grades_tuple = db.db_utils.get_student_grades_by_fio(json_fio)
    if not grades_tuple or len(grades_tuple) == 0:
        return {'error': "У ученика нет оценок"}
    fields = ['Предмет', 'Оценка', 'Преподаватель', 'Дата']
    dicts_data = [dict(zip(fields, values)) for values in grades_tuple]
    for i in range(len(dicts_data)):
        dicts_data[i]['Дата'] = dicts_data[i]['Дата'].isoformat()
    json_grades = json.dumps(dicts_data)
    return json_grades
