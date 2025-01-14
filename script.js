const rows = 10;
const cols = 10;
const spreadsheet = document.getElementById("spreadsheet");

// Initialize spreadsheet
function initSpreadsheet() {
  spreadsheet.style.gridTemplateColumns = `repeat(${cols}, 100px)`;
  for (let i = 0; i < rows * cols; i++) {
    const cell = document.createElement("div");
    cell.contentEditable = true;
    cell.className = "cell";
    cell.dataset.row = Math.floor(i / cols) + 1;
    cell.dataset.col = i % cols + 1;
    cell.dataset.id = `${String.fromCharCode(65 + (i % cols))}${Math.floor(i / cols) + 1}`;
    spreadsheet.appendChild(cell);
  }
}

// Formatting functions
function applyFormat(type) {
  const selection = document.getSelection();
  if (selection.rangeCount > 0) {
    const cell = selection.anchorNode.parentElement;
    if (cell.classList.contains("cell")) {
      switch (type) {
        case "bold":
          cell.style.fontWeight = cell.style.fontWeight === "bold" ? "normal" : "bold";
          break;
        case "italic":
          cell.style.fontStyle = cell.style.fontStyle === "italic" ? "normal" : "italic";
          break;
        case "uppercase":
          cell.textContent = cell.textContent.toUpperCase();
          break;
        case "lowercase":
          cell.textContent = cell.textContent.toLowerCase();
          break;
        case "trim":
          cell.textContent = cell.textContent.trim();
          break;
      }
    }
  }
}

// Add rows and columns
function addRow() {
  for (let i = 0; i < cols; i++) {
    const cell = document.createElement("div");
    cell.contentEditable = true;
    cell.className = "cell";
    spreadsheet.appendChild(cell);
  }
}

function addColumn() {
  const cells = Array.from(spreadsheet.children);
  cells.forEach((cell, index) => {
    if ((index + 1) % cols === 0) {
      const newCell = document.createElement("div");
      newCell.contentEditable = true;
      newCell.className = "cell";
      spreadsheet.insertBefore(newCell, cell.nextSibling);
    }
  });
}

// Mathematical Functions
function calculateFormula() {
  const formula = document.getElementById("formulaBar").value;
  if (!formula.startsWith("=")) return;

  const command = formula.slice(1, 4).toUpperCase();
  const range = formula.match(/\(([^)]+)\)/)[1];
  const [start, end] = range.split(":");

  const startCell = document.querySelector(`[data-id="${start}"]`);
  const endCell = document.querySelector(`[data-id="${end}"]`);
  const startIndex = Array.from(spreadsheet.children).indexOf(startCell);
  const endIndex = Array.from(spreadsheet.children).indexOf(endCell);

  const values = [];
  for (let i = startIndex; i <= endIndex; i++) {
    const value = parseFloat(spreadsheet.children[i].textContent) || 0;
    values.push(value);
  }

  let result;
  switch (command) {
    case "SUM":
      result = values.reduce((a, b) => a + b, 0);
      break;
    case "AVG":
      result = values.reduce((a, b) => a + b, 0) / values.length;
      break;
    case "MAX":
      result = Math.max(...values);
      break;
    case "MIN":
      result = Math.min(...values);
      break;
    case "CNT":
      result = values.filter((v) => v !== 0).length;
      break;
  }

  alert(`Result: ${result}`);
}

// Data Quality Functions
function removeDuplicates() {
  const rowsData = {};
  Array.from(spreadsheet.children).forEach((cell, index) => {
    const row = Math.floor(index / cols);
    rowsData[row] = rowsData[row] || [];
    rowsData[row].push(cell.textContent);
  });

  const uniqueRows = Object.values(rowsData).filter((row, index, self) =>
    index === self.findIndex((r) => JSON.stringify(r) === JSON.stringify(row))
  );

  spreadsheet.innerHTML = "";
  uniqueRows.forEach((row) => {
    row.forEach((value) => {
      const cell = document.createElement("div");
      cell.contentEditable = true;
      cell.className = "cell";
      cell.textContent = value;
      spreadsheet.appendChild(cell);
    });
  });
}

function findAndReplace() {
  const findText = document.getElementById("findText").value;
  const replaceText = document.getElementById("replaceText").value;
  Array.from(spreadsheet.children).forEach((cell) => {
    if (cell.textContent.includes(findText)) {
      cell.textContent = cell.textContent.replace(findText, replaceText);
    }
  });
}

// Initialize
initSpreadsheet();
