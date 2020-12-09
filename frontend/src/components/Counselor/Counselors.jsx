import React, { useState, useEffect } from "react";
import axios from "axios";
import Counselor from "./Counselor";

function Counselors(props) {
	const [isLoading, setLoading] = useState(true);
	const [allCounselors, setAllCounselors] = useState();

	useEffect(() => {
		axios.get("api/getAllCounselors/").then((response) => {
			setAllCounselors(response.data.response);
			setLoading(false);
		});
	}, []);

	if (isLoading) {
		return <div>Loading...</div>;
	}

	return (
		<div className="container p-3">
			<div className="row row-cols-1 row-cols-md-2 row-cols-lg-3">
				{allCounselors.map((counselor) => (
					<div key={counselor.sin} className="col mb-4">
						<Counselor {...counselor} />
					</div>
				))}
			</div>
		</div>
	);
}

export default Counselors;
