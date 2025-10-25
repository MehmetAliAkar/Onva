interface PersonaSectionProps {
  data: {
    role: string
    tone: string
    instructions: string
    constraints: string
  }
  onChange: (data: any) => void
}

export default function PersonaSection({ data, onChange }: PersonaSectionProps) {
  const toneOptions = [
    { value: 'professional', label: 'Professional' },
    { value: 'friendly', label: 'Friendly' },
    { value: 'casual', label: 'Casual' },
    { value: 'technical', label: 'Technical' },
    { value: 'empathetic', label: 'Empathetic' },
  ]

  const roleExamples = [
    'Senior Sales Engineer',
    'Technical Support Specialist',
    'Product Expert',
    'Customer Success Manager',
    'Integration Specialist',
  ]

  return (
    <div className="space-y-6">
      <div className="card">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Agent Persona</h2>
        <p className="text-gray-600 mb-6">
          Define the character and behavior of your agent
        </p>

        <div className="space-y-6">
          {/* Role */}
          <div>
            <label className="label">Role / Title</label>
            <input
              type="text"
              className="input"
              placeholder="e.g., Senior Technical Support Specialist"
              value={data.role}
              onChange={(e) => onChange({ ...data, role: e.target.value })}
            />
            <p className="mt-2 text-sm text-gray-500">
              Examples: {roleExamples.join(', ')}
            </p>
          </div>

          {/* Tone */}
          <div>
            <label className="label">Conversation Tone</label>
            <select
              className="input"
              value={data.tone}
              onChange={(e) => onChange({ ...data, tone: e.target.value })}
            >
              <option value="">Select tone...</option>
              {toneOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>

          {/* Instructions */}
          <div>
            <label className="label">Instructions & Objectives</label>
            <textarea
              className="input font-mono text-sm"
              rows={12}
              placeholder={`Define the agent's purpose and behavior. Example:

You are a knowledgeable product expert for Analytics Pro. Your goal is to:

1. Help customers understand product features and capabilities
2. Guide users through setup and configuration
3. Answer technical questions accurately and clearly
4. Provide relevant examples and use cases
5. Escalate complex issues when necessary

When responding:
- Be clear and concise
- Use specific examples from the documentation
- Ask clarifying questions when needed
- Provide step-by-step guidance for technical tasks
- Always maintain a helpful and patient tone`}
              value={data.instructions}
              onChange={(e) => onChange({ ...data, instructions: e.target.value })}
            />
            <p className="mt-2 text-sm text-gray-500">
              Detailed instructions on how the agent should behave and respond
            </p>
          </div>

          {/* Constraints */}
          <div>
            <label className="label">Constraints & Limitations</label>
            <textarea
              className="input font-mono text-sm"
              rows={8}
              placeholder={`Define what the agent should NOT do. Example:

Constraints:
- Do not make promises about features not yet released
- Do not provide pricing information (direct to sales team)
- Do not access or modify customer data
- Do not provide medical, legal, or financial advice
- Escalate to human support if customer is frustrated
- Always verify information from documentation before responding`}
              value={data.constraints}
              onChange={(e) => onChange({ ...data, constraints: e.target.value })}
            />
            <p className="mt-2 text-sm text-gray-500">
              Rules and boundaries for the agent's behavior
            </p>
          </div>
        </div>
      </div>

      {/* Preview */}
      <div className="card bg-gray-50">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">System Prompt Preview</h3>
        <div className="bg-white p-4 rounded-lg border border-gray-200 font-mono text-sm whitespace-pre-wrap">
          {data.role && `Role: ${data.role}\n\n`}
          {data.tone && `Tone: ${data.tone}\n\n`}
          {data.instructions || 'No instructions defined yet...'}
          {data.constraints && `\n\nConstraints:\n${data.constraints}`}
        </div>
      </div>
    </div>
  )
}
