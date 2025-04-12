import React, { useState } from 'react';
import { useRouter } from 'next/router';
import axios from 'axios';
import config from '../config';
import {Button} from "@/components/ui/button";
import {Card, CardHeader, CardTitle, CardContent, CardDescription} from "@/components/ui/card";
import {Label} from "@/components/ui/label";
import {Input} from "@/components/ui/input";

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
    <div className="flex items-center justify-center h-screen">
      <Card>
        <CardHeader className="text-center">
          <CardTitle className="text-xl">Login</CardTitle>
          <CardDescription>
            Login with your email and password
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit}>
            <div className="grid gap-6">
              <div className="grid gap-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="email@example.com"
                  required
                />
              </div>
              <div className="grid gap-2">
                <div className="flex items-center">
                  <Label htmlFor="password">Password</Label>
                </div>
                <Input id="password" type="password" onChange={(e) => setPassword(e.target.value)} required />
              </div>
            <Button type="submit">Login</Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
