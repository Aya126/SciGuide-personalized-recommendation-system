function gradeCalc(grade, unit) {
  if (grade === "A") {
    return 4.00 * unit;
  } else if (grade === "A-") {
    return 3.67 * unit;
  } else if (grade === "B+") {
    return 3.33 * unit;
  } else if (grade === "B") {
    return 3.00 * unit;
  } else if (grade === "B-") {
    return 2.67 * unit;
  } else if (grade === "C+") {
    return 2.33 * unit;
  }else if (grade === "C") {
    return 2.00 * unit;
  }else if (grade === "C-") {
    return 1.67 * unit;
  }else if (grade === "D+") {
    return 1.33 * unit;
  }else if (grade === "D") {
    return 1.00 * unit;
  }else if (grade === "F") {
    return 0 * unit;
  }
}

let counter = 1;

function addCourse() {
  let addNew = document.createElement("form");
  addNew.classList.add("add_new", `key-${counter}`);
  const course_name = `
  <form class="add_new key-${counter}">
    <input type="text" placeholder="Course Code" class="courses key-${counter}" required>
        <input type="number" placeholder="Credit Unit" class="credit-units key-${counter}" required>
        <select class="grade key-${counter}" required>
      <option value="select">Select</option>
      <option value="4.00">A</option>
      <option value="3.67">A-</option>
      <option value="3.33">B+</option>
      <option value="3.00">B</option>
      <option value="2.67">B-</option>
      <option value="2.33">C+</option>
      <option value="2.00">C</option>
      <option value="1.67">C-</option>
      <option value="1.33">D+</option>
      <option value="1.00">D</option>
      <option value="0">F</option>
    </select>  
  </form>
  `;
  addNew.innerHTML = course_name;
  document.getElementById("course-wrapper").appendChild(addNew);
  counter++;
}

function removeCourse() {
  let mainForm = document.querySelector("form.add_new");
  mainForm.remove();
}

const reports = [];

/**
 * @description calculates cgpa
 */
function calcCgpa() {
  const CGPAPARAGRAPH = document.getElementById("cgpa-calc");
  const GRADESSELECT = document.querySelectorAll("select.grade");
  const UNIT = document.querySelectorAll("input.credit-units");

  const courseReport = {};

  const listOfGrades = [];
  const listOfUnits = [];
  let totalUnits = 0;

  GRADESSELECT.forEach((e) => {
    let GRADES = e.options;
    const selectedIndex = e.selectedIndex;
    const selectedGrade = GRADES[selectedIndex];
    const gradeValue = selectedGrade.text.toUpperCase();
    listOfGrades.push(gradeValue);
  });
  console.log(listOfGrades);

  UNIT.forEach((e) => {
    const unitValue = parseInt(e.value);
    totalUnits += unitValue;
    listOfUnits.push(unitValue);
  });
  console.log(listOfUnits);

  let totalEarnedUnits = 0;

  for (let i = 0; i < listOfUnits.length; i++) {
    totalEarnedUnits += gradeCalc(listOfGrades[i], listOfUnits[i]);
  }
  const gpa = totalEarnedUnits / totalUnits;
  
  if (gpa >= 0){
    CGPAPARAGRAPH.textContent = "Your CGPA is " + gpa.toFixed(2);   
  } else {
    CGPAPARAGRAPH.textContent = "Please enter your correct grade and credit units";    
  }
  
}
