import { Bot, Plus, Settings } from 'lucide-react'
import { Link } from 'react-router-dom'
import { useState, useEffect } from 'react'
import AgentChat from '../components/AgentChat'
import { toast } from 'sonner'

export default function Agents() {
  const [selectedAgent, setSelectedAgent] = useState<any>(null)
  const [agents, setAgents] = useState<any[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    fetchAgents()
  }, [])

  const fetchAgents = async () => {
    try {
      setIsLoading(true)
      const response = await fetch('http://localhost:8000/api/v1/agents')
      
      if (!response.ok) {
        throw new Error('Failed to fetch agents')
      }

      const data = await response.json()
      setAgents(data)
    } catch (error) {
      console.error('Error fetching agents:', error)
      toast.error('Failed to load agents')
    } finally {
      setIsLoading(false)
    }
  }

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
      {isLoading ? (
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      ) : agents.length === 0 ? (
        <div className="text-center py-12">
          <Bot className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">No agents yet</h3>
          <p className="text-gray-600 mb-4">Create your first agent to get started</p>
          <Link to="/agents/new" className="btn btn-primary inline-flex items-center space-x-2">
            <Plus className="w-5 h-5" />
            <span>Create Agent</span>
          </Link>
        </div>
      ) : (
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
                <button
                  onClick={(e) => {
                    e.stopPropagation()
                    // Deploy logic here
                    console.log('Deploy agent:', agent.id)
                  }}
                  className="px-3 py-1 text-xs font-semibold text-purple-700 bg-purple-100 rounded-full border border-purple-200 hover:bg-purple-600 hover:text-white hover:border-purple-700 transition-all cursor-pointer shadow-sm hover:shadow-md active:scale-95"
                  title="Deploy Agent"
                >
                  {agent.status === 'active' ? 'deploy' : agent.status}
                </button>
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
                {agent.document_count || 0} docs
              </span>
              <span className="flex items-center gap-1">
                <span className="w-2 h-2 bg-purple-500 rounded-full"></span>
                {agent.endpoint_count || 0} endpoints
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
      )}

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
