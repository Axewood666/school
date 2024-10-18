import { addGrade } from '/static/js/teacher/requests.js';

export function print_error(error){
    const tbl = document.createElement("table");
    const tblBody = document.createElement("tbody");
    const headCell = document.createElement("th");
    const cellText = document.createTextNode("ERROR")
    let row = document.createElement("tr");
    headCell.appendChild(cellText);
    row.appendChild(headCell);
    tblBody.appendChild(row);
    row = document.createElement("tr");
    let cell = Add_cell(error)
    cell.classList.add("error-message")
    row.appendChild(cell)
    tblBody.appendChild(row)
    tbl.appendChild(tblBody)
    const outputElement = document.getElementById("output");
    clearElement(outputElement);
    tbl.classList.add("table-error")
    outputElement.appendChild(tbl);
}

export function Add_cell(el){
    const cell = document.createElement("td");
    let cellText = document.createTextNode(`${el}`);
    cell.appendChild(cellText);
    return cell;
}

export function clearElement(element) {
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
}

function serializeForm(formNode){
    const { elements } = formNode;
    const data = Array.from(elements)
    .filter(item => !!item.name)
    .reduce((arr, el) => {
        const {name, value} = el;
        arr[name] = value
        return arr;
    }, {});
    return data;
}

export function openGradeForm(){
    document.getElementById("popup-background").style.display = "flex";
}
export function closeGradeForm(){
    event.preventDefault();
    document.getElementById("popup-background").style.display = "none";
}

export function handleGradeFormSubmit(event){
    event.preventDefault();
    document.getElementById("popup-background").style.display = "none";
    const gradeForm = document.getElementById("grade-form");
    const data = serializeForm(gradeForm);
    addGrade(data);
}