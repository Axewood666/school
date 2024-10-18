import {print_error, clearElement, Add_cell} from '/static/js/script.js';

export function subjects_response_process(result){
    const ol = document.createElement("ol");
    for(let i = 0; i < result.length; i++){
        let el = document.createElement("li")
        let aEl = document.createElement("a")
        aEl.setAttribute("href", `${result[i]}`);
        let elText = document.createTextNode(`${result[i]}`);
        aEl.appendChild(elText);
        el.appendChild(aEl);
        ol.appendChild(el);
    }
    const outputElement = document.getElementById("output");
    clearElement(outputElement);
     outputElement.appendChild(ol);
     ol.classList.add('rectangle')
}

export function students_response_process(response) {
    const className = response.pop();
    const tbl = createTable(response, className);
    const outputElement = document.getElementById("output");
    clearElement(outputElement);
    outputElement.appendChild(tbl);
}

function createTable(response, className) {
    const tbl = document.createElement("table");
    const tblBody = document.createElement("tbody");

    const classHeader = createClassHeader(className, response[0].length);
    tblBody.appendChild(classHeader);

    const headerRow = createHeaderRow(response[0]);
    tblBody.appendChild(headerRow);

    const dataRows = createDataRows(response.slice(1));
    dataRows.forEach(row => tblBody.appendChild(row));

    tbl.appendChild(tblBody);
    return tbl;
}

function createClassHeader(className, colspan) {
    let row = document.createElement("tr");
    let headCell = document.createElement("th");
    let cellText = document.createTextNode(`Class ${className}:`);
    headCell.appendChild(cellText);
    headCell.setAttribute("colspan", colspan);
    headCell.style.textAlign = "center";
    row.appendChild(headCell);
    return row;
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

function createDataRows(data) {
    return data.map(student => {
        let row = document.createElement("tr");
        student.forEach(item => {
            const cell = document.createElement("td");
            let text = item != null ? item : '';
            let cellText = document.createTextNode(text);
            cell.appendChild(cellText);
            row.appendChild(cell);
        });
        return row;
    });
}

export function grade_response_process(grades){
        const tbl = document.createElement("table");
        const tblBody = document.createElement("tbody");
        for(let i = 0; i < grades.length;i++){
            let row = document.createElement("tr");
            let cell = Add_cell(grades[i].name);
            row.appendChild(cell);
            cell = Add_cell(grades[i].classname);
            row.appendChild(cell);
            cell = Add_cell(grades[i].subject);
            row.appendChild(cell);
            cell = Add_cell(grades[i].grade);
            row.appendChild(cell);
            cell = Add_cell(grades[i].date);
            row.appendChild(cell);
            tblBody.appendChild(row);
        }
        tbl.appendChild(tblBody);
        const outputElement = document.getElementById("output");
        clearElement(outputElement);
        outputElement.appendChild(tbl);
}


