import * as process from '/static/js/teacher/data_process.js';
import {print_error, clearElement, Add_cell} from '/static/js/script.js';
import { students_response_process } from '/static/js/student/data-process.js';

export async function addGrade(data) {
    try {
    let response = await fetch('/profile/teacher/add-grade', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    if(response.ok){
        let result = await response.json();
        let isError = (result.pop()).error
        if(isError){
            print_error(isError)
        }else{
            students_response_process(result)
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

    fetch('/teacher/students', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(errorData => {
                throw new Error(errorData[0].error);
            });
        }
        return response.json();
    })
    .then(responseData => {
        process.students_response_process(responseData);
    })
    .catch(error => {
        print_error(error.message);
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
            print_error(errorResult.error)
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
        print_error(errorResult.error)
    }
    } catch (error){
        console.error('Ошибка: ', error)
    }
}

window.List_of_students = List_of_students;
window.List_of_subjects = List_of_subjects;
window.List_of_grades = List_of_grades;



