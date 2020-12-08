import React, { Component } from "react";

class AddOffering extends Component {

	constructor(props) {
        super(props);

        this.state = {
            showCourseForm: true,
			showOfferingForm: false,
			showConfirmationForm: false,
			course_name: '',
			course_number: '',
			offering_ID: '',
			offering_number: '',
			offering_capacity: '',
			offering_start_time: '',
			offering_end_time: '',
			offering_room_ID: ''
        }

        this.onClickCourse = this.onClickCourse.bind(this);
        this.onClickOffering = this.onClickOffering.bind(this);
        this.onClickConfirm = this.onClickConfirm.bind(this);
        this.handleField = this.handleField.bind(this);
    }

    onClickCourse() {
        this.setState({ showCourseForm: true});
        this.setState({ showOfferingForm: false});
        this.setState({ showConfirmationForm: false});
    }

    onClickOffering() {
        this.setState({ showCourseForm: false});
        this.setState({ showOfferingForm: true});
        this.setState({ showConfirmationForm: false});
	}

	onClickConfirm() {
        this.setState({ showCourseForm: false});
        this.setState({ showOfferingForm: false});
        this.setState({ showConfirmationForm: true});
	}

	handleField(event, field) {
		this.setState({[field]: event.target.value});
	}

    chooseCourse () {
        return (
            <>
                <h1>Choose a Course</h1>
				<input type="text" value={this.state.value} name="courseName" placeholder="Course Name" onChange={(event)=>this.handleField(event, "course_name")}></input>
				<br></br>
				<input type="text" value={this.state.value} name="courseNumber" placeholder="Course ID" onChange={(event)=>this.handleField(event, "course_number")}></input>
				<br></br>
				<button onClick={ this.onClickOffering }>Submit</button>
            </>
        )
    }

    addOffering () {
        return (
            <>
				<h1>Course Information</h1>
				<p> Course Name: { this.state.course_name } </p>
				<p> Course ID: { this.state.course_number } </p>

                <h1>Add Offering</h1>
				<input type="text" name="offeringID" placeholder="Offering ID" onChange={(event)=>this.handleField(event, "offering_ID")}></input>
				<br></br>
				<input type="text" name="offeringNumber" placeholder="Offering Number" onChange={(event)=>this.handleField(event, "offering_number")}></input>
				<br></br>
				<input type="text" name="offeringCap" placeholder="Offering Capacity" onChange={(event)=>this.handleField(event, "offering_capacity")}></input>
				<br></br>
				<input type="text" name="offeringDay" placeholder="Offering Day" onChange={(event)=>this.handleField(event, "offering_day")}></input>
				<br></br>
				<input type="text" name="offeringStartTime" placeholder="Offering Start Time" onChange={(event)=>this.handleField(event, "offering_start_time")}></input>
				<br></br>
				<input type="text" name="offeringEndTime" placeholder="Offering End Time" onChange={(event)=>this.handleField(event, "offering_end_time")}></input>
				<br></br>
				<input type="text" name="roomID" placeholder="Offering Room ID" onChange={(event)=>this.handleField(event, "offering_room_ID")}></input>
				<br></br>
				<button onClick={ this.onClickConfirm }>Create Offering</button>
            </>
        )
	}
	
	confirmCourse () {
		return (
            <>
				<h1>Course Information</h1>
				<p> Course Name: { this.state.course_name } </p>
				<p> Course ID: { this.state.course_number } </p>

                <h1>Offering Information</h1>
				<p> Offering ID: { this.state.offering_ID } </p>
				<p> Offering Number: { this.state.offering_number } </p>
				<p> Offering Capacity: { this.state.offering_capacity } </p>
				<p> Offering Start Time: { this.state.offering_start_time } </p>
				<p> Offering End Time: { this.state.offering_end_time } </p>
				<p> Offering Room ID: { this.state.offering_room_ID } </p>
				
				<button onClick={ this.onClickCourse }>Confirm</button>
            </>
        )
	}
	
	render() {
		const { showCourseForm } = this.state;
        const { showOfferingForm } = this.state;
        const { showConfirmationForm } = this.state;
		return (
			<>
				{showCourseForm && this.chooseCourse()}
                {showOfferingForm && this.addOffering()}
                {showConfirmationForm && this.confirmCourse()}
			</>
		);
	}
}

export default AddOffering;