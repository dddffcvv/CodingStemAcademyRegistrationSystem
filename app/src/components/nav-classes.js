"use client"

import {
  SidebarGroup,
  SidebarGroupLabel,
  SidebarMenu, SidebarMenuAction,
  SidebarMenuButton,
  SidebarMenuItem, SidebarMenuSub, SidebarMenuSubButton
} from "@/components/ui/sidebar";
import {ChevronRight} from "lucide-react";
import {Collapsible, CollapsibleContent, CollapsibleTrigger} from "@/components/ui/collapsible";

const options = [
  { label: 'Assignments', value: '/assignments' },
  { label: 'Grades', value: '/grades' },
  { label: 'Contact', value: '/contact' },
];



export function NavClasses({ classes }) {
  return (
    <SidebarGroup>
      <SidebarGroupLabel>
        <span> Classes</span>
      </SidebarGroupLabel>
      <SidebarMenu>
        {classes.map((classItem) => (
          <Collapsible key={classItem['id']} href={`/classes/${classItem['id']}`}>
            <SidebarMenuItem>
              <SidebarMenuButton asChild tooltip={classItem['class_name']}>
                <a href={`/classes/${classItem['id']}`}>
                  <span>
                    {classItem['class_name']}
                  </span>
                </a>
              </SidebarMenuButton>
              {options.length ? (
                <>
                  <CollapsibleTrigger asChild>
                    <SidebarMenuAction className="data-[state=open]:rotate-90">
                      <ChevronRight />
                      <span className="sr-only">Toggle</span>
                    </SidebarMenuAction>
                  </CollapsibleTrigger>
                  <CollapsibleContent>
                    <SidebarMenuSub>
                      {options.map((option) => (
                        <SidebarMenuItem key={option.value}>
                          <SidebarMenuSubButton asChild>
                            <a href={`/classes/${classItem['id']}${option.value}`}>
                              {option.label}
                            </a>
                          </SidebarMenuSubButton>
                        </SidebarMenuItem>
                      ))}
                    </SidebarMenuSub>
                  </CollapsibleContent>
                </>
              ) : null}
            </SidebarMenuItem>
          </Collapsible>
        ))}
      </SidebarMenu>
    </SidebarGroup>
  );
}
