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
		<div className="card h-100" style={{ width: "18rem" }}>
			<div className="card-body">
				<h4 className="card-title text-center">{name}</h4>
				<h5 className="text-muted font-weight-light">
					{"SIN: " + sin}
				</h5>
				<h5 className="text-muted font-weight-light">
					{"Gender: " + gender}
				</h5>
				<h5 className="text-muted font-weight-light">
					{"Salary: " + salary}
				</h5>
				<h5 className="text-muted font-weight-light">Hired Date: </h5>
				<h5 className="text-muted font-weight-light">{hired_date}</h5>
				<h5 className="text-muted font-weight-light">Can Teach: </h5>
				<div>
					{can_teach.map((course) => (
						<ul key={course.course_id}>{course.course_name}</ul>
					))}
				</div>
				<h5 className="text-muted font-weight-light">Office Hours: </h5>
				<div>
					{office_hours.map((office_hour) => (
						<ul className="text-muted font-weight-light">
							{office_hour.day +
								", " +
								office_hour.hour_from +
								"-" +
								office_hour.hour_to}
						</ul>
					))}
				</div>
			</div>
		</div>
	);
}

export default Teacher;
