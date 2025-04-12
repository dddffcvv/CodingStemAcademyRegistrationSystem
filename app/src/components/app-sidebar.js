"use client"

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarHeader, SidebarMenu, SidebarMenuButton, SidebarMenuItem,
} from "@/components/ui/sidebar"
import {
  User2,
  ChevronUp,
  Command
} from "lucide-react";
import {jwtDecode} from "jwt-decode";
import {useEffect, useState} from "react";
import {DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger} from "@/components/ui/dropdown-menu";
import {useRouter} from "next/router";
import {NavClasses} from "@/components/nav-classes";
import axios from "axios";
import config from "@/config";
import NavSecondary from "@/components/nav-secondary";
import {
  Sheet, SheetClose,
  SheetContent,
  SheetDescription,
  SheetFooter,
  SheetHeader,
  SheetTitle,
  SheetTrigger
} from "@/components/ui/sheet";
import {Label} from "@/components/ui/label";
import {Input} from "@/components/ui/input";
import {Button} from "@/components/ui/button";




export function AppSidebar({ ...props }) {
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState({});
  const [classes, setClasses] = useState([]);
  const router = useRouter()

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      const user = jwtDecode(token);
      console.log(user)
      setUser(user['sub']);
    } else {
      console.log("Token not found in local storage");
      window.location.href = "/";
    }
  }, []);

  useEffect(() => {
    const fetchClasses = async () => {
      axios.get(`${config.backendUrl}/all-classes-by-student`, {
        params : {
          student_id: user['id']
        },
      })
        .then((response) => {
          console.log(response.data);
          setClasses(response.data['classes']);
        })
        .catch((error) => {
          console.error("Error fetching classes:", error);
        });
    };

    const fetchClassesTeacher = async () => {
      console.log("Fetching classes for teacher");
      axios.get(`${config.backendUrl}/all-classes-by-teacher`, {
        params : {
          teacher_id: user['id']
        },
      })
        .then((response) => {
          console.log(response.data);
          setClasses(response.data['classes']);
        })
        .catch((error) => {
          console.error("Error fetching classes:", error);
        });
    }

    if (user['id']) {
      if (user['role'] === 'Student') {
        console.log("Fetching classes for student");
        fetchClasses().then(() => console.log("Fetched classes"));
      } else if (user['role'] === 'Teacher') {
        fetchClassesTeacher().then(() => console.log("Fetched classes for teacher"));
      }
      setLoading(false);
    }
  }, [user]);

  const handleSignOutClick = () => {
    localStorage.removeItem('token');
    router.push("/").then(() => console.log("Redirected to login page"));
  }

  return (
    <Sidebar className="top-[--header-height] !h-[calc(100svh-var(--header-height))]"
             {...props}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton size="lg" asChild>
              <a href="/dashboard">
                <div className="flex aspect-square size-8 items-center justify-center rounded-lg bg-sidebar-primary text-sidebar-primary-foreground">
                  <Command className="size-4" />
                </div>
                <div className="grid flex-1 text-left text-sm leading-tight">
                  <span className="truncate font-semibold">Coding Stem Academy</span>
                </div>
              </a>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        {loading ? (<span>Loading...</span>) :
          user["role"] !== 'Admin' ? (
          <NavClasses classes={classes} />
        ) : null }
        <NavSecondary />
      </SidebarContent>
      <SidebarFooter>
        <SidebarMenu>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <SidebarMenuButton>
                <User2 /> {user['first_name'] ? user['first_name'] + " " + user['last_name'] : "User"}
                <ChevronUp className="ml-auto" />
              </SidebarMenuButton>
            </DropdownMenuTrigger>
            <DropdownMenuContent
              side="top"
              className="w-[--radix-popper-anchor-width]"
            >
              <DropdownMenuItem>
                <span>Account</span>
              </DropdownMenuItem>
              <DropdownMenuItem>
                <span>Settings</span>
              </DropdownMenuItem>
              <DropdownMenuItem>
                <span>Billing</span>
              </DropdownMenuItem>
              <DropdownMenuItem
                onClick={handleSignOutClick}>
                <span>Sign out</span>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
)}
