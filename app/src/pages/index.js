import Link from "next/link";
import {useEffect} from "react";

export default function Home() {

  useEffect (() => {
    if (localStorage.getItem('token')) {
      console.log("Token found in local storage");
      window.location.href = "/dashboard";
    }
  }, []);

  return (
    <div className="">
      <Link href="/login">Login</Link>
      <br />
      <Link href={"/register"}>Register</Link>
    </div>
  );
}
