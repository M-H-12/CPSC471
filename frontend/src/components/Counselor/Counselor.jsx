import React from "react";

function Counselor(props) {
	const {
		sin,
		name,
		gender,
		id,
		salary,
		hired_date,
		counsels,
		office_hours,
	} = props;

	return (
		<div className="card h-100" style={{ width: "18rem" }}>
			<div className="card-body">
				<h5 className="card-title">{name}</h5>
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
				<h5 className="text-muted font-weight-light">Counsels: </h5>
				<div>
					{counsels.map((student) => (
						<ul key={student.sin}>
							<h5 className="text-muted font-weight-light">
								{student.name}
							</h5>
						</ul>
					))}
				</div>
				<h5 className="text-muted font-weight-light">Office Hours: </h5>
				<div>
					{office_hours.map((office_hour) => (
						<ul>
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

export default Counselor;
