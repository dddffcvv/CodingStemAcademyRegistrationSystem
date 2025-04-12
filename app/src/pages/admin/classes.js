// File: `app/src/pages/admin/classes.js`
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import config from '@/config';
import {Layout} from "@/app/layout";

const ManageClasses = () => {
  const [classes, setClasses] = useState([]);
  const [newClass, setNewClass] = useState('');
  const [editingClass, setEditingClass] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch classes from the backend
    axios.get(`${config.backendUrl}/classes`)
      .then(response => {
        setClasses(response.data['classes']);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching classes:', error);
        setLoading(false);
      });
  }, []);

  const handleAddClass = () => {
    if (!newClass.trim()) return;

    const classData = { name: newClass };
    axios.post(`${config.backendUrl}/classes`, classData)
      .then(response => {
        setClasses([...classes, response.data]);
        setNewClass('');
      })
      .catch(error => console.error('Error adding class:', error));
  };

  const handleEditClass = (id, name) => {
    setEditingClass({ id, name });
  };

  const handleUpdateClass = () => {
    if (!editingClass.name.trim()) return;

    axios.put(`${config.backendUrl}/classes/${editingClass.id}`, { name: editingClass.name })
      .then(() => {
        setClasses(classes.map(cls =>
          cls.id === editingClass.id ? { ...cls, name: editingClass.name } : cls
        ));
        setEditingClass(null);
      })
      .catch(error => console.error('Error updating class:', error));
  };

  const handleDeleteClass = (id) => {
    axios.delete(`${config.backendUrl}/classes/${id}`)
      .then(() => {
        setClasses(classes.filter(cls => cls.id !== id));
      })
      .catch(error => console.error('Error deleting class:', error));
  };

  if (loading) return <p>Loading...</p>;

  return (
    <Layout>
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-4">Manage Classes</h1>
      <Card className="mb-6">
        <CardHeader>
          <CardTitle>Add New Class</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex gap-4">
            <Input
              value={newClass}
              onChange={(e) => setNewClass(e.target.value)}
              placeholder="Class Name"
            />
            <Button onClick={handleAddClass}>Add</Button>
          </div>
        </CardContent>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>Existing Classes</CardTitle>
        </CardHeader>
        <CardContent>
          <table className="w-full border-collapse border border-gray-300">
            <thead>
            <tr>
              <th className="border border-gray-300 p-2">ID</th>
              <th className="border border-gray-300 p-2">Name</th>
              <th className="border border-gray-300 p-2">Actions</th>
            </tr>
            </thead>
            <tbody>
            {classes.map(cls => (
              <tr key={cls.id}>
                <td className="border border-gray-300 p-2">{cls.id}</td>
                <td className="border border-gray-300 p-2">
                  {editingClass?.id === cls.id ? (
                    <Input
                      value={editingClass.name}
                      onChange={(e) => setEditingClass({ ...editingClass, name: e.target.value })}
                    />
                  ) : (
                    cls.name
                  )}
                </td>
                <td className="border border-gray-300 p-2">
                  {editingClass?.id === cls.id ? (
                    <Button onClick={handleUpdateClass} className="mr-2">Save</Button>
                  ) : (
                    <Button onClick={() => handleEditClass(cls.id, cls.name)} className="mr-2">Edit</Button>
                  )}
                  <Button onClick={() => handleDeleteClass(cls.id)} variant="destructive">Delete</Button>
                </td>
              </tr>
            ))}
            </tbody>
          </table>
        </CardContent>
      </Card>
    </div>
    </Layout>
  );
};

export default ManageClasses;
