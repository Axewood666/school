import * as process from '/static/js/data_process.js';



function List_of_students() {
    let data = {'fio': document.getElementById("teacher-fio").value};
    if(data.fio === "") return;
    $.ajax({
        url: '/teacher/students',
        type: 'POST',
        data: data,
        success: function (response) {
            process.students_response_process(response);
        },
        error: function (error) {
            console.log(error);
            document.getElementById("output").innerHTML = 'Преподаватель не найден';
        }
    });
}

async function List_of_subjects() {
    let data = {'fio': document.getElementById("teacher-fio").value};
    if(data.fio === "") return;
    try {
        let response = await fetch('/teacher/subjects', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        if (response.ok) {
            let result = await response.json();
            process.subjects_response_process(result.subjects);
        } else {
            document.getElementById("output").innerHTML = "Преподаватель не найден";
        }
    } catch (error) {
        console.error('Ошибка: ', error);
    }
}

async function List_of_grades(){
    let data = {'fio': document.getElementById("teacher-fio").value};
    if(data.fio === "") return;
    try{
    let response = await fetch('/teacher/grades', {
    method: 'POST',
    headers:{
        'Content-Type': 'application/json'
        },
    body: JSON.stringify(data)
    });
    if (response.ok) {
        let result = await response.json();
        process.grade_response_process(result)
    }else{
        document.getElementById("output").innerHTML = "Преподаватель не выставлял оценки";
    }
    } catch (error){
        console.error('Ошибка: ', error)
    }
}



window.List_of_students = List_of_students;
window.List_of_subjects = List_of_subjects;
window.List_of_grades = List_of_grades;



