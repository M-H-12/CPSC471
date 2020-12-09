import React, { useState, useEffect } from "react";
import axios from "axios";
import Course from "./Course";

function Courses(props) {
	const [isLoading, setLoading] = useState(true);
	const [allCourses, setAllCourses] = useState();

	useEffect(() => {
		axios.get("api/getAllCourses/").then((response) => {
			setAllCourses(response.data.response);
			setLoading(false);
		});
	}, []);

	if (isLoading) {
		return <div>Loading...</div>;
	}

	return (
		<div className="container p-3">
			<div className="row row-cols-1 row-cols-md-2 row-cols-lg-3">
				{allCourses.map((course) => (
					<div key={course.course_id} className="col mb-4">
						<Course {...course} />
					</div>
				))}
			</div>
		</div>
	);
}

export default Courses;
