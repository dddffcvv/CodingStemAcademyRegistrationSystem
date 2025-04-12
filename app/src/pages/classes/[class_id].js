import { useRouter } from 'next/router';
import {Layout} from "@/app/layout";
import {useEffect, useState} from "react";
import {jwtDecode} from "jwt-decode";
import axios from "axios";
import config from "@/config";
import {Card} from "@/components/ui/card";

const ClassPage = () => {
  const router = useRouter();
  const { class_id } = router.query; // Access the dynamic ID from the URL
  const [classData, setClassData] = useState({});
  const [user, setUser] = useState({});

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/').then(() => {console.log("Returning logged out user to main")})
    }
    const user = jwtDecode(token);
    setUser(user['sub']);
  }, []);

  useEffect(() => {
    const fetchClassData = async () => {
      axios.get(`${config.backendUrl}/class/${class_id}`)
        .then(response => {
          console.log(response.data);
          setClassData(response.data['class']);
        })
        .catch(error => {
          console.error("Error fetching class data:", error);
        });
    };

    if (class_id) {
      fetchClassData().then(r => console.log("Fetched class data"))
        .catch(error => {
          console.error("Error fetching class data:", error);
        });
    }
  }, [class_id])

  return (
    <Layout title={classData.class_name}>
      <div className="flex flex-1 flex-col gap-4 p-4">
        <h1 className="text-4xl font-bold mb-4">Class Details</h1>
        <Card className="grid grid-cols-1 md:grid-cols-2 p-4">
          <p>Course ID: {class_id}</p>
          <p>Semester ID: {classData.semester_id}</p>
          <p>Subject: {classData.subject}</p>
          <p>Teacher ID: {classData.teacher_id}</p>
        </Card>
      </div>
    </Layout>
  );
};

export default ClassPage;
