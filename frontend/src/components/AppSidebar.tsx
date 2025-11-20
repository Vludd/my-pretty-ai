import { NavLink } from "react-router-dom";

import { 
  Sidebar, 
  SidebarContent, 
  SidebarFooter, 
  SidebarHeader, 
} from "@/components/ui/sidebar";

import { navGroups } from "@/data/appSidebarItems";
import NavMain from "./sidebar/NavMain";
import NavUser from "./sidebar/NavUser";

export default function AppSidebar() {

  return (
    <Sidebar>
      <SidebarHeader className="flex flex-row items-center justify-between m-2">
        <NavLink to="/" className="font-bold cursor-pointer">MyPrettyAI</NavLink>
      </SidebarHeader>
      
      <SidebarContent>
        <NavMain navGroups={navGroups}/>
      </SidebarContent>
      
      <SidebarFooter>
        <NavUser />
      </SidebarFooter>
    </Sidebar>
  );
}
