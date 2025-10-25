import { Bot, Plus } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function Agents() {
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
          <Link
            key={agent.id}
            to={`/agents/${agent.id}/edit`}
            className="card hover:shadow-md transition-shadow"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="p-2 bg-primary-100 rounded-lg">
                <Bot className="w-6 h-6 text-primary-600" />
              </div>
              <span className="px-2 py-1 text-xs font-medium text-green-700 bg-green-100 rounded-full">
                {agent.status}
              </span>
            </div>
            
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              {agent.name}
            </h3>
            <p className="text-sm text-gray-600 mb-4">
              {agent.description}
            </p>
            
            <div className="flex items-center justify-between text-sm text-gray-500">
              <span>{agent.documents} docs</span>
              <span>{agent.endpoints} endpoints</span>
            </div>
          </Link>
        ))}
      </div>
    </div>
  )
}
