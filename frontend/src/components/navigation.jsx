import React from "react";
import { Link } from 'react-router-dom';

function Navigation(props) {
	return (
		<>
		    <nav>
                <h1>Admin</h1>
                <ul>
                    <Link to='create_course'>
                        <p>Create Course</p>
                    </Link>
                    <Link to='add_student'>
                        <p>Add Student</p>
                    </Link>
                    <Link to='add_staff'>
                        <p>Add Staff</p>
                    </Link>
                </ul>
            </nav>
		</>
	);
}

export default Navigation;