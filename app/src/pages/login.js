import React, { useState } from 'react';
import { useRouter } from 'next/router';
import axios from 'axios';
import config from '../config';
import {cn} from "@/lib/utils";
import {Button} from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export default function login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const router = useRouter();

  const handleSubmit = (e) => {
    e.preventDefault();

    axios.post(`${config.backendUrl}/login`, {
      email,
      password
    }).then(response => {
      console.log("Successfully logged in: " + response.data['message']);
      if (response.data['access_token']) {
        localStorage.setItem('token', response.data['access_token']);
        router.push('/dashboard').then( () => console.log("Redirecting to dashboard"));
      } else {
        throw new Error(response.data['message']);
      }
    }).catch( error => {
      console.log(error);
    });
  };

  return (
    <div className={"flex items-center justify-center h-screen"}>
      <Card>
        <CardHeader className="text-center">
           <CardTitle>Login</CardTitle>
            <CardDescription>
              Please login to your account
            </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit}>
            <div className="grid gap-6">
              <div className="grid gap-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="m@example.com"
                  required
                />
              </div>
              <div className="grid gap-2">
                <div className="flex items-center">
                  <Label htmlFor="password">Password</Label>
                </div>
                <Input id="password" type="password" required />
              </div>
            <Button type="submit" className="w-full">Login</Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
