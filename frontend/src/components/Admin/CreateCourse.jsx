import React from "react";

function CreateCourse(props) {
	return (
		<>
		    <h1>Create Course</h1>
			<input type="text" name="name" placeholder="Course Name"></input>
            <br></br>
			<input type="text" name="number" placeholder="Course Number"></input>
			<br></br>
			<button>Create Course</button>
		</>
	);
}

export default CreateCourse;