import { students_response_process, subjects_response_process } from '/static/js/response_processing.js';



export function List_of_students() {
    let data = fio();
    $.ajax({
        url: '/teacher/students',
        type: 'POST',
        data: data,
        success: function (response) {
            students_response_process(response);
        },
        error: function (error) {
            console.log(error);
            document.getElementById("output").innerHTML = error.responseText;
        }
    });
}

export async function List_of_subjects() {
    let data = fio();
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
            subjects_response_process(result.subjects);
        } else {
            document.getElementById("output").innerHTML = "Преподаватель не найден";
        }
    } catch (error) {
        console.error('Ошибка:', error);
    }
}

function fio() {
    let name = document.getElementById('name').value;
    let lastName = document.getElementById('lastName').value;
    let middleName = document.getElementById('middleName').value;
    return {
        '_name': name,
        '_lastName': lastName,
        '_middleName': middleName
    };
}

window.List_of_students = List_of_students;
window.List_of_subjects = List_of_subjects;



