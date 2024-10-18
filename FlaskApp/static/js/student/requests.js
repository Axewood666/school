import * as process from '/static/js/student/data-process.js';
import {print_error, clearElement, Add_cell} from '/static/js/script.js';

export async function getClassmates() {
    try {
    let response = await fetch('student/class?');
    if(response.ok){
        let result = await response.json();
        process.students_response_process(result)
    }else{
        console.log('error')
    }
    }catch(error){
        console.log('Ошибка: ', error);
    }
}

export async function getGrades() {
    try {
    let response = await fetch('student/grades?');
    if(response.ok){
        let result = await response.json();
        process.students_response_process(result)
    }else{
        console.log('error')
    }
    }catch(error){
        console.log('Ошибка: ', error);
    }
}

export async function getClass(className){
    try {
    let response = await fetch('student/class-list', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(className)
    });
    if(response.ok){
        let result = await response.json();
        process.studentsResponseWithButtons(result);
    }else{
        print_error(JSON.parse(error.responseText)[0].error)
    }
    }catch(error){
        console.log('Ошибка: ', error);
    }
}

export async function getGradesByFio(fio) {
    try {
    let response = await fetch('student/student-grades', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(fio)
    });
    if(response.ok){
        let result = await response.json();
        process.students_response_process(result)
        return 1
    }else{
        print_error(JSON.parse(error.responseText)[0].error)
    }
    }catch(error){
        console.log('Ошибка: ', error);
    }
    return 0
}