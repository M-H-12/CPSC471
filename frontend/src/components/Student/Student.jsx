import React from "react";

function Student(props) {
	const {
		sin,
		name,
		gender,
		id,
		year,
		grade_average,
		credits_received,
		signed_out_textbooks,
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
					{"Year: " + year}
				</h5>
				<h5 className="text-muted font-weight-light">
					{"GPA: " + grade_average}
				</h5>
				<h5 className="text-muted font-weight-light">
					{"Credits Received: " + credits_received}
				</h5>
				<h5 className="card-text text-muted font-weight-light">
					Course textbooks:{" "}
				</h5>
				<div>
					{signed_out_textbooks.map((signed_out_textbook) => (
						<ul key={signed_out_textbook.isbn}>
							<span>{signed_out_textbook.isbn}</span>{" "}
							<span>{signed_out_textbook.title}</span>
						</ul>
					))}
				</div>
			</div>
		</div>
	);
}

export default Student;
