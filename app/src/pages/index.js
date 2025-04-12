import Link from "next/link";
import React, {useEffect} from "react";
import {Card, CardContent, CardDescription, CardHeader, CardTitle} from "@/components/ui/card";
import {Button} from "@/components/ui/button";

export default function Home() {

  useEffect (() => {
    if (localStorage.getItem('token')) {
      console.log("Token found in local storage");
      window.location.href = "/dashboard";
    }
  }, []);

  return (
    <div className={"flex items-center justify-center h-screen"}>
      <Card className={"w-[350px]"}>
        <CardHeader className="text-center">
          <CardTitle className="text-4xl">Stem Coding Academy</CardTitle>
          <CardDescription>
            Where learning meets innovation
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className={"flex flex-row gap-4 justify-center"}>
            <Button asChild>
              <Link href={"/login"}>Login</Link>
            </Button>
            <span>or</span>
            <Button asChild>
              <Link href={"/register"}>Register</Link>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
