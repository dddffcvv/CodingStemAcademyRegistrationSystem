import { useRouter } from 'next/router';
import {Layout} from "@/app/layout";
import {useEffect, useState} from "react";
import {jwtDecode} from "jwt-decode";
import axios from "axios";
import config from "@/config";
import {Card} from "@/components/ui/card";

const ClassPage = () => {
  const router = useRouter();
  const { assignment_id } = router.query; // Access the dynamic ID from the URL
  const [assignmentData, setAssignmentData] = useState({});
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
    // Fetch assignment information here using Axios 

  }, [assignment_id])

  // YOUR CODE HERE
  return (
    <Layout title={assignmentData.details}>
        
    </Layout>
  );
};

export default ClassPage;
