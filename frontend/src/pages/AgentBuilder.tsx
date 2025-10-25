import { useState } from 'react'
import { Save, Bot } from 'lucide-react'
import { toast } from 'sonner'
// Update the import path below to match the actual location and filename (case-sensitive)
import PersonaSection from '../components/AgentBuilder/PersonaSection'
// For example, if the file is named 'personaSection.tsx', use:
// import PersonaSection from '../components/AgentBuilder/personaSection'
// Update the import path below to match the actual location and filename (case-sensitive)
import DocumentsSection from '../components/AgentBuilder/DocumentsSection'
import EndpointsSection from '../components/AgentBuilder/EndpointsSection'

export default function AgentBuilder() {
  const [activeTab, setActiveTab] = useState<'persona' | 'documents' | 'endpoints'>('persona')
  // Define types for agentData
  type PersonaType = {
    role: string
    tone: string
    instructions: string
    constraints: string
  }

  type DocumentType = {
      id: string
      name: string
      content: string
      type: string
      size: number
      status: string
      uploadedAt: string
    }

  type Endpoint = {
    id: string
    name: string
    description: string
    url: string
    method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH'
    requestExample: string
    responseExample: string
  }

  const [agentData, setAgentData] = useState<{
    name: string
    description: string
    persona: PersonaType
    documents: DocumentType[]
    endpoints: Endpoint[]
  }>({
    name: '',
    description: '',
    persona: {
      role: '',
      tone: '',
      instructions: '',
      constraints: '',
    },
    documents: [],
    endpoints: [],
  })

  const tabs = [
    { id: 'persona', name: 'Persona & Instructions', icon: Bot },
    { id: 'documents', name: 'Documents', icon: 'FileText' },
    { id: 'endpoints', name: 'API Endpoints', icon: 'Code' },
  ]

  const handleSave = async () => {
    try {
      // API call will be added here
      toast.success('Agent saved successfully!')
    } catch (error) {
      toast.error('Failed to save agent')
    }
  }

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Agent Builder</h1>
          <p className="mt-2 text-gray-600">
            Create an intelligent agent for your SaaS product
          </p>
        </div>
        <button
          onClick={handleSave}
          className="btn btn-primary flex items-center space-x-2"
        >
          <Save className="w-5 h-5" />
          <span>Save Agent</span>
        </button>
      </div>

      {/* Basic Info */}
      <div className="card">
        <div className="space-y-4">
          <div>
            <label className="label">Agent Name</label>
            <input
              type="text"
              className="input"
              placeholder="e.g., Analytics Pro Support Agent"
              value={agentData.name}
              onChange={(e) => setAgentData({ ...agentData, name: e.target.value })}
            />
          </div>
          <div>
            <label className="label">Description</label>
            <textarea
              className="input"
              rows={3}
              placeholder="Brief description of what this agent does"
              value={agentData.description}
              onChange={(e) => setAgentData({ ...agentData, description: e.target.value })}
            />
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="flex space-x-8">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === tab.id
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              {tab.name}
            </button>
          ))}
        </nav>
      </div>

      {/* Tab Content */}
      <div>
        {activeTab === 'persona' && (
          <PersonaSection
            data={agentData.persona}
            onChange={(persona: PersonaType) => setAgentData({ ...agentData, persona })}
          />
        )}
        {activeTab === 'documents' && (
            <DocumentsSection
            documents={agentData.documents}
            onChange={(documents: DocumentType[]) => setAgentData({ ...agentData, documents })}
          />
        )}
        {activeTab === 'endpoints' && (
          <EndpointsSection
            endpoints={agentData.endpoints}
            onChange={(endpoints) => setAgentData({ ...agentData, endpoints })}
          />
        )}
      </div>
    </div>
  )
}
