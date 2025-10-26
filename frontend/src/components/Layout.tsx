import { ReactNode } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Bot, LayoutDashboard, Sparkles, Menu, X, Zap } from 'lucide-react'
import { useState } from 'react'

interface LayoutProps {
  children: ReactNode
}

export default function Layout({ children }: LayoutProps) {
  const location = useLocation()
  const [sidebarOpen, setSidebarOpen] = useState(true)

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
    { name: 'Agents', href: '/agents', icon: Bot },
    { name: 'New Agent', href: '/agents/new', icon: Sparkles, highlight: true },
  ]

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Modern Sidebar with Gradient */}
      <aside
        className={`${
          sidebarOpen ? 'w-72' : 'w-20'
        } bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white transition-all duration-500 ease-in-out flex flex-col relative shadow-2xl`}
      >
        {/* Logo & Brand */}
        <div className="p-6 border-b border-gray-700/50 backdrop-blur-sm">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-400 to-primary-600 flex items-center justify-center shadow-glow animate-float">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            {sidebarOpen && (
              <div className="animate-slide-down">
                <h1 className="text-xl font-bold bg-gradient-to-r from-white to-blue-200 bg-clip-text text-transparent">
                  Onva
                </h1>
                <p className="text-xs text-gray-400">Agent Builder Platform</p>
              </div>
            )}
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href
            const Icon = item.icon

            return (
              <Link
                key={item.href}
                to={item.href}
                className={`
                  flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 group relative
                  ${
                    isActive
                      ? 'bg-gradient-to-r from-primary-600 to-primary-700 text-white shadow-glow scale-105'
                      : 'text-gray-300 hover:bg-white/10 hover:text-white'
                  }
                  ${item.highlight ? 'ring-2 ring-primary-400/50' : ''}
                `}
              >
                {isActive && (
                  <div className="absolute inset-0 bg-gradient-to-r from-primary-400/20 to-primary-600/20 rounded-xl blur-xl -z-10" />
                )}
                <Icon className={`w-5 h-5 ${isActive ? 'animate-scale-in' : 'group-hover:scale-110 transition-transform'}`} />
                {sidebarOpen && (
                  <span className={`font-semibold ${item.highlight ? 'text-transparent bg-gradient-to-r from-white to-blue-200 bg-clip-text' : ''}`}>
                    {item.name}
                  </span>
                )}
                {item.highlight && sidebarOpen && (
                  <Zap className="w-4 h-4 ml-auto text-yellow-400 animate-pulse" />
                )}
              </Link>
            )
          })}
        </nav>

        {/* Sidebar Toggle */}
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="absolute -right-3 top-20 w-6 h-6 bg-gradient-to-br from-primary-500 to-primary-700 rounded-full flex items-center justify-center shadow-lg hover:shadow-glow transition-all duration-300 hover:scale-110"
        >
          {sidebarOpen ? (
            <X className="w-3 h-3 text-white" />
          ) : (
            <Menu className="w-3 h-3 text-white" />
          )}
        </button>

        {/* User Profile Section */}
        {sidebarOpen && (
          <div className="p-4 border-t border-gray-700/50 backdrop-blur-sm">
            <div className="flex items-center gap-3 p-3 rounded-xl bg-white/5 hover:bg-white/10 transition-all duration-300 cursor-pointer group">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-400 to-pink-400 flex items-center justify-center text-white font-bold shadow-md group-hover:scale-110 transition-transform">
                M
              </div>
              <div className="flex-1">
                <p className="text-sm font-semibold text-white">Matreus</p>
                <p className="text-xs text-gray-400">info@matreus.com</p>
              </div>
            </div>
          </div>
        )}
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Modern Header with Gradient */}
        <header className="glass border-b border-white/20 backdrop-blur-xl sticky top-0 z-10">
          <div className="px-8 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                  <span className="text-sm text-gray-600 font-medium">System Online</span>
                </div>
              </div>
              
              {/* Quick Stats */}
              <div className="flex items-center gap-6">
                <div className="flex items-center gap-2 px-4 py-2 rounded-xl bg-blue-50 border border-blue-100">
                  <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse" />
                  <span className="text-sm font-semibold text-blue-700">2 Active Agents</span>
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 overflow-y-auto">
          <div className="px-8 py-6 animate-fade-in">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}
