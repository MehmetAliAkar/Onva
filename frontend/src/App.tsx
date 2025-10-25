import { Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard.tsx'
// import AgentBuilder from './pages/AgentBuilder'
// Update the import path below to match the actual file name and extension, e.g.:
import AgentBuilder from './pages/AgentBuilder.tsx'
// or, if the file is named agentBuilder.tsx or Agentbuilder.tsx, update accordingly:
// import AgentBuilder from './pages/agentBuilder'
// import AgentBuilder from './pages/Agentbuilder'
import Agents from './pages/Agents.tsx'

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/agents" element={<Agents />} />
        <Route path="/agents/new" element={<AgentBuilder />} />
        <Route path="/agents/:id/edit" element={<AgentBuilder />} />
      </Routes>
    </Layout>
  )
}

export default App
