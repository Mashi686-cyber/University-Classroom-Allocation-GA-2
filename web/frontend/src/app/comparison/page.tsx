"use client"
import { useEffect, useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function Comparison() {
  const [size, setSize] = useState('small');
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    fetch(`http://localhost:8000/api/comparison/${size}`).then(r => r.json()).then(res => {
        setData(res);
    }).catch(() => {});
  }, [size]);

  // Convert raw API map (Baseline/GA keys) into Recharts array
  const chartData = data ? [
    {
      algorithm: "Baseline",
      Conflicts: data.Baseline?.conflicts || 0,
      Utilization: data.Baseline?.utilization_percentage || 0,
      Allocated: data.Baseline?.allocated_courses || 0,
      Time: data.Baseline?.execution_time_s || 0,
    },
    {
      algorithm: "GA",
      Conflicts: data.GA?.conflicts || 0,
      Utilization: data.GA?.utilization_percentage || 0,
      Allocated: data.GA?.allocated_courses || 0,
      Time: data.GA?.execution_time_s || 0,
    }
  ] : [];

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-card border border-border rounded-lg shadow-sm p-3 text-sm">
          <p className="font-semibold mb-1 text-foreground">{label}</p>
          <p className="text-muted-foreground">
            <span style={{ color: payload[0].fill }} className="font-medium">{payload[0].name}:</span> {payload[0].value}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-border pb-6">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground">Baseline vs Genetic Algorithm</h1>
          <p className="text-sm text-muted-foreground mt-1 tracking-wide">Experimental comparison across scheduling datasets.</p>
        </div>
        <div className="flex gap-2 bg-muted p-1 rounded-md w-fit">
           {['small', 'medium', 'large'].map(s => (
             <Button 
               key={s} 
               variant={size === s ? "default" : "ghost"} 
               size="sm" 
               className="capitalize text-xs h-8 px-4"
               onClick={() => setSize(s)}
             >
               {s} Dataset
             </Button>
           ))}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {['Allocated', 'Conflicts', 'Utilization', 'Time'].map(metric => {
          const bValue = data?.Baseline ? (metric === 'Allocated' ? data.Baseline.allocated_courses : metric === 'Conflicts' ? data.Baseline.conflicts : metric === 'Utilization' ? `${data.Baseline.utilization_percentage}%` : `${data.Baseline.execution_time_s}s`) : '--';
          const gaValue = data?.GA ? (metric === 'Allocated' ? data.GA.allocated_courses : metric === 'Conflicts' ? data.GA.conflicts : metric === 'Utilization' ? `${data.GA.utilization_percentage}%` : `${data.GA.execution_time_s}s`) : '--';
          
          return (
            <Card key={metric} className="bg-[#111113]">
              <CardContent className="p-5 space-y-4">
                <h3 className="text-xs font-semibold text-muted-foreground tracking-wider uppercase">{metric}</h3>
                <div className="flex justify-between items-center border-b border-border/50 pb-2">
                  <span className="text-sm text-muted-foreground">Baseline</span>
                  <span className="font-bold text-foreground">{bValue}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-accent font-medium">GA</span>
                  <span className="font-bold text-accent">{gaValue}</span>
                </div>
              </CardContent>
            </Card>
          )
        })}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
        {[
          { title: "Total Conflicts", key: "Conflicts", color: "var(--error)" },
          { title: "Resource Utilization (%)", key: "Utilization", color: "var(--accent)" },
          { title: "Allocated Courses", key: "Allocated", color: "var(--success)" },
          { title: "Execution Time (s)", key: "Time", color: "var(--warning)" }
        ].map(chart => (
          <Card key={chart.title}>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-semibold tracking-wide text-foreground">{chart.title}</CardTitle>
            </CardHeader>
            <CardContent className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData} margin={{ top: 20, right: 30, left: -20, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" vertical={false} />
                  <XAxis dataKey="algorithm" stroke="var(--muted-foreground)" fontSize={12} tickLine={false} axisLine={false} />
                  <YAxis stroke="var(--muted-foreground)" fontSize={12} tickLine={false} axisLine={false} />
                  <Tooltip content={<CustomTooltip />} cursor={{ fill: 'var(--muted)' }} />
                  <Bar dataKey={chart.key} fill={chart.color} radius={[4, 4, 0, 0]} barSize={50} />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
