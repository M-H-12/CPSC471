import React, { useState, useEffect } from "react";
import axios from "axios";
import Admin from "./Admin";

function Admins(props) {
	const [isLoading, setLoading] = useState(true);
	const [allAdmins, setAllAdmins] = useState();

	useEffect(() => {
		axios.get("api/getAllAdmins/").then((response) => {
			setAllAdmins(response.data.response);
			setLoading(false);
		});
	}, []);

	if (isLoading) {
		return <div>Loading...</div>;
	}

	return (
		<div className="container p-3">
			<div className="row row-cols-1 row-cols-md-2 row-cols-lg-3">
				{allAdmins.map((admin) => (
					<div key={admin.sin} className="col mb-4">
						<Admin {...admin} />
					</div>
				))}
			</div>
		</div>
	);
}

export default Admins;
