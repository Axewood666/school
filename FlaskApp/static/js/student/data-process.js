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
        const emptyRow = document.createElement("tr");
        const emptyCell = document.createElement("td");
        emptyCell.appendChild(document.createTextNode("No students found"));
        emptyCell.setAttribute("colspan", "5");
        emptyRow.appendChild(emptyCell);
        tblBody.appendChild(emptyRow);
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

function clearElement(element) {
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
}