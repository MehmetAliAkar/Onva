import { Bot, Plus, Settings } from 'lucide-react'
import { Link } from 'react-router-dom'
import { useState } from 'react'
import AgentChat from '../components/AgentChat'

export default function Agents() {
  const [selectedAgent, setSelectedAgent] = useState<any>(null)

  // Placeholder data - will be replaced with API data
  const agents = [
    {
      id: 1,
      name: 'Analytics Pro Agent',
      description: 'Helps customers understand analytics features',
      status: 'active',
      documents: 12,
      endpoints: 8,
      createdAt: '2025-10-20',
    },
    {
      id: 2,
      name: 'CRM Support Agent',
      description: 'Assists with CRM integration and setup',
      status: 'active',
      documents: 8,
      endpoints: 15,
      createdAt: '2025-10-18',
    },
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Agents</h1>
          <p className="mt-2 text-gray-600">
            Manage your AI agents
          </p>
        </div>
        <Link
          to="/agents/new"
          className="btn btn-primary flex items-center space-x-2"
        >
          <Plus className="w-5 h-5" />
          <span>New Agent</span>
        </Link>
      </div>

      {/* Agents Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {agents.map((agent) => (
          <div
            key={agent.id}
            className="card hover:shadow-xl transition-all duration-300 cursor-pointer group"
            onClick={() => setSelectedAgent(agent)}
          >
            <div className="flex items-start justify-between mb-4">
              <div className="p-2 bg-gradient-to-br from-primary-100 to-primary-200 rounded-lg group-hover:scale-110 transition-transform">
                <Bot className="w-6 h-6 text-primary-600" />
              </div>
              <div className="flex items-center gap-2">
                <span className="px-3 py-1 text-xs font-semibold text-green-700 bg-green-100 rounded-full border border-green-200">
                  {agent.status}
                </span>
                <Link
                  to={`/agents/${agent.id}/edit`}
                  onClick={(e) => e.stopPropagation()}
                  className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
                  title="Agent Settings"
                >
                  <Settings className="w-4 h-4 text-gray-500 hover:text-primary-600" />
                </Link>
              </div>
            </div>
            
            <h3 className="text-lg font-semibold text-gray-900 mb-2 group-hover:text-primary-600 transition-colors">
              {agent.name}
            </h3>
            <p className="text-sm text-gray-600 mb-4">
              {agent.description}
            </p>
            
            <div className="flex items-center justify-between text-sm text-gray-500 pt-4 border-t border-gray-100">
              <span className="flex items-center gap-1">
                <span className="w-2 h-2 bg-blue-500 rounded-full"></span>
                {agent.documents} docs
              </span>
              <span className="flex items-center gap-1">
                <span className="w-2 h-2 bg-purple-500 rounded-full"></span>
                {agent.endpoints} endpoints
              </span>
            </div>

            <div className="mt-4 pt-4 border-t border-gray-100">
              <p className="text-xs text-gray-500 text-center">
                Click to chat with agent
              </p>
            </div>
          </div>
        ))}
      </div>

      {/* Chat Modal */}
      {selectedAgent && (
        <AgentChat
          agent={selectedAgent}
          onClose={() => setSelectedAgent(null)}
        />
      )}
    </div>
  )
}
