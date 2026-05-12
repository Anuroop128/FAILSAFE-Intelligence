import { Calendar, GraduationCap, AlertTriangle, AlertOctagon, CheckCircle2, Sparkles } from "lucide-react";

const statusMap = {
  "Critical Intervention": { label: "Critical Intervention", icon: AlertOctagon, cls: "bg-danger/10 text-danger border-danger/20", bar: "bg-danger", accent: "border-l-danger" },
  "Academic Alert": { label: "Academic Alert", icon: AlertTriangle, cls: "bg-warning/15 text-warning border-warning/30", bar: "bg-warning", accent: "border-l-warning" },
  "On Track": { label: "On Track", icon: CheckCircle2, cls: "bg-success/10 text-success border-success/20", bar: "bg-success", accent: "border-l-success" },
};

function formatLabel(label) {
  if (!label) return '';
  return label.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}

export function StudentCard({ student, index }) {
  const st = statusMap[student.risk_tier] || statusMap["On Track"];
  const Icon = st.icon;
  
  return (
    <div className={`bg-card rounded-2xl border border-border border-l-4 ${st.accent} p-5 hover:shadow-[var(--shadow-card)] transition-shadow fade-up`} style={{ animationDelay: `${Math.min(index * 0.06, 0.4)}s` }}>
      <div className="flex items-start justify-between mb-4">
        <div>
          <div className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold">Student ID</div>
          <div className="text-lg font-bold text-foreground leading-tight">#{student.student_id}</div>
          <div className="text-xs text-muted-foreground">Roll No: R-{1000 + student.student_id}</div>
        </div>
        <span className={`inline-flex items-center gap-1.5 text-xs font-semibold px-2.5 py-1 rounded-full border ${st.cls}`}>
          <Icon className="w-3.5 h-3.5" />
          {st.label}
        </span>
      </div>

      <div className="mb-4">
        <div className="flex justify-between text-sm mb-1.5">
          <span className="text-muted-foreground">Risk Probability</span>
          <span className="font-bold text-foreground">{student.risk_probability.toFixed(1)}%</span>
        </div>
        <div className="h-2 bg-muted rounded-full overflow-hidden">
          <div className={`h-full ${st.bar} rounded-full transition-all duration-700`} style={{ width: `${student.risk_probability}%` }} />
        </div>
      </div>

      <div className="flex gap-4 text-sm text-muted-foreground mb-4">
        <span className="inline-flex items-center gap-1.5"><GraduationCap className="w-4 h-4" /> Age <strong className="text-foreground">{student.age}</strong></span>
        <span className="inline-flex items-center gap-1.5"><Calendar className="w-4 h-4" /> Absences <strong className="text-foreground">{student.absences}</strong></span>
      </div>

      <div className="mb-4">
        <div className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold mb-2">Risk Drivers</div>
        <div className="flex flex-wrap gap-1.5">
          {student.top_drivers.map((d, i) => (
            <span key={i} className="text-[11px] font-medium px-2 py-1 rounded-md bg-primary/8 text-primary border border-primary/15">
              {formatLabel(d.feature)} <span className="opacity-70">+{d.impact.toFixed(2)}</span>
            </span>
          ))}
        </div>
      </div>

      <div>
        <div className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold mb-2">AI Action Plan</div>
        <div className="space-y-2">
          {student.interventions.map((a, i) => (
            <div key={i} className="rounded-lg border border-border bg-accent/40 p-3">
              <div className="inline-flex items-center gap-1 text-[10px] font-bold text-primary uppercase tracking-wide mb-1">
                <Sparkles className="w-3 h-3" /> {formatLabel(a.trigger)}
              </div>
              <p className="text-sm text-foreground/80 leading-snug">{a.action}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
