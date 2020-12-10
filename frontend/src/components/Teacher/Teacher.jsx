import React from "react";

function Teacher(props) {
	const {
		sin,
		name,
		gender,
		id,
		salary,
		hired_date,
		can_teach,
		office_hours,
	} = props;

	return (
		<div className="card h-100" style={{ width: "20rem" }}>
			<div className="card-body">
				<h4 className="card-title text-center">{name}</h4>
				<h5 className="text-muted font-weight-light">{"ID: " + sin}</h5>
				<h5 className="text-muted font-weight-light">
					{"Gender: " + gender}
				</h5>
				<h5 className="text-muted font-weight-light">
					{"Salary: " + salary}
				</h5>
				<h5 className="text-muted font-weight-light">
					Hired Date: {hired_date}
				</h5>
				<h5 className="text-muted font-weight-light">Can Teach: </h5>
				<ul className="list-group p-2">
					{can_teach.map((course) => (
						<li
							className="list-group-item text-muted"
							key={course.course_id}
						>
							{course.course_name}
						</li>
					))}
				</ul>
				<h5 className="text-muted font-weight-light">Office Hours: </h5>
				<ul className="list-group p-2">
					{office_hours.map((office_hour) => (
						<li className="list-group-item text-muted">
							{office_hour.day +
								", " +
								office_hour.hour_from +
								"-" +
								office_hour.hour_to}
						</li>
					))}
				</ul>
			</div>
		</div>
	);
}

export default Teacher;
