import React, {useEffect, useState} from "react";
import {useRouter} from "next/router";
import {jwtDecode} from "jwt-decode";
import axios from "axios";
import config from "@/config";


export default function TeacherSubmissions() {
  const [classes, setClasses] = useState([]);
  const [assignments, setAssignments] = useState([]);
  const [submissions, setSubmissions] = useState([]);
  const [user, setUser] = useState(null);
  const router = useRouter();

  useEffect(() => {
    const fetchUser = async () => {
      const token = localStorage.getItem('token');
      if (!token) {
        console.log("Token not found in local storage");
        router.push("/").then(() => { console.log("Redirected to login page") });
      } else {
        try {
          const user = await jwtDecode(token);
          setUser(user['sub']);
        } catch (error) {
          console.error('Error decoding token:', error);
          router.push("/").then(() => { console.log("Redirected to login page") });
        }
      }
    };

    fetchUser().then(() => console.log("User fetched successfully: ", user));
  },[]);

  useEffect(() => {
    const fetchSubmissions = async () => {
      try {
        const response =
          await axios.get(`${config.backendUrl}/teacher-submissions`, {
            params: {
              teacher_id: user['id'],
            },
          });
        setClasses(response.data['classes']);
        setAssignments(response.data['assignments']);
        setSubmissions(response.data['submissions']);
        return response.data;
      } catch (error) {
        console.error('Error fetching classes:', error);
      }
    }

    if (user) {
      fetchSubmissions().then((response) => {
        console.log("Classes fetched successfully: ", response)
      });
    }
  }, [user])

  const printSubmissions = (index) => {
    const itemElements = [];
    for (let i = 0; i < submissions[index].length; i++) {
      itemElements.push(
        <div key={i}>
          <h4>{submissions[index][i]['student_id']}</h4>
          <p>{submissions[index][i]['submission']}</p>
        </div>
      );
    }

    return (
      <div>
        {itemElements}
      </div>
    )
  }


  const printAssignments = (index) => {
    const itemElements = [];
    for (let i = 0; i < assignments[index].length; i++) {
      itemElements.push(
        <div key={i}>
          {assignments[i].map((assignment, j) => (
            <div key={j}>
              <p>{assignment['description']}</p>
              <p>Due Date: {assignment['due_date']}</p>
              <h4>Submissions:</h4>
              {printSubmissions(j)}
            </div>
          ))}
        </div>
      );
    }

    return (
      <div>
        {itemElements}
      </div>
    )
  }

  const PrintClasses = () => {
    const classElements = []
    for (let i = 0; i < classes.length; i++) {
      classElements.push(
        <div key={i}>
          <h2>{classes[i]['class_name']}</h2>
          {printAssignments(i)}
        </div>
      );
    }

    return (
      <div>
        {classElements}
      </div>
    )
  }

  return (
    <div>
      <h1>Submissions</h1>
      <p>This is the submissions page.</p>
      <p>Here you can view all the submissions made by students.</p>
      { classes.length > 0 && (
        <PrintClasses />
      )}
    </div>
  );
}
