import React from "react";

function AddStudent(props) {
	return (
		<>
		    <h1>Add Student</h1>
			<input type="text" name="name" placeholder="Name"></input>
			<br></br>
			<input type="text" name="gender" placeholder="Gender"></input>
			<br></br>
			<input type="text" name="sin" placeholder="SIN"></input>
			<br></br>
			<input type="text" name="id" placeholder="Student ID"></input>
			<br></br>
			<input type="password" name="password" placeholder="Password"></input>
			<br></br>
			<input type="text" name="year" placeholder="Grade Level"></input>
			<br></br>
			<input type="text" name="credits" placeholder="Credits Received"></input>
			<br></br>
			<input type="text" name="gradeAvg" placeholder="Grade Average"></input>
			<br></br>
			<br></br>
			<button>Add Student</button>
		</>
	);
}

export default AddStudent;