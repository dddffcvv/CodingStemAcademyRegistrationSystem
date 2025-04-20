import React, { useEffect, useState } from 'react';
import { jwtDecode } from 'jwt-decode';
import Link from "next/link";
import {Card, CardContent, CardHeader, CardTitle} from "@/components/ui/card";
import {Button} from "@/components/ui/button";

const AdminDash = () => {
  const [user, setUser] = useState({});

  useEffect(() => {
    const token = localStorage.getItem('token');
    const user = jwtDecode(token);
    setUser(user['sub']);
  }, []);

  return (
    <div>
      <div className="p-6 min-h-screen">
        <h1 className="text-4xl font-bold mb-4">Admin Dashboard</h1>
        <div className="grid grid-cols-1 gap-4">
          <p>Welcome, {user['first_name']} {user['last_name']}</p>
          <Card>
            <CardHeader>
              <CardTitle>Quick Links</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="grid grid-cols-1 md:grid-cols-2 space-y-2">
                <Link href="/admin/classes">Manage classes</Link>
                <Link href="/admin/assignments">Manage Assignments</Link>
                <Link href="/calendar">View Calendar</Link>
                <Link href="/admin/grades">View Grades</Link>
                <Link href="/admin/payments">Manage Payments</Link>
                <Link href="/admin/users">Manage Users</Link>
              </ul>
            </CardContent>
          </Card>
        </div>

      </div>
    </div>
  );
}

export default AdminDash;
