import React, {useEffect, useState} from 'react';
import axios from 'axios';
import config from '../config';
import {jwtDecode} from "jwt-decode";
import {useRouter} from "next/router";

export default function RegisterClasses() {
  const [classes, setClasses] = useState([]);
  const [selectedClasses, setSelectedClasses] = useState([]);

  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      window.location.href = '/';
      return;
    }
    const user = jwtDecode(token);
    if (user['sub']['role'] !== 'Student') {
      alert("You are not authorized to access this page");
      return;
    }

    axios.get(`${config.backendUrl}/classes`).then(response => {
      setClasses(response.data['classes']);
    }).catch(error => {
      console.log(error);
    });
  }, []);

  const handleClick = () => {
    const token = localStorage.getItem('token');
    const user = jwtDecode(token);
    const student_id = user['sub']['id'];
    console.log("Student ID: " + student_id);
    console.log("Selected Classes: " + selectedClasses);

    console.log("Registering for classes: " + selectedClasses + " for student: " + student_id)
    axios.post(`${config.backendUrl}/add_multiple_classes_to_student`, {
      user_id: student_id,
      classes: selectedClasses,
    }).then(response => {
      console.log("Successfully registered for class: " + response.data['message']);
      if (response.data['message'] === 'Student already registered for this class') {
        alert("You are already registered for this class");
      } else {
        console.log("Successfully registered for class: " + response.data['message']);
        router.push('/dashboard').then(() => console.log("Redirecting to dashboard"));
      }
    }).catch(error => {
      console.log(error);
    });
  }

  const handleCheckboxChange = (classId) => {
    setSelectedClasses(prevSelectedClasses => {
      if (prevSelectedClasses.includes(classId)) {
        return prevSelectedClasses.filter(id => id !== classId);
      } else {
        return [...prevSelectedClasses, classId];
      }
    });
  };

  return (
    <div>
      <h1>Available Classes</h1>
      <ul>
        {classes.map((classItem) => (
          <li key={classItem.id}>
            <label>
              <input
                type="checkbox"
                checked={selectedClasses.includes(classItem.id)}
                onChange={() => handleCheckboxChange(classItem.id)}
              />
              {classItem.class_name}
            </label>
          </li>
        ))}
      </ul>
      <br />
      <button onClick={() => handleClick()}>Register Classes</button>
    </div>
  );
}
