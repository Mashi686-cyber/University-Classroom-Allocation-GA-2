"use client"
import { useEffect, useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs';

export default function Experiments() {
  const [data, setData] = useState<any>({});

  useEffect(() => {
    fetch('http://localhost:8000/api/experiments').then(r => r.json()).then(res => {
       const parsed: any = {};
       for (const k in res) {
           parsed[k] = res[k].map((row: any) => {
               const newRow: any = {};
               for (const key in row) {
                   newRow[key] = parseFloat(row[key]) || row[key];
               }
               return newRow;
           });
       }
       setData(parsed);
    }).catch(() => {});
  }, []);

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-card border border-border rounded-lg shadow-sm p-3 text-sm">
          <p className="font-semibold mb-1 text-foreground">{label}</p>
          {payload.map((entry: any, index: number) => (
            <p key={index} className="text-muted-foreground">
              <span style={{ color: entry.color }} className="font-medium">{entry.name}:</span> {entry.value}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  const renderChart = (dataset: any[], xKey: string, yKey: string, color: string) => (
    <ResponsiveContainer width="100%" height="100%">
      <LineChart data={dataset} margin={{ top: 20, right: 30, left: -20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" vertical={false} />
        <XAxis dataKey={xKey} stroke="var(--muted-foreground)" fontSize={12} tickLine={false} axisLine={false} />
        <YAxis stroke="var(--muted-foreground)" fontSize={12} tickLine={false} axisLine={false} />
        <Tooltip content={<CustomTooltip />} cursor={{ stroke: 'var(--muted)', strokeWidth: 2 }} />
        <Legend wrapperStyle={{ fontSize: '13px', paddingTop: '10px' }} />
        <Line type="monotone" dataKey={yKey} stroke={color} strokeWidth={2} dot={{ r: 4, fill: 'var(--card)', strokeWidth: 2 }} activeDot={{ r: 6 }} />
      </LineChart>
    </ResponsiveContainer>
  );

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      <div className="border-b border-border pb-6 mb-6">
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Parameter Experiments</h1>
        <p className="text-sm text-muted-foreground mt-1 tracking-wide">Phase 5 empirical analysis on parameter sensitivities.</p>
      </div>
      
      <Tabs defaultValue="population_size_results" className="w-full">
        <TabsList className="mb-6 bg-muted/50 border border-border p-1 w-full sm:w-auto overflow-x-auto justify-start">
          <TabsTrigger value="population_size_results">Population Size</TabsTrigger>
          <TabsTrigger value="generations_results">Generations</TabsTrigger>
          <TabsTrigger value="crossover_rate_results">Crossover Rate</TabsTrigger>
          <TabsTrigger value="mutation_rate_results">Mutation Rate</TabsTrigger>
        </TabsList>

        {Object.keys(data).map(param => {
          const xKey = param.replace('_results', '');
          return (
            <TabsContent key={param} value={param}>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Card>
                  <CardHeader className="border-b border-border/50 pb-4">
                    <CardTitle className="text-sm font-semibold tracking-wide text-foreground">Fitness over {xKey.replace('_', ' ')}</CardTitle>
                  </CardHeader>
                  <CardContent className="h-80 pt-6">
                      {renderChart(data[param], xKey, 'fitness', 'var(--success)')}
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader className="border-b border-border/50 pb-4">
                    <CardTitle className="text-sm font-semibold tracking-wide text-foreground">Execution Time (s) over {xKey.replace('_', ' ')}</CardTitle>
                  </CardHeader>
                  <CardContent className="h-80 pt-6">
                      {renderChart(data[param], xKey, 'execution_time', 'var(--warning)')}
                  </CardContent>
                </Card>
              </div>
            </TabsContent>
          )
        })}
      </Tabs>
    </div>
  )
}
