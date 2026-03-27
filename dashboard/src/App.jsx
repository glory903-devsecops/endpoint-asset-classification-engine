import React, { useState, useEffect } from 'react';
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
  Zap,
  FolderOpen,
  Loader2
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const API_BASE = 'http://localhost:8000';

function App() {
  const [activeTab, setActiveTab] = useState('Overview');
  const [rootPath, setRootPath] = useState('g:\\내 드라이브\\99.Develop\\endpoint-asset-classification-engine\\test_data\\inbox');
  const [isScanning, setIsScanning] = useState(false);
  const [stats, setStats] = useState({
    total: 0,
    work: 0,
    personal: 0,
    security: 0,
    recent: []
  });

  const fetchStats = async () => {
    try {
      const response = await fetch(`${API_BASE}/api/stats`);
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    }
  };

  useEffect(() => {
    fetchStats();
    const interval = setInterval(fetchStats, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleScan = async () => {
    if (!rootPath) return;
    setIsScanning(true);
    try {
      const response = await fetch(`${API_BASE}/api/scan`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ root_path: rootPath })
      });
      const data = await response.json();
      if (data.status === 'success') {
        fetchStats();
      }
    } catch (error) {
      console.error('Scan failed:', error);
    } finally {
      setIsScanning(false);
    }
  };

  const statCards = [
    { label: 'Total Scanned', value: stats.total.toLocaleString(), icon: FileText, color: 'text-blue-400', bg: 'bg-blue-400/10' },
    { label: 'Work Assets', value: stats.work.toLocaleString(), icon: Shield, color: 'text-emerald-400', bg: 'bg-emerald-400/10' },
    { label: 'Personal Assets', value: stats.personal.toLocaleString(), icon: User, color: 'text-amber-400', bg: 'bg-amber-400/10' },
    { label: 'Threats Isolated', value: stats.security.toLocaleString(), icon: AlertTriangle, color: 'text-rose-400', bg: 'bg-rose-400/10' },
  ];

  return (
    <div className="flex h-screen bg-[#0a0c10] text-slate-200 overflow-hidden font-sans">
      {/* Sidebar */}
      <aside className="w-64 border-r border-slate-800 bg-black/20 backdrop-blur-3xl flex flex-col">
        <div className="p-6 flex items-center gap-3">
          <div className="bg-blue-600 p-2 rounded-xl shadow-lg shadow-blue-600/20">
            <Shield className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-xl font-bold tracking-tight bg-gradient-to-r from-white to-slate-500 bg-clip-text text-transparent">
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
                ? 'bg-blue-600/10 text-blue-400 shadow-inner border border-blue-500/20' 
                : 'hover:bg-white/5 text-slate-400'
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
          <div className="bg-white/5 p-4 rounded-2xl border border-white/10 flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-slate-800 overflow-hidden flex items-center justify-center border border-slate-700">
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
      <main className="flex-1 overflow-y-auto p-10 bg-gradient-to-br from-[#0a0c10] to-[#0d1117]">
        <header className="flex justify-between items-start mb-10">
          <div>
            <h2 className="text-3xl font-bold mb-2 tracking-tight">Active Governance</h2>
            <div className="flex items-center gap-2 text-slate-400">
              <FolderOpen className="w-4 h-4" />
              <input 
                type="text" 
                value={rootPath}
                onChange={(e) => setRootPath(e.target.value)}
                className="bg-transparent border-none outline-none text-sm w-96 hover:text-slate-200 transition-colors"
                placeholder="Target Scan Path..."
              />
            </div>
          </div>
          <div className="flex gap-4">
            <div className="bg-black/40 border border-slate-800 rounded-2xl px-4 py-2 flex items-center gap-3 backdrop-blur-md">
              <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              <span className="text-sm font-medium text-slate-300">Engine Online</span>
            </div>
            <button 
              onClick={handleScan}
              disabled={isScanning}
              className="group bg-blue-600 hover:bg-blue-500 disabled:bg-slate-700 text-white px-6 py-2.5 rounded-2xl font-semibold shadow-lg shadow-blue-600/20 transition-all active:scale-95 flex items-center gap-2"
            >
              {isScanning ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Activity className="w-5 h-5 group-hover:rotate-12 transition-transform" />
              )}
              {isScanning ? 'Scanning...' : 'Start Dynamic Scan'}
            </button>
          </div>
        </header>

        {/* Stats Grid */}
        <div className="grid grid-cols-4 gap-6 mb-10">
          {statCards.map((stat, i) => (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              key={stat.label}
              className="bg-white/5 border border-white/10 p-6 rounded-[2rem] hover:border-blue-500/30 transition-all group relative overflow-hidden"
            >
              <div className={`absolute top-0 right-0 w-24 h-24 ${stat.bg} blur-3xl -mr-10 -mt-10 group-hover:scale-110 transition-transform`} />
              <div className={`${stat.bg} ${stat.color} w-12 h-12 rounded-2xl flex items-center justify-center mb-4`}>
                <stat.icon className="w-6 h-6" />
              </div>
              <p className="text-slate-400 text-sm font-medium mb-1">{stat.label}</p>
              <p className="text-2xl font-bold text-white tracking-tight">{stat.value}</p>
            </motion.div>
          ))}
        </div>

        {/* Main Grid */}
        <div className="grid grid-cols-3 gap-8">
          {/* Classification Log */}
          <section className="col-span-2 bg-white/5 border border-white/10 rounded-[2.5rem] p-8 backdrop-blur-xl">
            <div className="flex justify-between items-center mb-8">
              <h3 className="text-xl font-bold flex items-center gap-2">
                <Activity className="w-5 h-5 text-blue-400" />
                Live Classification Log
              </h3>
              <button className="text-blue-400 hover:text-blue-300 text-sm font-medium flex items-center gap-1 transition-colors">
                View All History <ChevronRight className="w-4 h-4" />
              </button>
            </div>
            <div className="space-y-3">
              <AnimatePresence>
                {stats.recent.map((item, idx) => (
                  <motion.div 
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    key={idx} 
                    className="flex items-center justify-between p-4 bg-white/5 border border-white/5 rounded-2xl hover:bg-white/10 transition-all group"
                  >
                    <div className="flex items-center gap-4">
                      <div className={`p-3 rounded-xl ${
                        item.category === 'Work' ? 'bg-emerald-400/10 text-emerald-400' :
                        item.category === 'Personal' ? 'bg-amber-400/10 text-amber-400' :
                        'bg-rose-400/10 text-rose-400'
                      }`}>
                        {item.category === 'Work' && <Lock className="w-5 h-5" />}
                        {item.category === 'Personal' && <User className="w-5 h-5" />}
                        {(item.category === 'Vulnerability_Sample' || item.is_malware) && <AlertTriangle className="w-5 h-5" />}
                      </div>
                      <div>
                        <p className="font-semibold text-slate-100 group-hover:text-white transition-colors">
                          {item.original_name}
                        </p>
                        <p className="text-[10px] text-slate-500 font-mono tracking-widest uppercase mt-0.5">
                          {item.category} • {item.file_hash.substring(0, 12)}...
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-xs text-slate-400">{new Date(item.detected_at).toLocaleTimeString()}</p>
                      <p className="text-[10px] text-slate-600 font-mono italic">in-place organized</p>
                    </div>
                  </motion.div>
                ))}
              </AnimatePresence>
              {stats.recent.length === 0 && (
                <div className="py-20 text-center text-slate-500 italic border-2 border-dashed border-white/5 rounded-3xl">
                  No scan history detected. Please start a scan above.
                </div>
              )}
            </div>
          </section>

          {/* Real-time Health */}
          <section className="bg-white/5 border border-white/10 rounded-[2.5rem] p-8 flex flex-col backdrop-blur-xl relative overflow-hidden">
            <div className="absolute inset-0 bg-blue-600/5 blur-3xl rounded-full -bottom-1/2 -right-1/2" />
            <h3 className="text-xl font-bold mb-8 relative z-10 flex items-center gap-2">
                <BarChart3 className="w-5 h-5 text-blue-400" />
                System Health
            </h3>
            <div className="flex-1 flex flex-col items-center justify-center p-6 text-center relative z-10">
              <div className="relative mb-6">
                <div className="absolute inset-0 bg-blue-600 blur-3xl opacity-20 animate-pulse" />
                <BarChart3 className="w-24 h-24 text-blue-500 relative" />
              </div>
              <p className="text-lg font-bold mb-2">Zero-Trust Engine</p>
              <p className="text-sm text-slate-400 mb-8 leading-relaxed">
                Autonomous classification and isolation are active. All metadata is hashed and logged for audit.
              </p>
              <div className="w-full bg-slate-900/50 rounded-2xl p-5 border border-white/10 text-left">
                <div className="flex justify-between items-center mb-2">
                    <span className="text-xs font-semibold text-blue-400 uppercase tracking-widest">Confidence Index</span>
                    <span className="text-xs font-mono text-slate-500">98.2%</span>
                </div>
                <div className="w-full h-1 bg-slate-800 rounded-full overflow-hidden">
                    <motion.div 
                        initial={{ width: 0 }}
                        animate={{ width: '98.2%' }}
                        transition={{ duration: 2 }}
                        className="h-full bg-blue-500 shadow-[0_0_10px_rgba(59,130,246,0.5)]" 
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
