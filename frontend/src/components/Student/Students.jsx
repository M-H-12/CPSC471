import React, { useState, useEffect } from "react";
import axios from "axios";
import Student from "./Student";

function Students(props) {
	const [isLoading, setLoading] = useState(true);
	const [allStudents, setAllStudents] = useState();

	useEffect(() => {
		axios.get("api/getAllStudents/").then((response) => {
			setAllStudents(response.data.response);
			setLoading(false);
		});
	}, []);

	if (isLoading) {
		return <div>Loading...</div>;
	}

	return (
		<div className="container p-3">
			<div className="row row-cols-1 row-cols-md-2 row-cols-lg-3">
				{allStudents.map((student) => (
					<div key={student.sin} className="col mb-4">
						<Student {...student} />
					</div>
				))}
			</div>
		</div>
	);
}

export default Students;
