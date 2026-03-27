import React, { useState, useEffect } from 'react';
import { 
  Shield, 
  FileText, 
  User, 
  AlertTriangle, 
  Activity, 
  Lock,
  Zap,
  FolderOpen,
  Loader2,
  Globe,
  ChevronRight,
  BarChart3
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const API_BASE = 'http://localhost:8000';

// 데모 모드 감지 (localhost가 아니면 데모 모드로 동작)
const isDemoMode = typeof window !== 'undefined' && 
  window.location.hostname !== 'localhost' && 
  window.location.hostname !== '127.0.0.1';

const mockStats = {
  total: 2458,
  work: 1124,
  personal: 1320,
  security: 14,
  recent: [
    { original_name: '기업_기밀_계약서_v2.pdf', category: 'Work', file_hash: 'a1b2c3d4e5f67890', detected_at: new Date(Date.now() - 1000 * 60 * 5).toISOString() },
    { original_name: '가족_해외여행_2024.mp4', category: 'Personal', file_hash: 'f6e5d4c3b2a10987', detected_at: new Date(Date.now() - 1000 * 60 * 15).toISOString() },
    { original_name: '보안_취약점_샘플.exe', category: 'Vulnerability_Sample', file_hash: '7890abcdef123456', detected_at: new Date(Date.now() - 1000 * 60 * 60).toISOString(), is_malware: true },
    { original_name: '시스템_아키텍처_설계.docx', category: 'Work', file_hash: '12345678abcdefgh', detected_at: new Date(Date.now() - 1000 * 60 * 120).toISOString() },
  ]
};

function App() {
  const [activeTab, setActiveTab] = useState('실시간 거버넌스');
  const [rootPath, setRootPath] = useState(isDemoMode ? '/demo/security/assets' : 'g:\\내 드라이브\\99.Develop\\endpoint-asset-classification-engine\\test_data\\inbox');
  const [isScanning, setIsScanning] = useState(false);
  const [stats, setStats] = useState(isDemoMode ? mockStats : {
    total: 0,
    work: 0,
    personal: 0,
    security: 0,
    recent: []
  });

  const fetchStats = async () => {
    if (isDemoMode) return;
    try {
      const response = await fetch(`${API_BASE}/api/stats`);
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error('데이터 통신 실패:', error);
    }
  };

  useEffect(() => {
    if (!isDemoMode) {
      fetchStats();
      const interval = setInterval(fetchStats, 5000);
      return () => clearInterval(interval);
    }
  }, []);

  const handleScan = async () => {
    if (!rootPath) return;
    setIsScanning(true);

    if (isDemoMode) {
      // 데모 모드용 시뮬레이션
      await new Promise(resolve => setTimeout(resolve, 2500));
      setStats(prev => ({
        ...prev,
        total: prev.total + 1,
        work: prev.work + 1,
        recent: [
          { original_name: '신규_보안_분석_데이터.py', category: 'Work', file_hash: 'demo_' + Math.random().toString(16).slice(2), detected_at: new Date().toISOString() },
          ...prev.recent
        ].slice(0, 6)
      }));
      setIsScanning(false);
      return;
    }

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
      console.error('스캔 작업 실패:', error);
    } finally {
      setIsScanning(false);
    }
  };

  const statCards = [
    { label: '전체 자산 스캔', value: stats.total.toLocaleString(), icon: FileText, color: 'text-blue-400', bg: 'bg-blue-400/10' },
    { label: '업무용 승인됨', value: stats.work.toLocaleString(), icon: Shield, color: 'text-emerald-400', bg: 'bg-emerald-400/10' },
    { label: '개인용 식별됨', value: stats.personal.toLocaleString(), icon: User, color: 'text-amber-400', bg: 'bg-amber-400/10' },
    { label: '위협 격리 완료', value: stats.security.toLocaleString(), icon: AlertTriangle, color: 'text-rose-400', bg: 'bg-rose-400/10' },
  ];

  return (
    <div className="flex h-screen bg-[#08090a] text-slate-300 overflow-hidden font-sans selection:bg-blue-500/30">
      {/* Sidebar - 오직 기능하는 메뉴만 유지 */}
      <aside className="w-64 border-r border-white/5 bg-black/40 backdrop-blur-2xl flex flex-col">
        <div className="p-8 flex items-center gap-3">
          <div className="bg-blue-600 p-2.5 rounded-2xl shadow-2xl shadow-blue-600/40 transform rotate-3 hover:rotate-0 transition-transform cursor-pointer">
            <Shield className="w-6 h-6 text-white" />
          </div>
          <h1 className="text-xl font-black tracking-tighter text-white uppercase italic">
            AntiGravity
          </h1>
        </div>
        
        <nav className="flex-1 px-6 py-6 space-y-3">
          {['실시간 거버넌스'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`w-full flex items-center gap-3 px-5 py-3.5 rounded-2xl transition-all duration-500 ${
                activeTab === tab 
                ? 'bg-blue-600/10 text-white shadow-[inset_0_0_20px_rgba(37,99,235,0.1)] border border-blue-500/30' 
                : 'hover:bg-white/5 text-slate-500'
              }`}
            >
              <Activity className={`w-5 h-5 ${activeTab === tab ? 'text-blue-400' : ''}`} />
              <span className="font-bold tracking-tight">{tab}</span>
            </button>
          ))}
        </nav>

        <div className="p-6">
          <div className="bg-gradient-to-br from-white/5 to-transparent p-4 rounded-3xl border border-white/10 flex items-center gap-3 shadow-inner">
            <div className="w-10 h-10 rounded-full bg-slate-800 border border-white/10 flex items-center justify-center overflow-hidden">
               <User className="w-6 h-6 text-slate-500" />
            </div>
            <div>
              <p className="text-xs font-bold text-white">보안 관리자</p>
              <p className="text-[10px] text-slate-500 font-mono tracking-tighter uppercase opacity-60">Engine v2.5 Online</p>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto p-12 bg-[#08090a]">
        <header className="flex justify-between items-end mb-12">
          <div className="space-y-3">
            <div className="flex items-center gap-4">
                <h2 className="text-4xl font-black tracking-tighter text-white">엔드포인트 보안 파일 자산 분류 및 식별</h2>
                {isDemoMode && (
                    <span className="bg-blue-500/10 text-blue-400 text-[10px] font-black px-3 py-1 rounded-full border border-blue-500/20 flex items-center gap-1.5 animate-pulse">
                        <Globe className="w-3 h-3" /> LIVE DEMO
                    </span>
                )}
            </div>
            <div className="flex items-center gap-3 bg-white/5 px-4 py-2 rounded-2xl border border-white/5 group hover:border-blue-500/30 transition-all">
              <FolderOpen className="w-4 h-4 text-slate-500 group-hover:text-blue-400" />
              <input 
                type="text" 
                value={rootPath}
                onChange={(e) => setRootPath(e.target.value)}
                className="bg-transparent border-none outline-none text-[13px] w-[500px] text-slate-400 group-hover:text-white transition-colors font-mono"
                placeholder="스캔하여 분류할 폴더 전제 경로를 입력하십시오..."
              />
            </div>
          </div>
          
          <div className="flex gap-4">
            <button 
              onClick={handleScan}
              disabled={isScanning}
              className="group relative bg-white text-black hover:bg-white/90 disabled:bg-slate-800 disabled:text-slate-500 px-8 py-4 rounded-3xl font-black text-sm tracking-tighter transition-all active:scale-95 flex items-center gap-3 overflow-hidden"
            >
              {isScanning ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Zap className="w-5 h-5 group-hover:fill-current transition-all" />
              )}
              {isScanning ? '분류 처리 중...' : isDemoMode ? '샘플 분류 시뮬레이션' : '자산 분류 프로세스 시작'}
            </button>
          </div>
        </header>

        {/* Stats Grid */}
        <div className="grid grid-cols-4 gap-6 mb-12">
          {statCards.map((stat, i) => (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              key={stat.label}
              className="bg-black/20 border border-white/5 p-7 rounded-[2.5rem] hover:border-blue-500/40 transition-all group relative overflow-hidden"
            >
              <div className={`absolute -top-10 -right-10 w-32 h-32 ${stat.bg} blur-[80px] opacity-0 group-hover:opacity-40 transition-opacity`} />
              <div className={`${stat.bg} ${stat.color} w-14 h-14 rounded-3xl flex items-center justify-center mb-5 transform group-hover:-rotate-6 transition-transform`}>
                <stat.icon className="w-7 h-7" />
              </div>
              <p className="text-slate-500 text-xs font-bold mb-1 tracking-tight">{stat.label}</p>
              <div className="flex items-baseline gap-1">
                <p className="text-3xl font-black text-white tracking-tighter">{stat.value}</p>
                <span className="text-[10px] text-slate-600 font-bold uppercase">Meta</span>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Main Grid */}
        <div className="grid grid-cols-3 gap-8">
          {/* Classification Log */}
          <section className="col-span-2 bg-white/[0.02] border border-white/5 rounded-[3rem] p-10 relative overflow-hidden">
            <div className="flex justify-between items-center mb-10">
              <h3 className="text-2xl font-black tracking-tighter text-white flex items-center gap-3">
                <Activity className="w-6 h-6 text-blue-500" />
                실시간 데이터 처리 로그
              </h3>
            </div>
            <div className="space-y-3 relative z-10">
              <AnimatePresence>
                {stats.recent.map((item, idx) => (
                  <motion.div 
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    key={idx} 
                    className="flex items-center justify-between p-5 bg-white/[0.03] border border-white/5 rounded-[2rem] hover:bg-white/[0.06] transition-all group"
                  >
                    <div className="flex items-center gap-5">
                      <div className={`p-4 rounded-2xl ${
                        item.category === 'Work' ? 'bg-emerald-500/10 text-emerald-500' :
                        item.category === 'Personal' ? 'bg-amber-500/10 text-amber-500' :
                        'bg-rose-500/10 text-rose-500'
                      }`}>
                        {item.category === 'Work' && <Lock className="w-6 h-6" />}
                        {item.category === 'Personal' && <User className="w-6 h-6" />}
                        {(item.category === 'Vulnerability_Sample' || item.is_malware) && <AlertTriangle className="w-6 h-6" />}
                      </div>
                      <div>
                        <p className="font-bold text-white text-lg tracking-tight group-hover:text-blue-400 transition-colors">
                          {item.original_name}
                        </p>
                        <div className="flex items-center gap-2 mt-1">
                            <span className={`text-[10px] font-black px-2 py-0.5 rounded-md ${
                                item.category === 'Work' ? 'bg-emerald-500/10 text-emerald-500' : 'bg-slate-800 text-slate-400'
                            }`}>
                                {item.category === 'Work' ? '업무용 승인' : item.category === 'Personal' ? '개인용 분류' : '격리 위협'}
                            </span>
                            <span className="text-[10px] text-slate-600 font-mono tracking-tighter">
                                {item.file_hash.substring(0, 16).toUpperCase()}
                            </span>
                        </div>
                      </div>
                    </div>
                    <div className="text-right flex flex-col items-end gap-1">
                      <div className="flex items-center gap-1.5 text-xs text-slate-500 font-bold">
                        <div className="w-1.5 h-1.5 rounded-full bg-blue-600" />
                        {new Date(item.detected_at).toLocaleTimeString()}
                      </div>
                      <p className="text-[10px] text-blue-500 font-black tracking-widest uppercase opacity-40">
                        {isDemoMode ? 'SIMULATED' : 'ORGANIZED'}
                      </p>
                    </div>
                  </motion.div>
                ))}
              </AnimatePresence>
              {stats.recent.length === 0 && (
                <div className="py-24 text-center border-2 border-dashed border-white/5 rounded-[3rem] flex flex-col items-center gap-4">
                  <Database className="w-12 h-12 text-slate-800" />
                  <p className="text-slate-600 font-bold tracking-tight">수신된 실시간 데이터 스트림이 없습니다.</p>
                </div>
              )}
            </div>
          </section>

          {/* Engine Insights */}
          <section className="bg-gradient-to-b from-blue-600 to-blue-800 rounded-[3rem] p-10 flex flex-col shadow-2xl shadow-blue-600/20 relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-64 h-64 bg-white/20 blur-[100px] -mr-20 -mt-20 group-hover:scale-110 transition-transform duration-1000" />
            
            <h3 className="text-2xl font-black tracking-tighter text-white mb-10 flex items-center gap-3 relative z-10">
                <BarChart3 className="w-6 h-6" />
                엔진 인텔리전스
            </h3>
            
            <div className="flex-1 flex flex-col items-center justify-center p-6 text-center relative z-10">
              <div className="w-24 h-24 bg-white rounded-[2.5rem] flex items-center justify-center shadow-2xl mb-8 transform group-hover:rotate-12 transition-transform shadow-white/20">
                <Shield className="w-12 h-12 text-blue-600" />
              </div>
              
              <p className="text-2xl font-black text-white mb-3 tracking-tighter">제로트러스트 가드</p>
              <p className="text-sm text-blue-100/70 font-bold leading-relaxed mb-10">
                {isDemoMode 
                    ? '이 웹 페이지는 데모용 라이브 프리뷰입니다. 실제 로컬 시스템 연동을 위해서는 통합 도구를 실행하십시오.'
                    : '엔드포인트 실시간 모니터링이 활성화되었습니다. 모든 무단 자산 접근은 자동으로 식별 및 격리됩니다.'}
              </p>
              
              <div className="w-full bg-black/20 backdrop-blur-md rounded-3xl p-6 border border-white/10 text-left">
                <div className="flex justify-between items-center mb-3">
                    <span className="text-xs font-black text-white/50 uppercase tracking-widest">자동 분류 신뢰도</span>
                    <span className="text-xs font-mono font-black text-white">98.2%</span>
                </div>
                <div className="w-full h-1.5 bg-black/30 rounded-full overflow-hidden">
                    <motion.div 
                        initial={{ width: 0 }}
                        animate={{ width: '98.2%' }}
                        transition={{ duration: 2.5, ease: "easeOut" }}
                        className="h-full bg-white shadow-[0_0_15px_rgba(255,255,255,0.8)]" 
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
