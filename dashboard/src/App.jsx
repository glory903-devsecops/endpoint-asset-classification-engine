import React, { useState } from 'react';
import { 
  Shield, 
  FileText, 
  User, 
  AlertTriangle, 
  Search, 
  Activity, 
  Database, 
  Settings,
  ChevronRight,
  BarChart3,
  Lock,
  Zap
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const stats = [
  { label: 'Scanned Files', value: '1,732', icon: FileText, color: 'text-blue-400', bg: 'bg-blue-400/10' },
  { label: 'Work Assets', value: '842', icon: Shield, color: 'text-emerald-400', bg: 'bg-emerald-400/10' },
  { label: 'Personal Assets', value: '884', icon: User, color: 'text-amber-400', bg: 'bg-amber-400/10' },
  { label: 'Threats Isolated', value: '6', icon: AlertTriangle, color: 'text-rose-400', bg: 'bg-rose-400/10' },
];

const mockData = [
  { id: 1, name: 'project_proposal_v2.docx', category: 'Work', score: 85, time: '2 mins ago' },
  { id: 2, name: 'family_photo_2024.jpg', category: 'Personal', score: 92, time: '15 mins ago' },
  { id: 3, name: 'malware_detector.exe', category: 'Threat', score: 100, time: '1 hour ago' },
  { id: 4, name: 'architecture_diagram.pdf', category: 'Work', score: 78, time: '3 hours ago' },
];

function App() {
  const [activeTab, setActiveTab] = useState('Overview');

  return (
    <div className="flex h-screen bg-background text-slate-200 overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 border-r border-slate-800 bg-surface/50 backdrop-blur-xl flex flex-col">
        <div className="p-6 flex items-center gap-3">
          <div className="bg-primary p-2 rounded-lg shadow-lg shadow-primary/20">
            <Shield className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-xl font-bold tracking-tight bg-gradient-to-r from-white to-slate-400 bg-clip-text text-transparent">
            AntiGravity
          </h1>
        </div>
        
        <nav className="flex-1 px-4 py-4 space-y-2">
          {['Overview', 'Governance', 'Threats', 'Settings'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 ${
                activeTab === tab 
                ? 'bg-primary/20 text-primary shadow-inner border border-primary/20' 
                : 'hover:bg-slate-800 text-slate-400'
              }`}
            >
              {tab === 'Overview' && <Activity className="w-5 h-5" />}
              {tab === 'Governance' && <Database className="w-5 h-5" />}
              {tab === 'Threats' && <Zap className="w-5 h-5" />}
              {tab === 'Settings' && <Settings className="w-5 h-5" />}
              <span className="font-medium">{tab}</span>
            </button>
          ))}
        </nav>

        <div className="p-4 border-t border-slate-800">
          <div className="bg-slate-900/50 p-4 rounded-2xl border border-slate-800 flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-slate-700 overflow-hidden flex items-center justify-center border border-slate-600">
              <User className="w-6 h-6 text-slate-400" />
            </div>
            <div>
              <p className="text-sm font-semibold">DevSecOps Admin</p>
              <p className="text-xs text-slate-500">Live Engine v2.5</p>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto p-10">
        <header className="flex justify-between items-center mb-10">
          <div>
            <h2 className="text-3xl font-bold mb-2">Governance Dashboard</h2>
            <p className="text-slate-400 italic">Endpoint Asset Classification Engine</p>
          </div>
          <div className="flex gap-4">
            <div className="bg-surface border border-slate-800 rounded-xl px-4 py-2 flex items-center gap-3">
              <Lock className="w-4 h-4 text-emerald-400" />
              <span className="text-sm font-medium">Zero-Trust Secured</span>
            </div>
            <button className="bg-primary hover:bg-primary/90 text-white px-6 py-2 rounded-xl font-semibold shadow-lg shadow-primary/20 transition-all active:scale-95">
              Run Intelligent Scan
            </button>
          </div>
         header>

        {/* Stats Grid */}
        <div className="grid grid-cols-4 gap-6 mb-10">
          {stats.map((stat, i) => (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              key={stat.label}
              className="bg-surface/40 border border-slate-800 p-6 rounded-3xl hover:border-slate-700 transition-colors group relative overflow-hidden"
            >
              <div className={`absolute top-0 right-0 w-24 h-24 ${stat.bg} blur-3xl -mr-10 -mt-10 group-hover:scale-110 transition-transform`} />
              <div className={`${stat.bg} ${stat.color} w-12 h-12 rounded-2xl flex items-center justify-center mb-4`}>
                <stat.icon className="w-6 h-6" />
              </div>
              <p className="text-slate-400 text-sm font-medium mb-1">{stat.label}</p>
              <p className="text-2xl font-bold">{stat.value}</p>
            </motion.div>
          ))}
        </div>

        {/* Main Grid */}
        <div className="grid grid-cols-3 gap-8">
          {/* Classification Log */}
          <section className="col-span-2 bg-surface/40 border border-slate-800 rounded-3xl p-8 backdrop-blur-sm">
            <div className="flex justify-between items-center mb-8">
              <h3 className="text-xl font-bold">Recent Classifications</h3>
              <button className="text-primary hover:underline text-sm font-medium flex items-center gap-1">
                View All <ChevronRight className="w-4 h-4" />
              </button>
            </div>
            <div className="space-y-4">
              {mockData.map((item) => (
                <div key={item.id} className="flex items-center justify-between p-4 bg-slate-900/40 border border-slate-800/50 rounded-2xl hover:bg-slate-800/50 transition-colors">
                  <div className="flex items-center gap-4">
                    <div className={`p-3 rounded-xl ${
                      item.category === 'Work' ? 'bg-emerald-400/10 text-emerald-400' :
                      item.category === 'Threat' ? 'bg-rose-400/10 text-rose-400' :
                      'bg-amber-400/10 text-amber-400'
                    }`}>
                      {item.category === 'Work' && <Lock className="w-5 h-5" />}
                      {item.category === 'Personal' && <User className="w-5 h-5" />}
                      {item.category === 'Threat' && <AlertTriangle className="w-5 h-5" />}
                    </div>
                    <div>
                      <p className="font-semibold text-slate-100">{item.name}</p>
                      <p className="text-xs text-slate-500 font-mono tracking-wider">{item.category.toUpperCase()} • Confidence {item.score}%</p>
                    </div>
                  </div>
                  <p className="text-sm text-slate-500">{item.time}</p>
                </div>
              ))}
            </div>
          </section>

          {/* Quick Analysis */}
          <section className="bg-surface/40 border border-slate-800 rounded-3xl p-8 flex flex-col">
            <h3 className="text-xl font-bold mb-8">Network Activity</h3>
            <div className="flex-1 flex flex-col items-center justify-center p-6 text-center">
              <div className="relative mb-6">
                <div className="absolute inset-0 bg-primary blur-3xl opacity-20 animate-pulse" />
                <BarChart3 className="w-24 h-24 text-primary relative" />
              </div>
              <p className="text-lg font-bold mb-2">Local Governance Sync</p>
              <p className="text-sm text-slate-400 mb-6">Real-time metadata detection is active on your endpoint.</p>
              <div className="w-full bg-slate-900/80 rounded-2xl p-4 border border-slate-800 text-left">
                <div className="flex justify-between items-center mb-1">
                    <span className="text-xs font-semibold text-primary uppercase tracking-widest">Processing</span>
                    <span className="text-xs font-mono text-slate-500">85%</span>
                </div>
                <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                    <motion.div 
                        initial={{ width: 0 }}
                        animate={{ width: '85%' }}
                        transition={{ duration: 1.5, repeat: Infinity, repeatType: 'reverse' }}
                        className="h-full bg-primary" 
                    />
                </div>
              </div>
            </div>
          </section>
        </div>
      </main>
    </div>
  );
}

export default App;
