import { Footer } from "@/components/layout/Footer";
import { Header } from "@/components/layout/Header";
import { useUser } from "@/context/useUser";

export default function Dashboard() {
  const { userId } = useUser();
  
  return (
    <div className="p-2 min-h-screen flex flex-col">
      <Header>

        <p>Dashboard Page. User ID: {userId}</p>
      </Header>
      <main className="flex-1">

      </main>
      <Footer>
      </Footer>
    </div>
  )
}
