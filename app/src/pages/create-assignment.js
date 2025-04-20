import React, { useState, useEffect } from 'react';
import { useRouter } from "next/router";
import axios from "axios";
import { jwtDecode } from "jwt-decode";
import config from "../config";


export default function CreateAssignment() {
  const [user, setUser] = useState({});
  const [classes, setClasses] = useState([]);
  const [formData, setFormData] = useState({
    description: '',
    due_date: '',
    class_id: ''
  });
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/');
      return;
    }
    const decoded = jwtDecode(token);
    setUser(decoded['sub']);

    if (decoded['sub']['role'] !== 'Teacher') {
      router.push('/');
      return;
    }
    const fetchClasses = async () => {
      try {
        const response =
          await axios.get(`${config.backendUrl}/classes/teacher/${decoded['sub']['id']}`);
        setClasses(response.data['classes']);
        console.log("Classes fetched successfully:", response.data);
      } catch (error) {
        console.error("Error fetching classes:", error);
      }
    };
    fetchClasses().then(() => {
      console.log("Classes fetched successfully");
    });
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${config.backendUrl}/assignments`, formData);
      console.log("Assignment created successfully:", response.data);
      router.push('/assignments');
    } catch (error) {
      console.error("Error creating assignment:", error);
    }
  }

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <h1>Create Assignment</h1>
        <div>
          <label htmlFor="description">Description:</label>
          <input
            type="text"
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label htmlFor="due_date">Due Date:</label>
          <input
            type="date"
            id="due_date"
            name="due_date"
            value={formData.due_date}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label htmlFor="class_id">Class ID:</label>
          <select
            id="class_id"
            name="class_id"
            value={formData.class_id}
            onChange={handleChange}
            required
          >
            <option value="">Select a class</option>
            {classes.map((item) => (
              <option key={item.id} value={item.id}>{item.id} {item.class_name}</option>
            ))}
          </select>
        </div>
        <button type="submit">Create Assignment</button>
      </form>
    </div>
  );
}
