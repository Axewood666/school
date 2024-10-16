import {List_of_grades, List_of_students, List_of_subjects} from '/static/js/teacher/requests.js';

function getListOfStudents(){
    let data = document.getElementById("teacher-fio").value;
    List_of_students(data)
}
function getListOfSubjects(){
    let data = document.getElementById("teacher-fio").value;
    List_of_subjects(data)
}
function getListOfGrades(){
    let data = document.getElementById("teacher-fio").value;
    List_of_grades(data)
}

window.getListOfStudents = getListOfStudents;
window.getListOfSubjects = getListOfSubjects;
window.getListOfGrades = getListOfGrades;