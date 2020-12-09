import React from "react";

function Course(props) {
	const {
		course_id,
		course_name,
		offerings,
		prerequisites,
		required_textbooks,
	} = props;

	return (
		<div className="card h-100" style={{ width: "18rem" }}>
			<div className="card-body">
				<h5 className="card-title">{course_id}</h5>
				<h5 className="card-title">{course_name}</h5>
				<p className="card-text">Offering: </p>
				<div>
					{offerings.map((offering) => (
						<ul key={offering.offering_no}>
							{offering.offering_no}
						</ul>
					))}
				</div>
				<p className="card-text">Prerequisites: </p>
				<div>
					{prerequisites.map((prerequisite) => (
						<ul key={prerequisite.course_id}>
							{prerequisite.course_name}
						</ul>
					))}
				</div>
				<p className="card-text">Course textbooks: </p>
				<div>
					{required_textbooks.map((required_textbook) => (
						<ul key={required_textbook.isbn}>
							<span>{required_textbook.isbn}</span>{" "}
							<span>{required_textbook.title}</span>
						</ul>
					))}
				</div>
			</div>
		</div>
	);
}

export default Course;
