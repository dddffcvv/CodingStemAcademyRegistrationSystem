import React, { useState } from 'react';
import { useRouter } from 'next/router';
import axios from 'axios';
import config from '../config';

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
    <div>
      <h1>Login</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <br />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <br />
        <button type="submit">Login</button>
      </form>
    </div>
  )
}
