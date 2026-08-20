import { Card, CardContent } from "@/components/ui/card";
import { LucideIcon } from "lucide-react";

interface MetricCardProps {
  title: string;
  value: string | number;
  icon: LucideIcon;
  trend?: string;
  trendUp?: boolean;
}

export function MetricCard({ title, value, icon: Icon, trend, trendUp }: MetricCardProps) {
  return (
    <Card className="hover:border-muted-foreground/30 transition-colors">
      <CardContent className="p-5 flex items-start justify-between">
        <div className="space-y-2">
          <p className="text-xs font-medium text-muted-foreground tracking-wider uppercase">{title}</p>
          <div className="text-2xl font-semibold text-foreground tracking-tight">{value}</div>
          {trend && (
            <p className={`text-xs font-medium ${trendUp ? "text-success" : "text-error"}`}>
              {trend}
            </p>
          )}
        </div>
        <div className="w-10 h-10 rounded-full bg-muted flex items-center justify-center shrink-0">
          <Icon className="w-5 h-5 text-muted-foreground" />
        </div>
      </CardContent>
    </Card>
  );
}
