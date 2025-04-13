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

  // YOUR CODE HERE
  return (
    <Layout title={classData.class_name}>
      
    </Layout>
  );
};

export default ClassPage;
