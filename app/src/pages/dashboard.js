import Link from "next/link";
import {useEffect, useState} from "react";
import { jwtDecode } from 'jwt-decode'
import StudentDash from "@/components/StudentDash";
import TeacherDash from "@/components/TeacherDash";

export default function Dashboard() {
  const [role, setRole] = useState('');


  useEffect(() => {
    const fetchRole = async () => {
      const token = localStorage.getItem('token');
      if (!token) {
        console.log("Token found in local storage");
        window.location.href = "/";
      } else {
        const user = await jwtDecode(token);
        console.log(user['sub']);
        setRole(user['sub']['role']);
      }
    };

    fetchRole().then(() => console.log("Role set"));
  }, []);

  return (
    <div>
      {role === 'Student' && <StudentDash />}
      {role === 'Teacher' && <TeacherDash />}
      {role === 'Admin' && <h1>Admin Dashboard</h1>}
    </div>
  );
}
