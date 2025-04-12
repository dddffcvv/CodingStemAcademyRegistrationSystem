import React, { useEffect, useState } from 'react';
import { jwtDecode } from 'jwt-decode';
import Link from "next/link";
import { useRouter } from 'next/router';
import {Button} from "@/components/ui/button";
import {Layout} from "@/app/layout";
import {Card, CardContent, CardHeader, CardTitle} from "@/components/ui/card";

const TeacherDash = () => {
  const [user, setUser] = useState({});
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('token');
    const user = jwtDecode(token);
    setUser(user['sub']);
  }, []);

  const logout = () => {
    localStorage.removeItem('token');
    router.push('/');
  }

  return (
    <div className="p-6 min-h-screen">
      <h1 className="text-4xl font-bold mb-4">Teacher Dashboard</h1>
      <div className="grid grid-cols-1 gap-4">
        <p>Welcome, {user['first_name']} {user['last_name']}</p>
        <Card>
          <CardHeader>
            <CardTitle>Quick Links</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="grid grid-cols-1 md:grid-cols-2 space-y-2">
              <Link href="/courses">View Courses</Link>
              <Link href="/assignments">View Assignments</Link>
              <Link href="/calendar">View Calendar</Link>
              <Link href="/grades">View Grades</Link>
            </ul>
          </CardContent>
        </Card>
        <Button onClick={() => {logout()} }>Logout</Button>
      </div>
    </div>
  );
}

export default TeacherDash;
