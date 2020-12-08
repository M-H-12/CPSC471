import logo from "./logo.svg";
import "./App.css";
import Test from "./components/Test";
import Login from "./components/Login/Login";
import Navigation from "./components/navigation";
import CreateCourse from "./components/Admin/CreateCourse";
import AddStudent from "./components/Admin/AddStudent";
import AddStaff from "./components/Admin/AddStaff";

import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

function App() {
	return (
		<Router>
		    <div className="App">
				<Navigation />
				<Switch>
					{/*<Route path="/" exact component={Login} />*/}
					<Route path="/create_course" component={CreateCourse} />
					<Route path="/add_student" component={AddStudent} />
					<Route path="/add_staff" component={AddStaff} />
				</Switch>
			</div>
		</Router>
	);
}

export default App;
