import { Link, useLocation } from 'react-router-dom'
import { Activity } from 'lucide-react'

export function Navbar() {
  const { pathname } = useLocation()

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 h-16 flex items-center justify-between px-8 glass border-b border-white/[0.06]">
      <Link to="/" className="flex items-center gap-2.5 group">
        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-violet-500 to-purple-700 flex items-center justify-center shadow-lg shadow-violet-500/20">
          <Activity size={16} className="text-white" />
        </div>
        <span className="font-semibold text-white tracking-tight">
          Medi<span className="gradient-text">Guide</span>
        </span>
      </Link>

      <div className="flex items-center gap-6">
        <Link
          to="/"
          className={`text-sm transition-colors ${pathname === '/' ? 'text-violet-300' : 'text-white/50 hover:text-white/80'}`}
        >
          Home
        </Link>
        <Link
          to="/chat"
          className={`text-sm transition-colors ${pathname === '/chat' ? 'text-violet-300' : 'text-white/50 hover:text-white/80'}`}
        >
          Chat
        </Link>
        <a href="#" className="text-sm text-white/50 hover:text-white/80 transition-colors">
          About
        </a>
        <Link
          to="/chat"
          className="btn-primary text-sm font-medium text-white px-4 py-2 rounded-lg"
        >
          Get Started
        </Link>
      </div>
    </nav>
  )
}
