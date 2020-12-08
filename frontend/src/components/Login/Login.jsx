import React, { Component } from "react";

class Login extends Component {
	render() {
		return (
			<>
				<h1>Main Page</h1>
				<input type="number" name="user_id" placeholder="ID"></input>
				<br></br>
				<br></br>
				<input type="password" name="password" placeholder="Password"></input>
				<br></br>
				<br></br>
				<button>login</button>
			</>
		);
	}
}

export default Login;