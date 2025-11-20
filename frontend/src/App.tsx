import './App.css'
import AppLayout from '@/components/layout/AppLayout'

import { ThemeProvider } from "@/components/theme-provider"

function App() {
  return (
    <ThemeProvider defaultTheme="system" storageKey="vite-ui-theme">
      <AppLayout />
    </ThemeProvider>
  )
}

export default App
