import React from "react";
import { Link } from 'react-router-dom';

function Navigation(props) {
	return (
		<>
		    <nav>
                <h1>Admin</h1>
                <ul>
                    <Link to='add_student'>
                        <p>Add Student</p>
                    </Link>
                    <Link to='add_staff'>
                        <p>Add Staff</p>
                    </Link>
                    <Link to='create_course'>
                        <p>Create Course</p>
                    </Link>
                    <Link to='add_offering'>
                        <p>Add Course Offering</p>
                    </Link>
                </ul>
            </nav>
		</>
	);
}

export default Navigation;