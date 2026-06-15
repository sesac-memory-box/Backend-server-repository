import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { AppProvider } from '@/store/useStore'
import HomePage from '@/pages/HomePage'
import ChatPage from '@/pages/ChatPage'
import GuardianInfoPage from '@/pages/GuardianInfoPage'
import SummaryPage from '@/pages/SummaryPage'
import HistoryPage from '@/pages/HistoryPage'

function App() {
  return (
    <AppProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/guardian-info" element={<GuardianInfoPage />} />
          <Route path="/summary" element={<SummaryPage />} />
          <Route path="/history" element={<HistoryPage />} />
        </Routes>
      </BrowserRouter>
    </AppProvider>
  )
}

export default App
