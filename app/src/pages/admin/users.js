import React, {useEffect} from 'react';
import {Layout} from "@/app/layout";
import {jwtDecode} from "jwt-decode";
import {useRouter} from "next/router";
import axios from "axios";
import config from "@/config";
import {DataTable} from "@/app/users/data-table";
import {columns} from "@/app/users/columns";


export default function Users() {
  const router = useRouter()
  const [users, setUsers] = React.useState([]);
  const [user, setUser] = React.useState({});
  const [loading, setLoading] = React.useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/').then(() => {
        console.log('Redirected to home page')
      })
    } else {
      const decodedToken = jwtDecode(token);
      setUser(decodedToken['sub']);
      console.log("Decoded token:", decodedToken);
    }
  }, []);

  useEffect(() => {
    const fetchUsers = async () => {
      axios.get(`${config.backendUrl}/users`)
        .then((response) => {
          console.log(response.data);
          setUsers(response.data['users']);
        })
        .catch((error) => {
          console.error("Error fetching users:", error);
        });
      }
    if (user['role'] === 'Admin') {
      console.log("Fetching users");
      fetchUsers().then(() => console.log("Fetched users"));
    }
    setLoading(false);
  }, [user])

  return (
    <Layout>
      <div className="container mx-auto p-12">
      {loading ? (
        <div className="flex items-center justify-center h-screen">
          <h1 className="text-3xl font-bold">Loading...</h1>
        </div>
      ) : user['role'] === 'Admin' ? (
        <DataTable columns={columns} data={users} />
      ) : (
        <div className="text-center">
          <h1 className="text-3xl font-bold">You are not authorized to view this page</h1>
        </div>
      )}
      </div>
    </Layout>
  );

}
