import React from 'react';
import { useState, useEffect } from 'react';
import axios from 'axios';
import config from '../config';
import { useRouter } from 'next/router';
import { jwtDecode } from 'jwt-decode';

export default function CoursesPage() {
  const [classes, setClasses] = useState([]);
  const [user, setUser] = useState({});

  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      window.location.href = '/';
      return;
    }
    const decodedUser = jwtDecode(token);
    setUser(decodedUser['sub']);
  }, []);

  useEffect(() => {
    // TODO: Show Admin all teacher classes and their information
    if (user['role'] === 'Student') {
      axios.get(`${config.backendUrl}/all-classes-by-student`, {
        params: {
          student_id: user['id']
        }
      }).then(response => {
        console.log(response.data['classes'])
        setClasses(response.data['classes']);
      }).catch(error => {
        console.log(error);
      });
    } else if (user['role'] === 'Teacher') {
      axios.get(`${config.backendUrl}/all-classes-by-teacher`, {
        params: {
          teacher_id: user['id']
        }
      }).then(response => {
        console.log(response.data)
        setClasses(response.data['classes']);
      }).catch(error => {
        console.log(error);
      });
    }
  }, [user])

  return (
    <div className="courses-container">
      <h1>Courses</h1>
      <p>Welcome to the Courses page!</p>
      {user && user['role'] === 'Student' ? (
        <div>
          <h2>Your Classes</h2>
          { classes.length > 0 && (
          <ul>
            {classes.map((classItem) => (
              <li key={classItem['id']}>
                <h3>{classItem['class_name']}</h3>
                <p>Subject: {classItem['subject']}</p>
                <p>Semester: {classItem['semester_id']}</p>
              </li>
            ))}
          </ul>
          )}
          { classes.length === 0 && <p>You are not enrolled in any classes.</p>}
        </div>
      ) : user && user['role'] === 'Teacher' ? (
        <div>
          <h2>Your Classes</h2>
          <ul>
            {classes.map((classItem) => (
              <li key={classItem['id']}>
                <h3>{classItem['class_name']}</h3>
                <p>Subject: {classItem['subject']}</p>
                <p>Semester: {classItem['semester_id']}</p>
              </li>
            ))}
            {classes.length === 0 && <p>You are not teaching any classes.</p>}
          </ul>
        </div>
      ) : (
        <p>You are not authorized to view this page.</p>
      )}
    </div>
  );
}
