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
@app.route("/teacher/students", methods=['POST'])
def List_of_students(): #сделать через 1 запрос
    name = request.form.get('_name')
    lastName = request.form.get('_lastName')
    middleName = request.form.get('_middleName')
    result = db_utils.get_class_id_by_teacher_name(name, lastName, middleName)
    if result == 404:
        return 'Преподавателя с таким фио не существует, либо у него нет класса!', 404
    else:
        result = db_utils.get_class_list_by_classid(result[0])
    return result
@app.route("/teacher/subjects", methods=['POST'])
def List_of_subjects():
    jsonFIO = request.get_json()
    name = jsonFIO['_name']
    lastName = jsonFIO['_lastName']
    middleName = jsonFIO['_middleName']
    result = db_utils.get_subjects_by_teacher(name, lastName, middleName)
    if (len(result) == 0):
        return {"error": "Преподавателя с таким фио не существует, либо он не ведёт предметы!"}, 404
    subjects = [row[0] for row in result]
    jsonRes = {'subjects': subjects}
    return json.dumps(jsonRes)

@app.route("/teacher/grades", methods=['POST'])
def List_of_grades():
    jsonFIO = request.get_json()
    name = jsonFIO['_name']
    lastName = jsonFIO['_lastName']
    middleName = jsonFIO['_middleName']
    result = db_utils.get_grades_by_teacher(name, lastName, middleName)
    if len(result) == 0:
        return {"error": "Преподавателя с таким фио не существует, либо он не выставлял оценки!"}, 404
    fields = ['name', 'subject', 'date', 'grade']
    dicts_data = [dict(zip(fields, values)) for values in result]
    for i in range(len(dicts_data)):
        dicts_data[i]['date'] = dicts_data[i]['date'].isoformat()
    json_data = json.dumps(dicts_data)
    return json_data

if __name__ == "__main__":
    app.run()
