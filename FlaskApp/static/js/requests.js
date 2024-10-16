import * as process from '/static/js/data_process.js';

export async function addGrade(data) {
    try {
    let response = await fetch('teacher/add-grade', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    if(response.ok){
        let result = await response.json();
        let isError = (result.pop()).error
        if(isError){
            process.print_error(isError)
        }else{
            process.grade_response_process(result)
        }
    }else{
        console.log('error')
    }
    }catch(error){
        console.log('Ошибка: ', error);
    }
}

export function List_of_students(fio) {
    let data = {'fio': fio};
    if(data.fio === "") return;
    $.ajax({
        url: '/teacher/students',
        type: 'POST',
        data: data,
        success: function (response) {
            console.log(response);
            process.students_response_process(response);
        },
        error: function (error) {
            process.print_error(JSON.parse(error.responseText)[0].error)

        }
    });
}

export async function List_of_subjects(fio) {
    let data = {'fio': fio};
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
            let errorResult = await response.json();
            process.print_error(errorResult.error)
        }
    } catch (error) {
        console.error('Ошибка: ', error);
    }
}

export async function List_of_grades(fio){
    let data = {'fio': fio};
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
        let errorResult = await response.json();
        process.print_error(errorResult.error)
    }
    } catch (error){
        console.error('Ошибка: ', error)
    }
}

window.List_of_students = List_of_students;
window.List_of_subjects = List_of_subjects;
window.List_of_grades = List_of_grades;



