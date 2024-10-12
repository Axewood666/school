import json

from flask import Flask, render_template, request, jsonify
import db_utils

app = Flask(__name__)


@app.route("/")
def Main():
    return render_template('index.html')

@app.route("/teacher")
def Teacher():
    return render_template('teacher.html')
@app.route("/teacher/list-of-students", methods=['POST'])
def List_of_students():
    name = request.form.get('_name')
    lastName = request.form.get('_lastName')
    middleName = request.form.get('_middleName')
    result = db_utils.get_class_id_by_teacher_name(name, lastName, middleName)
    if result == 404:
        return 'Преподавателя с таким фио не существует, либо у него нет класса!', 404
    else:
        result = db_utils.get_class_list_by_classid(result[0])
    return result

@app.route("/teacher/list-of-subjects", methods=['POST'])
def List_of_subjects():
    jsonFIO = request.get_json()
    name = jsonFIO['_name']
    lastName = jsonFIO['_lastName']
    middleName = jsonFIO['_middleName']
    teacherId = db_utils.get_teacher_id_by_name(name, lastName, middleName)
    if teacherId == 404:
        return "Преподаватель не найден", 404
    result = db_utils.get_subjects_by_teacher(teacherId[0])
    subjects = [row[0] for row in result]
    jsonRes = {'subjects': subjects}
    return json.dumps(jsonRes)

if __name__ == "__main__":
    app.run()