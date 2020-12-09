import React from "react";

function Admin(props) {
	const { sin, name, gender, id, salary, hired_date, position_title } = props;

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
				<h5 className="text-muted font-weight-light">
					Position Title:{" " + position_title}
				</h5>
				{/* <h5 className="text-muted font-weight-light">
					{position_title}
				</h5> */}
			</div>
		</div>
	);
}

export default Admin;
