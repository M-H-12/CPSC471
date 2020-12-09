import React, { useState } from "react";
import axios from "axios";

function LoginLogout(props) {
	const [sinValue, setSIN] = useState("");
	const [passwordValue, setPassword] = useState("");

	const handleLogin = (e) => {
		e.preventDefault();
		axios
			.post("login/", {
				content: { sin: sinValue, password: passwordValue },
				withCredentials: true,
			})
			.then((response) => console.log(response.data));
	};

	const handleLogout = (e) => {
		e.preventDefault();
		axios.get("logout/").then((response) => console.log(response.data));
	};

	return (
		<div className="container p-4 App">
			<h1 className="pb-3">Main Page</h1>
			<input
				value={sinValue}
				onInput={(e) => setSIN(e.target.value)}
				placeholder="SIN"
			></input>
			<br></br>
			<br />
			<input
				value={passwordValue}
				onInput={(e) => setPassword(e.target.value)}
				placeholder="Password"
			></input>
			<br></br>
			<br></br>
			<button onClick={handleLogin}>Login</button>
			<br></br>
			<br></br>
			<button onClick={handleLogout}>Logout</button>
		</div>
	);
}

export default LoginLogout;
