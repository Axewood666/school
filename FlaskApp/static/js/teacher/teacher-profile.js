import { addGrade } from '/static/js/teacher/requests.js';
import { handleGradeFormSubmit, closeGradeForm, openGradeForm } from '/static/js/script.js';

const gradeForm = document.getElementById("grade-form");
gradeForm.addEventListener('submit', handleGradeFormSubmit);
window.openGradeForm = openGradeForm;
window.closeGradeForm = closeGradeForm;
