import {Layout} from "@/app/layout";
import React, { useEffect, useState } from 'react';
import {Card} from "@/components/ui/card";
import {useRouter} from "next/router";
import axios from "axios";
import { jwtDecode } from "jwt-decode";
import {Table, TableBody, TableCell, TableHead, TableHeader, TableRow} from "@/components/ui/table";
import config from "@/config";

export default function Grades() {
  const router = useRouter();
  const { class_id } = router.query;
  const [submissions, setSubmissions] = useState([]);
  const [assignments, setAssignments] = useState([]);
  const [scores, setScores] = useState([]);
  const [user, setUser] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/').then(() => {console.log("Returning logged out user to main")})
    }
    const user = jwtDecode(token);
    setUser(user['sub']);
  }
  , []);

  useEffect(() => {
    // Fetch assignment information (Assignments) here using Axios
    
    
  }, [class_id]);

  useEffect(() => {
    // Fetch Submissions and Scores here using Axios
   

  }, [assignments]);


  // Your Code here
  return (
    <Layout title={"Grades"}>
      <div className="flex flex-1 flex-col gap-4 p-4">
        
      </div>
    </Layout>
  );
}
