from flask import Flask, render_template, request, json
import psycopg2

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='schoolDB',
                            user='postgres',
                            password='axewood')
    return conn

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/teacher")
def teacher():
    ''' conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT')
    users = cur.fetchall()
    cur.close()
    conn.close() '''
    return render_template('teacher.html')
@app.route("/process", methods=['POST'])
def process():
    name = request.form.get('_name')
    lastName = request.form.get('_lastName')
    middleName = request.form.get('_middleName')
    conn = get_db_connection()
    cur = conn.cursor()
    if len(middleName) != 0:
        cur.execute(f"SELECT * FROM get_class_id_by_teacher_name('{name}','{lastName}','{middleName}')")
    else:
        cur.execute(f"SELECT * FROM get_class_id_by_teacher_name('{name}','{lastName}')")
    if(cur.rowcount == 0):
        result = "Преподавателя с таким именем не существует, либо у него нету класса"
    else:
        result = cur.fetchone()
        cur.execute(f"SELECT * FROM STUDENT WHERE CLASSID={result[0]}")
        result = cur.fetchall()
    cur.close()
    conn.close()
    return result

if __name__ == "__main__":
    app.run()