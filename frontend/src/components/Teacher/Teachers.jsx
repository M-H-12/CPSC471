import React, { useState, useEffect } from "react";
import axios from "axios";
import Teacher from "./Teacher";

function Teachers(props) {
	const [isLoading, setLoading] = useState(true);
	const [allTeachers, setAllTeachers] = useState();

	useEffect(() => {
		axios.get("api/getAllTeachers/").then((response) => {
			setAllTeachers(response.data.response);
			setLoading(false);
		});
	}, []);

	if (isLoading) {
		return <div>Loading...</div>;
	}

	return (
		<div className="container p-3">
			<div className="row row-cols-1 row-cols-md-2 row-cols-lg-3">
				{allTeachers.map((teacher) => (
					<div key={teacher.sin} className="col mb-4">
						<Teacher {...teacher} />
					</div>
				))}
			</div>
		</div>
	);
}

export default Teachers;
