import { useUser } from "@/context/useUser";

export default function Dashboard() {
  const { userId } = useUser();
  
  return (
    <p>Dashboard Page. User ID: {userId}</p>
  );
}