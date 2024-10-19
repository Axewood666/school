import { getClassmates, getGrades } from '/static/js/student/requests.js';
import { toggleStudentInfo } from '/static/js/student/data-process.js';
import { handleGradeFormSubmit, closeGradeForm, openGradeForm } from '/static/js/script.js';

window.toggleStudentInfo = toggleStudentInfo
window.getClassmates = getClassmates
window.getGrades = getGrades
