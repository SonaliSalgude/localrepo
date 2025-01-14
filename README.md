Google Sheets Mimic Web Application
This project is a web-based application that mimics the core functionality of Google Sheets. It provides an interactive spreadsheet where users can perform basic mathematical operations, data quality functions, and cell formatting, while also handling user data entry and validation.

Features
1. Spreadsheet Interface
Mimics Google Sheets UI: The design closely resembles Google Sheets with a familiar toolbar, formula bar, and cell grid.
Drag Functions: Users can drag cells to copy content, formulas, and selections, similar to Google Sheets' behavior.
Cell Dependencies: Formulas automatically update when changes are made to related cells, respecting dependencies.
Basic Cell Formatting: Supports basic formatting such as bold, italic, font size, and color.
Row and Column Management: Users can add, delete, and resize rows and columns.
2. Mathematical Functions
SUM: Calculates the sum of a range of cells.
AVERAGE: Calculates the average of a range of cells.
MAX: Returns the maximum value from a range of cells.
MIN: Returns the minimum value from a range of cells.
COUNT: Counts the number of cells containing numerical values.
3. Data Quality Functions
TRIM: Removes leading and trailing whitespace from a cell.
UPPER: Converts the text in a cell to uppercase.
LOWER: Converts the text in a cell to lowercase.
REMOVE_DUPLICATES: Removes duplicate rows from a selected range.
FIND_AND_REPLACE: Allows users to find and replace specific text within a range of cells.
4. Data Entry and Validation
Supports various data types (numbers, text, dates).
Implements basic data validation checks (e.g., ensuring numeric cells only contain numbers).
5. Testing
Allows users to test implemented functions with their own data.
Results of function execution are displayed clearly.
Technologies Used
1. Frontend Technologies
HTML5:

Why: HTML provides the basic structure of the application, creating the grid layout, toolbar, formula bar, and buttons.
How: The application structure is made up of a table for the grid, input fields for data entry, and interactive elements like buttons and the formula bar.
CSS3:

Why: CSS is used for styling the spreadsheet interface, ensuring it is responsive, visually appealing, and easy to use.
How: Flexbox and Grid layout systems are used for responsive design, while other CSS properties control font size, alignment, and styling of cells.
JavaScript (Vanilla):

Why: JavaScript is used for implementing interactivity and dynamic functionality in the web application.
How: JavaScript handles drag-and-drop functionality, cell updates (dependencies), mathematical operations, and data validation checks. It also enables users to update cells and trigger relevant calculations.
Data Structures Used
1. 2D Array (Grid Representation)
Why: The core data structure for managing the spreadsheet is a 2D array, where each element represents a cell in the spreadsheet.
How: Each row in the grid is represented as an array, and all rows are stored in an array, forming a 2D grid structure.
Cell Format: Each cell is an object that holds its value (text, number, formula), formatting (bold, italic, color), and dependency information.
javascript
Copy code
let spreadsheet = [
  [{value: 'A1', formula: '', formatting: {bold: false}, dependencies: []}],
  [{value: 'B1', formula: '', formatting: {italic: false}, dependencies: []}]
];
2. HashMap (For Formula Evaluation)
Why: HashMap (or JavaScript object) is used for storing cell formulas and their dependencies. This allows efficient lookup of formula references and ensures formulas are recalculated when dependent cells are updated.
How: Each formula refers to a cell's coordinates (e.g., A1, B2), which are stored in a dictionary for efficient access and modification.
javascript
Copy code
let formulas = {
  'C1': {formula: '=SUM(A1:B1)', dependencies: ['A1', 'B1']},
  'D1': {formula: '=AVERAGE(A1:B1)', dependencies: ['A1', 'B1']}
};
3. Stacks (For Undo/Redo Functionality)
Why: A stack is used to keep track of cell states for undo/redo functionality.
How: Every time a user makes an edit to a cell (text or formula), the previous state is pushed onto a stack. If the user wants to undo the change, the last state can be popped from the stack.
javascript
Copy code
let undoStack = [];
let redoStack = [];

// Save current state to undo stack
undoStack.push(currentState);
Why These Technologies and Data Structures?
HTML/CSS/JavaScript: These are the most suitable technologies for a web-based spreadsheet application. HTML provides the structure, CSS ensures a user-friendly UI, and JavaScript enables dynamic interactions and the implementation of complex logic like cell dependencies and calculations.

2D Array: A 2D array is an intuitive choice for representing the grid because each element corresponds directly to a cell in the spreadsheet. Operations such as adding rows/columns, updating cell values, and applying formulas are simplified using a 2D array structure.

HashMap: Storing formulas and their dependencies in a HashMap allows for efficient lookups and updates when a formula needs to be recalculated due to changes in dependent cells. This structure ensures that the formulas remain accurate and up-to-date.

Stacks: The stack-based approach for undo and redo allows users to efficiently revert or reapply changes. This is especially important in applications like spreadsheets, where users often need to modify data frequently and may want to undo or redo actions.

