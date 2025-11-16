import type { UserContextType } from "@/types/UserContextType";
import { createContext } from "react";

export const UserContext = createContext<UserContextType | undefined>(undefined);
