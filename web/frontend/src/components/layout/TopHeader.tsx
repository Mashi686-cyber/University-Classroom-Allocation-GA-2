"use client"
import { usePathname } from "next/navigation";
import { Menu, CheckCircle2 } from "lucide-react";

export function TopHeader() {
  const pathname = usePathname();
  
  // Format pathname to Title
  const getPageTitle = () => {
    if (pathname === "/") return "Dashboard";
    const path = pathname.split('/')[1];
    if (!path) return "Dashboard";
    return path.charAt(0).toUpperCase() + path.slice(1);
  };

  return (
    <header className="h-14 border-b border-border bg-background flex items-center justify-between px-6 shrink-0">
      <div className="flex items-center gap-4">
        <button className="md:hidden text-muted-foreground hover:text-foreground">
          <Menu className="w-5 h-5" />
        </button>
        <h1 className="font-semibold text-foreground text-sm tracking-wide">
          {getPageTitle()}
        </h1>
      </div>
      
      <div className="flex items-center gap-6">
        <div className="hidden sm:flex items-center gap-2">
          <span className="text-xs font-medium text-muted-foreground">Dataset:</span>
          <span className="text-xs font-semibold text-foreground bg-muted px-2 py-1 rounded">Small</span>
        </div>
        
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-success animate-pulse" />
          <span className="text-xs font-medium text-muted-foreground">System Ready</span>
        </div>
      </div>
    </header>
  );
}
