import React, { useState } from "react"
import { format } from "date-fns"
import { CalendarIcon } from "lucide-react"
import axios from 'axios';
import config from '../config';
import { useRouter } from 'next/router';
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Calendar } from "@/components/ui/calendar"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"



export function DatePickerDemo() {
  const [date, setDate] = useState(0)

  return (
    <Popover>
      <PopoverTrigger asChild>
        <Button
          variant={"outline"}
          className={cn(
            "w-[280px] justify-start text-left font-normal",
            !date && "text-muted-foreground"
          )}
        >
          <CalendarIcon />
          {date ? format(date, "PPP") : <span>Pick a date</span>}
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-auto p-0">
        <Calendar
          mode="single"
          selected={date}
          onSelect={setDate}
          initialFocus
        />
      </PopoverContent>
    </Popover>
  )
}

export default function Register() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    birth_date: '',
    email: '',
    gender: '',
    phone: '',
    password: '',
    address: '',
    guardian: '',
    guardian_phone: '',
    health_ins: '',
    health_ins_number: '',
    role: 'Student',
    grade_level: '',
  });
  const [confirmPassword, setConfirmPassword] = useState('');
  const gradeLevels = Array.from({length: 12}, (_, i) => i + 1);

  function handleSignUp(e) {
    e.preventDefault();

    if (formData.password !== confirmPassword) {
      alert("Passwords do not match");
      return;
    }
    axios.post(`${config.backendUrl}/register`, formData).then(response => {
      console.log("Successfully registered: " + response.data['message']);
      if (response.data['access_token']) {
        localStorage.setItem('token', response.data['access_token']);
        router.push('/register-classes').then( () => console.log("Redirecting to register classes"));
      } else {
        throw new Error(response.data['message']);
      }
    }).catch( error => {
      console.log(error);
    });
  }

  function handleChange(e) {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  }

  return (
    <div>
      <h1>Register</h1>
      <form onSubmit={handleSignUp}>
        <input
          type="text"
          name="first_name"
          value={formData.first_name}
          onChange={handleChange}
          placeholder="First Name"
        />
       <br />
        <input
          type="text"
          name="last_name"
          value={formData.last_name}
          onChange={handleChange}
          placeholder="Last Name"
        />
        <br />
        <DatePickerDemo />
        <br />
        <select
          name="gender"
          value={formData.gender}
          onChange={handleChange}
        >
          <option value="">Gender</option>
          <option key="Male" value="Male">
            Male
          </option>
          <option key="Female" value="Female">
            Female
          </option>
          <option key="Other" value="Other">
            Other
          </option>
        </select>
        <br />
        <input
          type="text"
          name="phone"
          value={formData.phone}
          onChange={handleChange}
          placeholder="Phone"
          />
        <br />
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          placeholder="Email"
          />
        <br />
        <input
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          placeholder="Password"
          />
        <br />
        <input
          type="password"
          name="confirm_password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          placeholder="Confirm Password"
          />
        <br />
        <input
          type="text"
          name="address"
          value={formData.address}
          onChange={handleChange}
          placeholder="Address"
          />
        <br />
        <input
          type="text"
          name="guardian"
          value={formData.guardian}
          onChange={handleChange}
          placeholder="Guardian Name"
          />
        <br />
        <input
          type="text"
          name="guardian_phone"
          value={formData.guardian_phone}
          onChange={handleChange}
          placeholder="Guardian Phone"
          />
        <br />
        <input
          type="text"
          name="health_ins"
          value={formData.health_ins}
          onChange={handleChange}
          placeholder="Health Insurance"
          />
        <br />
        <input
          type="text"
          name="health_ins_number"
          value={formData.health_ins_number}
          onChange={handleChange}
          placeholder="Health Insurance Number"
          />
        <br />
        <select
          name="grade_level"
          value={formData.grade_level}
          onChange={handleChange}
          >
          <option value="">Select Grade Level</option>
          {gradeLevels.map((level) => (
            <option key={level} value={level}>
              {level}
            </option>
          ))}
        </select>
        <br />
        <button type="submit">Register</button>
      </form>
    </div>
  );
}
