import { UserContext } from "./UserContext";
import type { ReactNode } from "react";

interface Props {
  userId: string;
  children: ReactNode;
}

export const UserProvider = ({ userId, children }: Props) => (
  <UserContext.Provider value={{ userId }}>
    {children}
  </UserContext.Provider>
);
