from flask import Flask, render_template, request, Response
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
        return 'Преподавателя с таким фио не существует, либо у него нет класса!', 404
    else:
        result = cur.fetchone()
        cur.execute(f'''SELECT 
            s.FirstName,
            s.MiddleName,
            s.LastName,
            s.BirthDate,
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
            s.CLASSID={result[0]}''')
        result = cur.fetchall()
        headers = tuple([i[0] for i in cur.description])
        result.insert(0, headers)
    cur.close()
    conn.close()
    return result

if __name__ == "__main__":
    app.run()