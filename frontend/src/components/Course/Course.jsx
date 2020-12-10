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
		<div className="card h-100 bg-muted" style={{ width: "20rem" }}>
			<div className="card-body">
				<h5 className="card-title text-center">
					Course {course_id}: {course_name}
				</h5>
				<h5 className="text-muted font-weight-light">Offering: </h5>
				<ul className="list-group p-2">
					{offerings.map((offering) => (
						<li
							className="list-group-item text-muted"
							key={offering.offering_no}
						>
							{offering.offering_no}
						</li>
					))}
				</ul>
				<h5 className="text-muted font-weight-light">
					Prerequisites:{" "}
				</h5>
				<ul className="list-group p-2">
					{prerequisites.map((prerequisite) => (
						<li
							className="list-group-item text-muted"
							key={prerequisite.course_id}
						>
							{prerequisite.course_name}
						</li>
					))}
				</ul>
				<h5 className="text-muted font-weight-light">
					Course textbooks:
				</h5>
				<ul className="list-group p-2">
					{required_textbooks.map((required_textbook) => (
						<li
							className="list-group-item text-muted"
							key={required_textbook.isbn}
						>
							<span>{required_textbook.isbn}</span>{" "}
							<span>{required_textbook.title}</span>
						</li>
					))}
				</ul>
			</div>
		</div>
	);
}

export default Course;
