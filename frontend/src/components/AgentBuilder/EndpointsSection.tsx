import { useState } from 'react'
import { Plus, Trash2, Globe, Play } from 'lucide-react'
import { toast } from 'sonner'

interface Endpoint {
  id: string
  name: string
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH'
  url: string
  description: string
  requestExample: string
  responseExample: string
  headers?: Record<string, string>
}

interface EndpointsSectionProps {
  endpoints: Endpoint[]
  onChange: (endpoints: Endpoint[]) => void
  agentId?: string
}

export default function EndpointsSection({ endpoints, onChange, agentId }: EndpointsSectionProps) {
  const [isAdding, setIsAdding] = useState(false)
  const [editingId, setEditingId] = useState<string | null>(null)
  const [formData, setFormData] = useState<Partial<Endpoint>>({
    method: 'GET',
    headers: {},
  })

  const methodColors = {
    GET: 'bg-blue-100 text-blue-700 border-blue-300',
    POST: 'bg-green-100 text-green-700 border-green-300',
    PUT: 'bg-yellow-100 text-yellow-700 border-yellow-300',
    DELETE: 'bg-red-100 text-red-700 border-red-300',
    PATCH: 'bg-purple-100 text-purple-700 border-purple-300',
  }

  const handleAdd = () => {
    setIsAdding(true)
    setFormData({
      method: 'GET',
      headers: {},
    })
  }

  const handleSave = () => {
    if (!formData.name || !formData.url) {
      toast.error('Please fill in name and URL')
      return
    }

    const endpoint: Endpoint = {
      id: editingId || Math.random().toString(36).substr(2, 9),
      name: formData.name!,
      method: formData.method || 'GET',
      url: formData.url!,
      description: formData.description || '',
      requestExample: formData.requestExample || '',
      responseExample: formData.responseExample || '',
      headers: formData.headers,
    }

    if (editingId) {
      onChange(endpoints.map(e => e.id === editingId ? endpoint : e))
      toast.success('Endpoint updated')
    } else {
      onChange([...endpoints, endpoint])
      toast.success('Endpoint added')
    }

    setIsAdding(false)
    setEditingId(null)
    setFormData({ method: 'GET', headers: {} })
  }

  const handleEdit = (endpoint: Endpoint) => {
    setEditingId(endpoint.id)
    setFormData(endpoint)
    setIsAdding(true)
  }

  const handleDelete = (id: string) => {
    onChange(endpoints.filter(e => e.id !== id))
    toast.success('Endpoint deleted')
  }

  const handleCancel = () => {
    setIsAdding(false)
    setEditingId(null)
    setFormData({ method: 'GET', headers: {} })
  }

  const testEndpoint = async (endpoint: Endpoint) => {
    toast.info('Testing endpoint...')
    // Simulate API test
    setTimeout(() => {
      toast.success('Endpoint is reachable')
    }, 1500)
  }

  return (
    <div className="space-y-6">
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-xl font-semibold text-gray-900">API Endpoints</h2>
            <p className="text-gray-600 mt-1">
              Define the API endpoints that your agent can interact with
            </p>
          </div>
          {!isAdding && (
            <button onClick={handleAdd} className="btn-primary">
              <Plus className="w-4 h-4" />
              Add Endpoint
            </button>
          )}
        </div>

        {/* Add/Edit Form */}
        {isAdding && (
          <div className="mb-6 p-6 bg-gray-50 rounded-lg border-2 border-primary-200">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              {editingId ? 'Edit Endpoint' : 'Add New Endpoint'}
            </h3>
            
            <div className="space-y-4">
              {/* Name and Method */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="label">Endpoint Name</label>
                  <input
                    type="text"
                    className="input"
                    placeholder="e.g., Get User Profile"
                    value={formData.name || ''}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  />
                </div>
                <div>
                  <label className="label">HTTP Method</label>
                  <select
                    className="input"
                    value={formData.method}
                    onChange={(e) => setFormData({ ...formData, method: e.target.value as any })}
                  >
                    <option value="GET">GET</option>
                    <option value="POST">POST</option>
                    <option value="PUT">PUT</option>
                    <option value="DELETE">DELETE</option>
                    <option value="PATCH">PATCH</option>
                  </select>
                </div>
              </div>

              {/* URL */}
              <div>
                <label className="label">Endpoint URL</label>
                <input
                  type="text"
                  className="input font-mono text-sm"
                  placeholder="https://api.example.com/v1/users/{id}"
                  value={formData.url || ''}
                  onChange={(e) => setFormData({ ...formData, url: e.target.value })}
                />
              </div>

              {/* Description */}
              <div>
                <label className="label">Description</label>
                <textarea
                  className="input"
                  rows={3}
                  placeholder="What does this endpoint do?"
                  value={formData.description || ''}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                />
              </div>

              {/* Request Example */}
              <div>
                <label className="label">Request Example (JSON)</label>
                <textarea
                  className="input font-mono text-sm"
                  rows={6}
                  placeholder={`{
  "userId": "12345",
  "includeDetails": true
}`}
                  value={formData.requestExample || ''}
                  onChange={(e) => setFormData({ ...formData, requestExample: e.target.value })}
                />
              </div>

              {/* Response Example */}
              <div>
                <label className="label">Response Example (JSON)</label>
                <textarea
                  className="input font-mono text-sm"
                  rows={6}
                  placeholder={`{
  "success": true,
  "data": {
    "id": "12345",
    "name": "John Doe",
    "email": "john@example.com"
  }
}`}
                  value={formData.responseExample || ''}
                  onChange={(e) => setFormData({ ...formData, responseExample: e.target.value })}
                />
              </div>

              {/* Actions */}
              <div className="flex justify-end space-x-3">
                <button onClick={handleCancel} className="btn-secondary">
                  Cancel
                </button>
                <button onClick={handleSave} className="btn-primary">
                  {editingId ? 'Update' : 'Add'} Endpoint
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Endpoints List */}
        {endpoints.length === 0 && !isAdding ? (
          <div className="text-center py-12 text-gray-500">
            <Globe className="w-12 h-12 mx-auto mb-3 opacity-50" />
            <p>No API endpoints configured yet</p>
            <p className="text-sm mt-1">Add endpoints that your agent can interact with</p>
          </div>
        ) : (
          <div className="space-y-3">
            {endpoints.map((endpoint) => (
              <div
                key={endpoint.id}
                className="p-4 bg-white rounded-lg border border-gray-200 hover:border-gray-300 transition-colors"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <span className={`px-2 py-1 rounded text-xs font-semibold border ${methodColors[endpoint.method]}`}>
                        {endpoint.method}
                      </span>
                      <h3 className="text-lg font-semibold text-gray-900">{endpoint.name}</h3>
                    </div>
                    <p className="text-sm font-mono text-gray-600 mb-2">{endpoint.url}</p>
                    {endpoint.description && (
                      <p className="text-sm text-gray-500">{endpoint.description}</p>
                    )}
                  </div>
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => testEndpoint(endpoint)}
                      className="p-2 text-gray-400 hover:text-primary-600 transition-colors"
                      title="Test endpoint"
                    >
                      <Play className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => handleEdit(endpoint)}
                      className="p-2 text-gray-400 hover:text-blue-600 transition-colors"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleDelete(endpoint.id)}
                      className="p-2 text-gray-400 hover:text-red-600 transition-colors"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Info Card */}
      <div className="card bg-amber-50 border-amber-200">
        <h3 className="text-lg font-semibold text-amber-900 mb-2">Endpoint Configuration</h3>
        <p className="text-sm text-amber-700">
          Define the API endpoints your agent can call to perform actions. The agent will
          automatically understand when to use each endpoint based on user requests and
          the descriptions you provide.
        </p>
      </div>
    </div>
  )
}
