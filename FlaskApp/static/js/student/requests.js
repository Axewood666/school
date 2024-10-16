import * as process from '/static/js/student/data-process.js';

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