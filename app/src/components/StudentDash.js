import React, { useEffect, useState } from 'react';
import { jwtDecode } from 'jwt-decode';
import Link from "next/link";

const StudentDash = () => {
  const [user, setUser] = useState({});

  useEffect(() => {
    const token = localStorage.getItem('token');
    const user = jwtDecode(token);
    setUser(user['sub']);
  }, []);

  return (
    <div>
      <h1>Student Dashboard</h1>
      <p>Welcome, {user['first_name']} {user['last_name']}</p>
      <h2>Quick Links</h2>
      <Link href="/courses">View Courses</Link>
      <br />
      <Link href="/assignments">View Assignments</Link>
      <br />
      <Link href="/enroll">Enroll in a Course</Link>
      <br />
      <Link href="/calendar">View Calendar</Link>
      <br />
      <Link href="/grades">View Grades</Link>
    </div>
  );
}

export default StudentDash;
