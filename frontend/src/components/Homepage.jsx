import React from "react";

function Homepage(props) {
	return (
		<>
			<img
				className="img-fluid"
				style={{ maxWidth: "100%", height: "auto" }}
				src="https://school.cbe.ab.ca/School/Repository/SBPictureLibrary/c31a5631-4fb5-466c-b2f2-4d06b47a8eb1_20200123-ALP-PLP-Sports-Day-Robert-Thirsk.jpg"
				alt="homepage banner"
			/>
			<div className="container p-4">
				<div className="row justify-content-center pt-3">
					<h1 className="display-3 text-center">
						Learning Management and Student Information System
					</h1>
				</div>
			</div>
		</>
	);
}

export default Homepage;
