import './App.css'
import ChatPage from './pages/ChatPage'

import { ThemeProvider } from "@/components/theme-provider"

function App() {
  return (
    <ThemeProvider defaultTheme="system" storageKey="vite-ui-theme">
      <ChatPage userId="c602e0b8-464c-431e-a5aa-f6098d27defb" conversationId="99b5a593-8fe9-4aac-9d7b-f8f6b3b25ed6" />
    </ThemeProvider>
  )
}

export default App
