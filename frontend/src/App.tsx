import './App.css'
import ChatPage from './pages/ChatPage'

import { ThemeProvider } from "@/components/theme-provider"

function App() {
  return (
    <ThemeProvider defaultTheme="system" storageKey="vite-ui-theme">
      <ChatPage userId="c602e0b8-464c-431e-a5aa-f6098d27defb" conversationId="773dce58-e040-41f3-b29c-40218d9d6390" />
    </ThemeProvider>
  )
}

export default App
