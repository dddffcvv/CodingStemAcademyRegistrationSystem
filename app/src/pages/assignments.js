import React, { useState, useEffect } from 'react';
import {useRouter} from "next/router";
import axios from "axios";
import {jwtDecode} from "jwt-decode";
import config from "../config";
import Link from "next/link";


export default function Assignments() {
  const [assignments, setAssignments] = useState([]);
  const [classes, setClasses] = useState([]);
  const [user, setUser] = useState({});
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/');
      return
    }
    const decoded = jwtDecode(token);
    setUser(decoded['sub']);
  }, [])

  useEffect(() => {
    const fetchClasses = async () => {
      try {
        if (user['role'] === 'Teacher') {
          fetchClassesForTeacher()
            .then(() => {
              console.log("Classes fetched successfully", assignments);
            })
            .catch(() => {
              console.error("Error fetching classes");
            })
        } else if (user['role'] === 'Student') {
          fetchClassesForStudent()
            .then(() => {
              console.log("Classes fetched successfully: ", assignments);
            })
            .catch((error) => {
              console.error("Error fetching classes:", error);
            });
        }
      } catch (error) {
        console.error("Error fetching assignments:", error);
      }
    };

    const fetchClassesForStudent = async () => {
      console.log("Fetching classes for student", user['id'])
      const response = await axios.get(`${config.backendUrl}/classes/${user['id']}`)
      for (let i = 0; i < response.data['classes'].length; i++) {
        const classId = response.data['classes'][i]['id'];
        console.log("Class ID:", classId);
        await setAssignments((prevAssignments => [...prevAssignments, {classId: classId, assignments: []}]));
        await setClasses((prevClasses => [...prevClasses, classId]));
      }
    }

    const fetchClassesForTeacher = async () => {
      console.log("Fetching classes for teacher", user['id'])
      const response =
        await axios.get(`${config.backendUrl}/classes/teacher/${user['id']}`)
      console.log("Classes fetched successfully:", response.data);
      for (let i = 0; i < response.data['classes'].length; i++) {
        const classId = response.data['classes'][i]['id'];
        console.log("Class ID:", classId);
        await setAssignments((prevAssignments => [...prevAssignments, {classId: classId, assignments: []}]));
        await setClasses((prevClasses => [...prevClasses, classId]));
      }

    }

    fetchClasses().then(() => {
      console.log("Classes fetched successfully");
    })
      .catch(() => {
        console.error("Error fetching classes");
      });
  }, [user])

  useEffect(() => {
    const fetchAssignments = async () => {
      for (let i = 0; i < assignments.length; i++) {
        const classId = assignments[i]['classId'];
        const assignmentsResponse = await axios.get(`${config.backendUrl}/assignments`, {
          params: {
            'class_id': classId
          }
        });
        setAssignments((prevAssignments => {
          const updatedAssignments = [...prevAssignments];
          updatedAssignments[i]['assignments'] = assignmentsResponse.data['assignments'];
          return updatedAssignments;
        }));
      }
    }

    fetchAssignments()
      .then(() => {
        console.log("Assignments fetched successfully");
      })
      .catch(() => {
        console.error("Error fetching assignments");
      });
  }, [classes]);

  return (
    <div>
      <h1>Assignments</h1>
      <br />
      {assignments.map((assignment, index) => (
        <div key={index}>
          <h2>Class ID: {assignment.classId}</h2>
          <ul>
            {assignment.assignments.map((item, i) => (
              <li key={i}>
                <strong>Description:</strong> {item.description} |
                <strong>Due Date:</strong> {item.due_date}
              </li>
            ))}
          </ul>
        </div>
      ))}
      {user['role'] === "Teacher" && (
        <div>
          <h2>Quick Links</h2>
          <Link href="/create-assignment">Create Assignment</Link>
          <br />
          <Link href="/update-assignment">Update Assignment</Link>
          <br />
          <Link href="/delete-assignment">Delete Assignment</Link>
        </div>
      )}
    </div>
  );
}
