import React, { useState } from 'react';
import axios from 'axios';
import config from '../config';


function SignUp() {
    
      
    const [formData, setFormData] = useState({ 

        teacher_id: '',
        subject: '',
        semester_id: '',
        class_name: '',

    });

    const handleSubmit = (e) => {
        e.preventDefault();
    
        axios.post(`${config.backendUrl}/add_class`, {
          formData['teacher_id'],
          formData.subject,
          formData.semester_id,
          formData.class_name
        }).then(response => {
          console.log("Successfully added class: " + response.data['message']);
        }).catch( error => {
          console.log(error);
        });
    };


    return (
        <div className="signup-container">
            <form className="signup-form" onSubmit={handleSubmit}>
                <input
                    type="text"
                    name="teacher_id"
                    value={formData.teacher_id}
                    onChange={handleChange}
                    placeholder="Teacher ID"
                />3
                <br />
                <input
                    type="text"
                    name="class_name"
                    value={formData.class_name}
                    onChange={handleChange}
                    placeholder="Class Name"
                />
                <br />
                <input
                    type="text"
                    name="subject"
                    value={formData.subject}
                    onChange={handleChange}
                    placeholder="Subject"
                />
                <br />
                <input
                    type="text"
                    name="semester_id"
                    value={formData.semester_id}
                    onChange={handleChange}
                    placeholder="Semester_ID"
                />
                <button type="submit">Sign Up</button>
            </form>
        </div>
    )
}

export default SignUp;