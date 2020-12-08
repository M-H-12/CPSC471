import React, { Component } from "react";

class AddStaff extends Component {

    constructor(props) {
        super(props);

        this.state = {
            showTeacherForm: false,
            showCounselorForm: false,
            showAdminForm: false
        }

        this.onClickTeacher = this.onClickTeacher.bind(this);
        this.onClickCounselor = this.onClickCounselor.bind(this);
        this.onClickAdmin = this.onClickAdmin.bind(this);
    }

    onClickTeacher() {
        this.setState({ showTeacherForm: true});
        this.setState({ showCounselorForm: false});
        this.setState({ showAdminForm: false});
    }

    onClickCounselor() {
        this.setState({ showTeacherForm: false});
        this.setState({ showCounselorForm: true});
        this.setState({ showAdminForm: false});
    }

    onClickAdmin() {
        this.setState({ showTeacherForm: false});
        this.setState({ showCounselorForm: false});
        this.setState({ showAdminForm: true});
    }

    addTeacher () {
        return (
            <>
                <input type="text" name="name" placeholder="Teacher Name"></input>
                <br></br>
                <input type="text" name="gender" placeholder="Gender"></input>
                <br></br>
                <input type="text" name="sin" placeholder="SIN"></input>
                <br></br>
                <input type="text" name="id" placeholder="Staff ID"></input>
                <br></br>
                <input type="text" name="password" placeholder="Password"></input>
                <br></br>
                <input type="text" name="salary" placeholder="Salary"></input>
                <br></br>
                <p>Hire Date: </p>
                <input type="text" name="day" placeholder="Day"></input>
                <input type="text" name="month" placeholder="Month"></input>
                <input type="text" name="year" placeholder="Year"></input>
                <br></br>
                <button>Add Staff</button>
            </>
        )
    }

    addCounselor () {
        return (
            <>
                <input type="text" name="name" placeholder="Counselor Name"></input>
                <br></br>
                <input type="text" name="gender" placeholder="Gender"></input>
                <br></br>
                <input type="text" name="sin" placeholder="SIN"></input>
                <br></br>
                <input type="text" name="id" placeholder="Staff ID"></input>
                <br></br>
                <input type="text" name="password" placeholder="Password"></input>
                <br></br>
                <input type="text" name="salary" placeholder="Salary"></input>
                <br></br>
                <p>Hire Date: </p>
                <input type="text" name="day" placeholder="Day"></input>
                <input type="text" name="month" placeholder="Month"></input>
                <input type="text" name="year" placeholder="Year"></input>
                <br></br>
                <button>Add Staff</button>
            </>
        )
    }

    addAdmin () {
        return (
            <>
                <input type="text" name="name" placeholder="Admin Name"></input>
                <br></br>
                <input type="text" name="gender" placeholder="Gender"></input>
                <br></br>
                <input type="text" name="sin" placeholder="SIN"></input>
                <br></br>
                <input type="text" name="id" placeholder="Staff ID"></input>
                <br></br>
                <input type="text" name="password" placeholder="Password"></input>
                <br></br>
                <input type="text" name="salary" placeholder="Salary"></input>
                <br></br>
                <p>Hire Date: </p>
                <input type="text" name="day" placeholder="Day"></input>
                <input type="text" name="month" placeholder="Month"></input>
                <input type="text" name="year" placeholder="Year"></input>
                <br></br>
                <button>Add Staff</button>
            </>
        )
    }

    render() {
        const { showTeacherForm } = this.state;
        const { showCounselorForm } = this.state;
        const { showAdminForm } = this.state;
        return (
            <>
                <h1>Add Staff</h1>
                <button onClick={ this.onClickTeacher }>Add Teacher</button>
                <button onClick={ this.onClickCounselor }>Add Counselor</button>
                <button onClick={ this.onClickAdmin }>Add Admin</button>
                <br></br>

                {showTeacherForm && this.addTeacher()}
                {showCounselorForm && this.addCounselor()}
                {showAdminForm && this.addAdmin()}
            </>
        );
    }
}

export default AddStaff;