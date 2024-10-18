import {print_error, clearElement, Add_cell} from '/static/js/script.js';

export function students_response_process(response) {
    const tbl = createTable(response);
    const outputElement = document.getElementById("output");
    clearElement(outputElement);
    outputElement.appendChild(tbl);
}

function createTable(students) {
    const tbl = document.createElement("table");
    const tblBody = document.createElement("tbody");

    if (students.length > 0) {
        const allKeys = getAllKeys(students);

        const headerRow = createHeaderRow(allKeys);
        tblBody.appendChild(headerRow);

        const dataRows = createDataRows(students, allKeys);
        dataRows.forEach(row => tblBody.appendChild(row));
    } else {
       print_error("Такого класса не существует")
    }

    tbl.appendChild(tblBody);
    return tbl;
}

function getAllKeys(students) {
    const keys = new Set();
    students.forEach(student => {
        Object.keys(student).forEach(key => keys.add(key));
    });
    return Array.from(keys);
}

function createHeaderRow(headers) {
    let row = document.createElement("tr");
    headers.forEach(header => {
        let headCell = document.createElement("th");
        let cellText = document.createTextNode(header);
        headCell.appendChild(cellText);
        row.appendChild(headCell);
    });
    return row;
}

function createDataRows(data, headers) {
    return data.map(student => {
        let row = document.createElement("tr");
        headers.forEach(header => {
            const cell = document.createElement("td");
            let text = student[header] != null ? student[header] : '';
            let cellText = document.createTextNode(text);
            cell.appendChild(cellText);
            row.appendChild(cell);
        });
        return row;
    });
}

export function studentsResponseWithButtons(response) {
    const tbl = createTableWithButtons(response);
    const outputElement = document.getElementById("output-class");
    clearElement(outputElement);
    outputElement.appendChild(tbl);
}

function createTableWithButtons(students) {
    const tbl = document.createElement("table");
    const tblBody = document.createElement("tbody");

    if (students.length > 0) {
        const allKeys = getAllKeys(students);

        const headerRow = createHeaderRow(allKeys);
        tblBody.appendChild(headerRow);

        const dataRows = createDataRowsWithButtons(students, allKeys);
        dataRows.forEach(row => tblBody.appendChild(row));
    } else {
       print_error("Такого класса не существует, либо в нём нет учеников")
    }
    tbl.setAttribute("id", "class-list");
    tbl.appendChild(tblBody);
    tbl.onclick = (event) => {
        let target = event.target;

        while (target && target.tagName.toLowerCase() !== 'tr') {
            target = target.parentElement;
        }

        if (target && target.tagName.toLowerCase() === 'tr') {
            let i = target.rowIndex;
            if(i != 0){
                getStudent(i)
            }
        }
    };
    return tbl;
}

function createDataRowsWithButtons(data, headers) {
    return data.map(student => {
        let row = document.createElement("tr");
        headers.forEach(header => {
            const cell = document.createElement("td");
            let text = student[header] != null ? student[header] : '';
            let cellText = document.createTextNode(text);
            cell.appendChild(cellText);
            row.appendChild(cell);
        });
        return row;
    });
}


export function toggleStudentInfo() {
    const studentInfo = document.getElementById('student-info');
    const toggleText = document.getElementById('toggle-text');
    const toggleButton = document.getElementById('toggle-button');
    if (studentInfo.classList.contains('student-info-toggle')) {
        toggleButton.classList.add('expanded');
        studentInfo.classList.remove('student-info-toggle');

    } else {

        toggleButton.classList.remove('expanded');
        studentInfo.classList.add('student-info-toggle');
    }
}