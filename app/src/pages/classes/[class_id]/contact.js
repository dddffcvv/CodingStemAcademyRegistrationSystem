import {Layout} from "@/app/layout";
import React, { useEffect, useState } from 'react';
import {Card, CardContent, CardDescription, CardHeader, CardTitle} from "@/components/ui/card";
import {useRouter} from "next/router";
import axios from "axios";
import config from "@/config";

export default function Grades() {
  const router = useRouter();
  const { class_id } = router.query;
  const [teacherData, setTeacherData] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchClassData = async () => {
      axios.get(`${config.backendUrl}/get-teacher-by-class`, {
        params : {
          class_id: class_id
        }
      })
        .then(response => {
          console.log("Teacher data retrieved: ", response.data);
          setTeacherData(response.data['teacher']);
        })
        .catch(error => {
          console.error("Error fetching class data:", error);
        });
    };

    if (class_id) {
      console.log("Fetching class data for class_id: ", class_id)
      fetchClassData().then(r => console.log("Fetched class data"))
        .catch(error => {
          console.error("Error fetching class data:", error);
        });
    }
  }, [class_id])

  useEffect(() => {
    if (teacherData !== {}) {
      console.log("Teacher data fetched successfully");
      setLoading(false);
    }
  }, [teacherData]);

  return (
    <>
    {loading ? <p>loading</p> : (
    <Layout title={"Teacher Contact Information"}>
      <div className="flex flex-1 flex-col gap-4 p-4">
        <div className="grid auto-rows-min gap-4 md:grid-cols-3">
          <Card className={"p-4"}>
            <CardHeader>
              <CardTitle>
                Teacher Contact Information
              </CardTitle>
              <CardDescription>Contact {teacherData['first_name']} {teacherData['last_name']} here</CardDescription>
            </CardHeader>
            <CardContent classname={"grid gap-4"}>
              <div className=" flex flex-col items-center space-y-4">
                <p>Email: {teacherData.email}</p>
                <p>Phone: {teacherData.phone}</p>
              </div>
            </CardContent>
          </Card>
        </div>
        <div className="min-h-[100vh] flex-1 rounded-xl bg-muted/50 md:min-h-min" />
      </div>
    </Layout>
      )}
    </>
  );
}
