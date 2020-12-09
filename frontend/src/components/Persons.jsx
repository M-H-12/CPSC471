import React from "react";
import Students from "./Student/Students";
import Teachers from "./Teacher/Teachers";
import Counselors from "./Counselor/Counselors";
import Admins from "./Admin/Admins";

function Persons(props) {
	return (
		<>
			<h3 className="text-center pt-4">Students</h3>
			<Students />
			<h3 className="text-center pt-2">Admins</h3>
			<Admins />
			<h3 className="text-center pt-2">Teachers</h3>
			<Teachers />
			<h3 className="text-center pt-2">Counselors</h3>
			<Counselors />
		</>
	);
}

export default Persons;
