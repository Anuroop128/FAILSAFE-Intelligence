import { LayoutDashboard, Users, Brain, AlertTriangle, FileBarChart, Settings, ShieldCheck } from "lucide-react";

const items = [
  { title: "Dashboard", icon: LayoutDashboard, active: true },
  { title: "Students", icon: Users },
  { title: "AI Insights", icon: Brain },
  { title: "Alerts", icon: AlertTriangle },
  { title: "Reports", icon: FileBarChart },
  { title: "Settings", icon: Settings },
];

export function AppSidebar() {
  return (
    <aside className="hidden lg:flex flex-col w-64 shrink-0 border-r border-border bg-card">
      <div className="h-16 flex items-center gap-2 px-6 border-b border-border">
        <div className="w-9 h-9 rounded-lg flex items-center justify-center" style={{ background: "var(--gradient-primary)" }}>
          <ShieldCheck className="w-5 h-5 text-primary-foreground" />
        </div>
        <div>
          <div className="font-bold tracking-tight text-foreground">FAILSAFE</div>
          <div className="text-[10px] text-muted-foreground uppercase tracking-wider">AI Engine</div>
        </div>
      </div>
      <nav className="flex-1 p-3 space-y-1">
        {items.map((it) => (
          <button
            key={it.title}
            className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
              it.active
                ? "bg-primary/10 text-primary"
                : "text-muted-foreground hover:bg-accent hover:text-foreground"
            }`}
          >
            <it.icon className="w-4 h-4" />
            {it.title}
          </button>
        ))}
      </nav>
      <div className="p-4 border-t border-border">
        <div className="rounded-xl p-4 text-primary-foreground" style={{ background: "var(--gradient-primary)" }}>
          <div className="text-xs font-semibold opacity-90">PRO TIP</div>
          <div className="text-sm mt-1">Upload weekly to track risk trends over time.</div>
        </div>
      </div>
    </aside>
  );
}
