import LoginLogout from "./components/Login/LoginLogout";
//import Navigation from "./components/Navigation";
import CreateCourse from "./components/Admin/CreateCourse";
import AddStudent from "./components/Admin/AddStudent";
import AddStaff from "./components/Admin/AddStaff";
import AddOffering from "./components/Admin/AddOffering";
//import TestingConnection from "./components/TestingConnection";
import Homepage from "./components/Homepage";
import Navbar from "./components/Navbar";
import Courses from "./components/Course/Courses";
import Persons from "./components/Persons";
import axios from "axios";

import { BrowserRouter as Router, Switch, Route } from "react-router-dom";

function App() {
	axios.defaults.baseURL = "http://127.0.0.1:8000/";
	axios.defaults.xsrfCookieName = "csrftoken";
	axios.defaults.xsrfHeaderName = "X-CSRFToken";
	//axios.defaults.withCredentials = true;

	// const content = {
	// 	sin: 0,
	// };

	// let temp;
	// axios.put("api/admin/", { content }).then((response) => {
	// 	temp = response.data;
	// 	console.log(temp);
	// });

	return (
		<Router>
			<Navbar />
			<Switch>
				<Route path="/" exact component={Homepage} />
				<Route path="/loginlogout" component={LoginLogout} />
				<Route path="/courses" component={Courses} />
				<Route path="/persons" component={Persons} />
				<Route path="/create_course" component={CreateCourse} />
				<Route path="/add_student" component={AddStudent} />
				<Route path="/add_staff" component={AddStaff} />
				<Route path="/add_offering" component={AddOffering} />
			</Switch>
		</Router>
	);

	// return (
	// 	<Router>
	// 		<Navbar />
	// 		<div className="App">
	// 			<TestingConnection />
	// 			<Navigation />
	// 			<Switch>
	// 				<Route path="/" exact component={Login} />
	// 				<Route path="/create_course" component={CreateCourse} />
	// 				<Route path="/add_student" component={AddStudent} />
	// 				<Route path="/add_staff" component={AddStaff} />
	// 				<Route path="/add_offering" component={AddOffering} />
	// 				<Route exact path="/login" component={Login} />
	// 			</Switch>
	// 		</div>
	// 	</Router>
	// );
}

export default App;
