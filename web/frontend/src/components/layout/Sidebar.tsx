"use client"
import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  LayoutDashboard, Database, PlayCircle, BarChart3, LineChart, FlaskConical, LayoutGrid, CalendarDays, Settings, CalendarClock 
} from "lucide-react";

export function Sidebar() {
  const pathname = usePathname();

  const navGroups = [
    {
      label: "OVERVIEW",
      items: [
        { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
      ]
    },
    {
      label: "DATA",
      items: [
        { name: "Datasets", href: "/datasets", icon: Database },
        { name: "Classrooms", href: "/classrooms", icon: LayoutGrid },
      ]
    },
    {
      label: "OPTIMIZATION",
      items: [
        { name: "Allocation", href: "/allocation", icon: PlayCircle },
        { name: "Timetable", href: "/results/latest/timetable", icon: CalendarClock },
      ]
    },
    {
      label: "ANALYTICS",
      items: [
        { name: "Results", href: "/results", icon: BarChart3 },
        { name: "Comparison", href: "/comparison", icon: LineChart },
        { name: "Experiments", href: "/experiments", icon: FlaskConical },
      ]
    },
    {
      label: "RESEARCH",
      items: [
        { name: "Research Findings", href: "/research", icon: BarChart3 },
      ]
    },
    {
      label: "SYSTEM",
      items: [
        { name: "Settings", href: "/settings", icon: Settings },
      ]
    }
  ];

  return (
    <div className="hidden md:flex w-64 border-r border-border bg-[#0D0D0F] flex-col overflow-y-auto">
      <div className="p-6 flex items-center gap-3 border-b border-border">
        <div className="w-8 h-8 rounded-lg bg-accent/20 flex items-center justify-center text-accent">
          <CalendarDays className="w-5 h-5" />
        </div>
        <div>
          <div className="font-bold tracking-tight text-foreground">UniClass GA</div>
          <div className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold">Optimization Platform</div>
        </div>
      </div>

      <div className="p-4 flex-1 space-y-6">
        {navGroups.map((group) => (
          <div key={group.label}>
            <div className="text-[11px] font-semibold text-muted-foreground mb-2 px-2 tracking-wider">
              {group.label}
            </div>
            <div className="space-y-1">
              {group.items.map(item => {
                const isActive = pathname.startsWith(item.href) && item.href !== "/results" || (item.href === "/results" && pathname === "/results");
                return (
                  <Link 
                    key={item.href} 
                    href={item.href} 
                    className={`flex items-center gap-3 px-2 py-2 rounded-md transition-colors text-sm font-medium ${
                      isActive 
                        ? "bg-accent/10 text-accent" 
                        : "text-muted-foreground hover:bg-muted hover:text-foreground"
                    }`}
                  >
                    <item.icon className="w-4 h-4" />
                    {item.name}
                    {isActive && (
                      <div className="ml-auto w-1 h-4 bg-accent rounded-full" />
                    )}
                  </Link>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
