import Link from "next/link";
import {useEffect, useState} from "react";
import { jwtDecode } from 'jwt-decode'
import StudentDash from "@/components/StudentDash";
import TeacherDash from "@/components/TeacherDash";
import AdminDash from "@/components/AdminDash";
import {Layout} from "@/app/layout";

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
      <Layout>
        {role === 'Student' && <StudentDash />}
        {role === 'Teacher' && <TeacherDash />}
        {role === 'Admin' && <AdminDash />}
      </Layout>
    </div>
  );
}
