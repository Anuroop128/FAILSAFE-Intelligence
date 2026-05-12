import { useState, useCallback, useEffect, useRef } from 'react';
import { Upload, Brain, Search, Bell, Users, AlertCircle, CheckCircle, Moon, Sun } from "lucide-react";
import { StudentCard } from "./components/StudentCard";
import './App.css';

export default function App() {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [dragOver, setDragOver] = useState(false);
  const [mounted, setMounted] = useState(false);
  const [theme, setTheme] = useState(localStorage.getItem('theme') || 'dark');
  const [filter, setFilter] = useState('All');
  const [query, setQuery] = useState("");
  const inputRef = useRef(null);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => setTheme(prev => prev === 'dark' ? 'light' : 'dark');

  const processFile = (f) => {
    if (!f) return;
    if (!f.name.endsWith('.csv')) {
      setError('Please upload a valid .csv file.');
      return;
    }
    setError(null);
    setFile(f);
    setResults([]);
    setFilter('All');
  };

  const handleFileChange = (e) => processFile(e.target.files[0]);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      processFile(e.dataTransfer.files[0]);
    }
  }, []);

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = () => setDragOver(false);

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a CSV file.');
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Server error');
      }
      const data = await response.json();
      setResults(data.data);
    } catch (err) {
      setError(err.message || 'API Error');
    } finally {
      setLoading(false);
    }
  };

  const high = results.filter(r => r.risk_tier === 'Critical Intervention').length;
  const medium = results.filter(r => r.risk_tier === 'Academic Alert').length;
  const low = results.filter(r => r.risk_tier === 'On Track').length;

  const stats = [
    { key: "All", label: "Total Managed", value: results.length, icon: Users, color: "text-primary bg-primary/10" },
    { key: "Critical Intervention", label: "Critical Priority", value: high, icon: AlertCircle, color: "text-danger bg-danger/10" },
    { key: "Academic Alert", label: "Early Alert", value: medium, icon: AlertCircle, color: "text-warning bg-warning/10" },
    { key: "On Track", label: "Stable/On Track", value: low, icon: CheckCircle, color: "text-success bg-success/10" },
  ];

  const q = query.trim().toLowerCase();
  const visible = results
    .filter(r => filter === 'All' || r.risk_tier === filter)
    .filter(r => {
      if (!q) return true;
      const rollNo = `R-${1000 + r.student_id}`.toLowerCase();
      const id = String(r.student_id).toLowerCase();
      return id.includes(q) || rollNo.includes(q);
    });

  if (!mounted) return null;

  return (
    <div className={`min-h-screen w-full bg-background text-foreground flex flex-col theme-transition ${mounted ? 'opacity-100' : 'opacity-0'}`}>
      {/* Top Action Bar */}
      <div className="flex justify-end p-6 max-w-[1400px] mx-auto w-full">
        <button 
          onClick={toggleTheme} 
          className="flex items-center gap-2 px-4 py-2 rounded-full border border-border bg-card hover:bg-accent transition-all text-[10px] font-black uppercase tracking-widest shadow-sm active:scale-95"
        >
          {theme === 'dark' ? (
            <><Sun className="w-3.5 h-3.5 text-amber-400" /> Light Mode</>
          ) : (
            <><Moon className="w-3.5 h-3.5 text-violet-500" /> Dark Mode</>
          )}
        </button>
      </div>

      <main className="flex-1 p-6 space-y-12 max-w-[1400px] mx-auto w-full">
        
        {/* Big Bold Hero Header */}
        <header className="text-center py-4">
          <h1 className="text-7xl sm:text-8xl md:text-9xl font-[1000] tracking-tighter mb-4 bg-gradient-to-b from-foreground to-foreground/40 bg-clip-text text-transparent uppercase leading-none font-apple">
            FAILSAFE
          </h1>
          <p className="text-sm md:text-lg text-muted-foreground font-semibold tracking-wide uppercase opacity-80">
            Advanced Early Student Risk Detection & Intelligence Engine
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 bg-card rounded-[2rem] border border-border p-8 shadow-sm">
            <div className="flex items-center justify-between mb-8">
              <div>
                <h2 className="text-xl font-bold text-foreground">Data Acquisition</h2>
                <p className="text-xs text-muted-foreground font-medium">Ingest student datasets for predictive modeling</p>
              </div>
              <button 
                onClick={handleUpload}
                disabled={loading || !file}
                className="bg-primary text-primary-foreground px-6 py-3 rounded-2xl text-xs font-black uppercase tracking-widest shadow-elegant hover:opacity-90 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                {loading ? <span className="spin">⟳</span> : <Brain className="w-4 h-4" />}
                {loading ? "Processing..." : "Execute AI Analysis"}
              </button>
            </div>
            <div
              onClick={() => inputRef.current?.click()}
              onDrop={handleDrop}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              className={`border-2 border-dashed rounded-[1.5rem] py-16 flex flex-col items-center justify-center gap-4 cursor-pointer transition-all ${
                dragOver ? "border-primary bg-primary/5 scale-[0.98]" : "border-border hover:border-primary/50 hover:bg-accent/30"
              }`}
            >
              <div className={`p-5 rounded-full shadow-inner ${file ? 'bg-primary/10 text-primary' : 'bg-muted text-muted-foreground'}`}>
                <Upload className="w-10 h-10" />
              </div>
              <div className="text-center">
                <div className="text-lg font-black text-foreground">{file ? file.name : "DEPLOY DATASET"}</div>
                <div className="text-[10px] uppercase font-bold text-muted-foreground mt-1 tracking-widest">{file ? `${(file.size / 1024).toFixed(1)} KB` : "Drop the CSV files here"}</div>
              </div>
              <input ref={inputRef} type="file" accept=".csv" hidden onChange={handleFileChange} />
            </div>
            {error && <div className="mt-4 p-3 rounded-xl bg-danger/10 border border-danger/20 text-danger text-[10px] font-black uppercase tracking-widest flex items-center gap-2">⚠️ {error}</div>}
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-1 gap-4">
            {stats.map((s) => (
              <button
                key={s.key}
                onClick={() => setFilter(s.key)}
                className={`bg-card rounded-[1.5rem] border p-6 text-left transition-all hover:border-primary/50 flex items-center justify-between ${
                  filter === s.key ? "border-primary ring-2 ring-primary/20 shadow-elegant bg-primary/[0.02]" : "border-border"
                }`}
              >
                <div>
                   <div className="text-[10px] uppercase tracking-[0.2em] font-black text-muted-foreground mb-1">{s.label}</div>
                   <div className="text-4xl font-[1000] text-foreground tracking-tighter">{s.value}</div>
                </div>
                <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${s.color}`}>
                  <s.icon className="w-6 h-6" />
                </div>
              </button>
            ))}
          </div>
        </div>

        {results.length > 0 && (
          <div className="bg-card rounded-[1.5rem] border border-border p-6 space-y-6 shadow-sm">
            <div className="flex flex-wrap items-center justify-between gap-6">
              <div>
                <h3 className="text-lg font-black tracking-tight uppercase italic">Intelligence Report</h3>
                <p className="text-xs text-muted-foreground font-bold">Populating {visible.length} data points based on selection</p>
              </div>
              <div className="flex items-center gap-3 px-4 py-3 bg-accent rounded-2xl w-full sm:w-96 border border-border focus-within:border-primary transition-all shadow-inner">
                <Search className="w-5 h-5 text-muted-foreground" />
                <input
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  className="bg-transparent outline-none text-sm flex-1 text-foreground font-semibold placeholder:text-muted-foreground/50"
                  placeholder="Query Student ID or Roll Number..."
                />
              </div>
            </div>

            <div className="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 pt-4 border-t border-border">
              {visible.map((s, i) => (
                <StudentCard key={s.student_id} student={s} index={i} />
              ))}
            </div>
          </div>
        )}

        {/* Empty state when no data */}
        {!loading && results.length === 0 && (
          <div className="text-center py-32 fade-up border-t border-border/50">
            <div className="w-32 h-32 bg-card rounded-[2.5rem] flex items-center justify-center mx-auto mb-8 text-5xl shadow-elegant border border-border">📊</div>
            <h3 className="text-3xl font-[1000] text-foreground tracking-tighter uppercase">No Intelligence Loaded</h3>
            <p className="text-muted-foreground max-w-sm mx-auto mt-4 text-sm font-bold tracking-tight uppercase opacity-60">Upload a student repository to initialize the analysis engine.</p>
          </div>
        )}

        {/* Empty state when search yields nothing */}
        {!loading && results.length > 0 && visible.length === 0 && (
          <div className="text-center py-32 fade-up border-t border-border/50">
             <div className="w-32 h-32 bg-card rounded-[2.5rem] flex items-center justify-center mx-auto mb-8 text-5xl shadow-elegant border border-border">🔍</div>
             <h3 className="text-3xl font-[1000] text-foreground tracking-tighter uppercase">No Matches Identified</h3>
             <p className="text-muted-foreground max-w-sm mx-auto mt-4 text-sm font-bold tracking-tight uppercase opacity-60">Refine your query parameters or adjust status filters.</p>
          </div>
        )}
      </main>

      <footer className="py-12 border-t border-border/50 flex flex-col items-center justify-center gap-2">
        <div className="text-[10px] text-muted-foreground uppercase tracking-[0.5em] font-black opacity-40">
           System Integrity Verified
        </div>
        <div className="text-[12px] text-foreground uppercase tracking-[0.3em] font-[1000]">
          FAILSAFE Intelligence v1.2 - ANUROOP
        </div>
      </footer>
    </div>
  );
}
