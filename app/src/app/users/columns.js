"use client"
import { columnDefs } from "@tanstack/react-table";
import { MoreHorizontal } from "lucide-react" 
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

export const roles = ['Admin', 'Student', 'Teacher'];

export const columns = [
    {
        accessorKey: "role",
        header: "Role",
      },
      {
        accessorKey: "last_name",
        header: "Last Name",
      },
      {
        accessorKey: "first_name",
        header: "First Name",
      },
      {
        accessorKey: "email",
        header: "Email",
      },
      {
        accessorKey: "phone",
        header: "Phone",
      },
      {
        id: "actions",
        cell: ({ row }) => {
            const user = row.original;
            const userRole = user['role'];
            return (
                <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                        <Button variant="ghost" className="h-8 w-8 p-0">
                        <span className="sr-only">Open menu</span>
                        <MoreHorizontal className="h-4 w-4" />
                        </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                        <DropdownMenuLabel>Actions</DropdownMenuLabel>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem>View User's classes</DropdownMenuItem>
                        <DropdownMenuItem>Add User Classes</DropdownMenuItem>
                        <DropdownMenuItem>Edit User Information</DropdownMenuItem>
                        <DropdownMenuItem>Change User Role</DropdownMenuItem>
                        {userRole === 'Student' ? (
                            <DropdownMenuItem>View Payments</DropdownMenuItem>
                        ) : null}
                    </DropdownMenuContent>
                </DropdownMenu>
            )
        }
      }
]
