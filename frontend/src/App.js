import "./App.css";
import Login from "./components/Login/Login";
import Navigation from "./components/Navigation";
import CreateCourse from "./components/Admin/CreateCourse";
import AddStudent from "./components/Admin/AddStudent";
import AddStaff from "./components/Admin/AddStaff";
import AddOffering from "./components/Admin/AddOffering";
import TestingConnection from "./components/TestingConnection";

import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

function App() {
	return (
		<Router>
		    <div className="App">
				<TestingConnection />
				<Navigation />
				<Switch>
					<Route path="/" exact component={Login} />
					<Route path="/create_course" component={CreateCourse} />
					<Route path="/add_student" component={AddStudent} />
					<Route path="/add_staff" component={AddStaff} />
					<Route path="/add_offering" component={AddOffering} />
				</Switch>
			</div>
		</Router>
	);
}

export default App;
