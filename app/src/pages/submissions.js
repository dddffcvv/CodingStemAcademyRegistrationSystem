import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { jwtDecode } from 'jwt-decode';
import config from '../config';
import axios from "axios";
import TeacherSubmissions from "@/components/TeacherSubmissions";
import StudentSubmissions from "@/components/StudentSubmissions";


export default function Submissions() {
  const [user, setUser] = useState({});

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      const decoded = jwtDecode(token);
      setUser(decoded['sub']);
    }
  }, []);

  return (
    <div>
      {user && user['role'] === 'Student' ? (
        <StudentSubmissions />
      ) : user && user['role'] === 'Teacher' ? (
        <TeacherSubmissions />
      ) : (
        <div>
          <h1>Submissions</h1>
          <p>You do not have permission to view this page.</p>
        </div>
      )}
    </div>
  )
}
