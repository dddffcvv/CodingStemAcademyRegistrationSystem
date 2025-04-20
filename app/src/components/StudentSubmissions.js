import {useEffect, useState} from "react";
import {jwtDecode} from "jwt-decode";
import Link from "next/link";
import config from "@/config";
import axios from "axios";


export default function StudentSubmissions() {
  const [user, setUser] = useState({});
  const [submissions, setSubmissions] = useState([]);
  const [assignments, setAssignments] = useState([]);
  const [classes, setClasses] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      const decoded = jwtDecode(token);
      setUser(decoded['sub']);
    }
  }, []);

  useEffect(() => {
    const fetchSubmissions = async () => {
      try {
        const response = await axios.get(`${config.backendUrl}/student-submissions`, {
          params: {
            student_id: user['id'],
          }
        });
        const data = response.data;
        setClasses(data['classes']);
        setSubmissions(data['submissions']);
        setAssignments(data['assignments']);
        return data;
      } catch (error) {
        console.error('Error fetching submissions:', error);
      }
    };

    fetchSubmissions().then(r => { console.log("Submissions fetched successfully: ", r) });
  }, [user])

  return (
    <div>
      <h1>Student Submissions</h1>
      <p>This is the student submissions page.</p>
      <Link href="/create-submission">Create Submission</Link>
    </div>
  );
}
