import { Bot, FileText, Zap, TrendingUp, ArrowRight, Activity, Users, Clock } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function Dashboard() {
  const stats = [
    {
      id: 1,
      name: 'Active Agents',
      value: '3',
      change: '+12%',
      trend: 'up',
      icon: Bot,
      color: 'from-blue-500 to-cyan-500',
      bgColor: 'from-blue-50 to-cyan-50',
    },
    {
      id: 2,
      name: 'Documents Processed',
      value: '24',
      change: '+8%',
      trend: 'up',
      icon: FileText,
      color: 'from-purple-500 to-pink-500',
      bgColor: 'from-purple-50 to-pink-50',
    },
    {
      id: 3,
      name: 'API Calls Today',
      value: '1,234',
      change: '+23%',
      trend: 'up',
      icon: Zap,
      color: 'from-orange-500 to-red-500',
      bgColor: 'from-orange-50 to-red-50',
    },
    {
      id: 4,
      name: 'Success Rate',
      value: '98.5%',
      change: '+2.1%',
      trend: 'up',
      icon: TrendingUp,
      color: 'from-green-500 to-emerald-500',
      bgColor: 'from-green-50 to-emerald-50',
    },
  ]

  const recentActivity = [
    { id: 1, agent: 'Analytics Pro Agent', action: 'Answered customer query', time: '2 minutes ago', status: 'success' },
    { id: 2, agent: 'CRM Support Agent', action: 'Updated customer record', time: '15 minutes ago', status: 'success' },
    { id: 3, agent: 'Analytics Pro Agent', action: 'Generated report', time: '1 hour ago', status: 'success' },
    { id: 4, agent: 'CRM Support Agent', action: 'API call failed', time: '2 hours ago', status: 'error' },
  ]

  const quickActions = [
    {
      title: 'Create New Agent',
      description: 'Build a custom AI agent for your product',
      icon: Bot,
      href: '/agents/new',
      color: 'from-primary-600 to-primary-700',
      iconBg: 'from-primary-100 to-primary-200',
    },
    {
      title: 'Upload Documents',
      description: 'Add knowledge base documents',
      icon: FileText,
      href: '/agents/new?tab=documents',
      color: 'from-purple-600 to-purple-700',
      iconBg: 'from-purple-100 to-purple-200',
    },
    {
      title: 'Configure APIs',
      description: 'Set up product API endpoints',
      icon: Zap,
      href: '/agents/new?tab=endpoints',
      color: 'from-orange-600 to-orange-700',
      iconBg: 'from-orange-100 to-orange-200',
    },
  ]

  return (
    <div className="space-y-8">
      {/* Page Header */}
      <div className="animate-slide-up">
        <h1 className="text-4xl font-bold text-gradient mb-2">Dashboard</h1>
        <p className="text-gray-600 text-lg">Welcome back! Here's what's happening with your agents.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 animate-slide-up" style={{ animationDelay: '0.1s' }}>
        {stats.map((stat) => {
          const Icon = stat.icon
          return (
            <div key={stat.id} className="stat-card">
              <div className="relative z-10">
                <div className="flex items-start justify-between mb-4">
                  <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${stat.bgColor} flex items-center justify-center hover:scale-110 transition-transform duration-300`}>
                    <Icon className={`w-6 h-6 bg-gradient-to-br ${stat.color} bg-clip-text text-transparent`} strokeWidth={2.5} />
                  </div>
                  <span className={`flex items-center text-sm font-semibold ${stat.trend === 'up' ? 'text-green-400' : 'text-red-400'}`}>
                    {stat.change}
                    <TrendingUp className={`w-4 h-4 ml-1 ${stat.trend === 'up' ? '' : 'rotate-180'}`} />
                  </span>
                </div>
                <h3 className="text-3xl font-bold text-white mb-1">{stat.value}</h3>
                <p className="text-blue-100 text-sm font-medium">{stat.name}</p>
              </div>
            </div>
          )
        })}
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Quick Actions */}
        <div className="lg:col-span-2 space-y-6">
          <div className="card animate-slide-up" style={{ animationDelay: '0.2s' }}>
            <h2 className="section-title">
              <Zap className="w-7 h-7 text-primary-600" />
              Quick Actions
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {quickActions.map((action) => {
                const Icon = action.icon
                return (
                  <Link
                    key={action.title}
                    to={action.href}
                    className="group relative overflow-hidden p-6 rounded-xl bg-gradient-to-br from-gray-50 to-white border-2 border-gray-100 hover:border-primary-300 transition-all duration-300 hover:shadow-lg hover:scale-105"
                  >
                    <div className={`absolute inset-0 bg-gradient-to-br ${action.color} opacity-0 group-hover:opacity-5 transition-opacity duration-300`} />
                    <div className="relative">
                      <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${action.iconBg} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300`}>
                        <Icon className="w-6 h-6 text-gray-700" />
                      </div>
                      <h3 className="font-bold text-gray-900 mb-2 group-hover:text-primary-600 transition-colors">
                        {action.title}
                      </h3>
                      <p className="text-sm text-gray-600 mb-4">{action.description}</p>
                      <div className="flex items-center text-primary-600 font-semibold text-sm group-hover:translate-x-2 transition-transform duration-300">
                        Get Started
                        <ArrowRight className="w-4 h-4 ml-2" />
                      </div>
                    </div>
                  </Link>
                )
              })}
            </div>
          </div>

          {/* Recent Activity */}
          <div className="card animate-slide-up" style={{ animationDelay: '0.3s' }}>
            <h2 className="section-title">
              <Activity className="w-7 h-7 text-primary-600" />
              Recent Activity
            </h2>
            <div className="space-y-3">
              {recentActivity.map((activity) => (
                <div
                  key={activity.id}
                  className="flex items-center justify-between p-4 rounded-xl bg-gradient-to-r from-gray-50 to-white border border-gray-100 hover:border-gray-200 transition-all duration-200 hover:shadow-md group"
                >
                  <div className="flex items-center gap-4">
                    <div className={`w-10 h-10 rounded-full flex items-center justify-center ${activity.status === 'success' ? 'bg-green-100' : 'bg-red-100'}`}>
                      <Bot className={`w-5 h-5 ${activity.status === 'success' ? 'text-green-600' : 'text-red-600'}`} />
                    </div>
                    <div>
                      <p className="font-semibold text-gray-900 group-hover:text-primary-600 transition-colors">{activity.agent}</p>
                      <p className="text-sm text-gray-600">{activity.action}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2 text-gray-500 text-sm">
                    <Clock className="w-4 h-4" />
                    {activity.time}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* System Status */}
          <div className="card-glow animate-slide-up" style={{ animationDelay: '0.2s' }}>
            <h2 className="section-title">
              <Activity className="w-7 h-7 text-primary-600" />
              System Status
            </h2>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 rounded-lg bg-green-50 border border-green-100">
                <div className="flex items-center gap-3">
                  <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse" />
                  <span className="font-semibold text-green-900">API Server</span>
                </div>
                <span className="text-sm font-medium text-green-700">Online</span>
              </div>
              <div className="flex items-center justify-between p-3 rounded-lg bg-green-50 border border-green-100">
                <div className="flex items-center gap-3">
                  <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse" />
                  <span className="font-semibold text-green-900">AI Models</span>
                </div>
                <span className="text-sm font-medium text-green-700">Active</span>
              </div>
              <div className="flex items-center justify-between p-3 rounded-lg bg-green-50 border border-green-100">
                <div className="flex items-center gap-3">
                  <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse" />
                  <span className="font-semibold text-green-900">Database</span>
                </div>
                <span className="text-sm font-medium text-green-700">Connected</span>
              </div>
            </div>
          </div>

          {/* Usage Stats */}
          <div className="card animate-slide-up" style={{ animationDelay: '0.3s' }}>
            <h2 className="section-title">
              <Users className="w-7 h-7 text-primary-600" />
              Usage This Month
            </h2>
            <div className="space-y-4">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-semibold text-gray-700">API Calls</span>
                  <span className="text-sm font-bold text-primary-600">45,231 / 100,000</span>
                </div>
                <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div className="h-full bg-gradient-to-r from-primary-500 to-primary-600 rounded-full" style={{ width: '45%' }} />
                </div>
              </div>
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-semibold text-gray-700">Document Storage</span>
                  <span className="text-sm font-bold text-purple-600">2.4 GB / 10 GB</span>
                </div>
                <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div className="h-full bg-gradient-to-r from-purple-500 to-purple-600 rounded-full" style={{ width: '24%' }} />
                </div>
              </div>
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-semibold text-gray-700">Active Agents</span>
                  <span className="text-sm font-bold text-green-600">3 / 10</span>
                </div>
                <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div className="h-full bg-gradient-to-r from-green-500 to-green-600 rounded-full" style={{ width: '30%' }} />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
