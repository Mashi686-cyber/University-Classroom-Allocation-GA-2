"use client"
import { useEffect, useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { MetricCard } from '@/components/dashboard/MetricCard';
import { PlayCircle, Database, LayoutGrid, CheckCircle2, TrendingUp, AlertTriangle, Play, Activity } from 'lucide-react';
import Link from 'next/link';
import { OptimizationChart } from '@/components/dashboard/OptimizationChart';

export default function Dashboard() {
  const [datasets, setDatasets] = useState<any[]>([]);
  const [comparison, setComparison] = useState<any>(null);

  useEffect(() => {
    fetch('http://localhost:8000/api/datasets').then(r => r.json()).then(setDatasets).catch(() => {});
    fetch('http://localhost:8000/api/comparison/small').then(r => r.json()).then(setComparison).catch(() => {});
  }, []);

  const smallData = datasets.find(d => d.size === 'small');
  
  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground">Dashboard</h1>
          <p className="text-sm text-muted-foreground mt-1 tracking-wide">University Classroom Allocation Optimization</p>
        </div>
        <div className="flex items-center gap-3">
          <Link href="/allocation">
            <Button variant="secondary" className="font-semibold text-xs tracking-wide">
              Run Baseline
            </Button>
          </Link>
          <Link href="/allocation">
            <Button className="font-semibold text-xs tracking-wide shadow-sm">
              <Play className="w-4 h-4 mr-2" /> Run Genetic Algorithm
            </Button>
          </Link>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <MetricCard title="Total Courses" value={smallData?.courses_count || "--"} icon={Database} />
        <MetricCard title="Classrooms" value={smallData?.classrooms_count || "--"} icon={LayoutGrid} />
        <MetricCard title="Allocated" value={comparison?.GA?.allocated_courses || "--"} icon={CheckCircle2} />
        <MetricCard title="Conflicts" value={comparison?.GA?.conflicts !== undefined ? comparison?.GA?.conflicts : "--"} icon={AlertTriangle} trend={comparison?.GA?.conflicts === 0 ? "Perfect" : ""} trendUp={comparison?.GA?.conflicts === 0} />
        <MetricCard title="Utilization" value={comparison?.GA?.utilization_percentage ? `${comparison.GA.utilization_percentage}%` : "--"} icon={TrendingUp} trend="Active" trendUp={true} />
        <MetricCard title="Best Fitness" value={comparison?.GA?.fitness ? comparison.GA.fitness.toLocaleString() : "--"} icon={Activity} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="col-span-1 lg:col-span-2 flex flex-col">
          <CardHeader>
            <CardTitle className="text-sm tracking-wide text-foreground font-semibold">Optimization Performance</CardTitle>
          </CardHeader>
          <CardContent className="flex-1 flex items-center justify-center min-h-[300px] pb-6">
            <OptimizationChart data={comparison} />
          </CardContent>
        </Card>
        
        <Card className="col-span-1 bg-[#111113] flex flex-col">
          <CardHeader>
            <CardTitle className="text-sm tracking-wide text-foreground font-semibold">Latest Optimization</CardTitle>
          </CardHeader>
          <CardContent className="flex-1 space-y-4">
            <div className="flex justify-between items-center py-2 border-b border-border">
              <span className="text-xs text-muted-foreground">Algorithm</span>
              <span className="text-sm font-medium">Genetic Algorithm</span>
            </div>
            <div className="flex justify-between items-center py-2 border-b border-border">
              <span className="text-xs text-muted-foreground">Dataset</span>
              <Badge variant="outline" className="text-xs">Small</Badge>
            </div>
            <div className="flex justify-between items-center py-2 border-b border-border">
              <span className="text-xs text-muted-foreground">Allocated</span>
              <span className="text-sm font-medium text-success">{comparison?.GA?.allocated_courses || 0} / {smallData?.courses_count || 0}</span>
            </div>
            <div className="flex justify-between items-center py-2 border-b border-border">
              <span className="text-xs text-muted-foreground">Conflicts</span>
              <span className="text-sm font-medium">{comparison?.GA?.conflicts || 0}</span>
            </div>
            <div className="flex justify-between items-center py-2">
              <span className="text-xs text-muted-foreground">Utilization</span>
              <span className="text-sm font-medium">{comparison?.GA?.utilization_percentage || 0}%</span>
            </div>
            <div className="pt-4">
              <Link href="/results/latest">
                <Button variant="secondary" className="w-full text-xs">View Result →</Button>
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="text-sm tracking-wide font-semibold">Optimization Progress</CardTitle>
          </CardHeader>
          <CardContent className="min-h-[200px] flex items-center justify-center border-t border-border mt-2 pt-6">
            <div className="text-sm text-muted-foreground">Line Chart Placeholder</div>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader>
            <CardTitle className="text-sm tracking-wide font-semibold">Constraint Status</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3 pt-4">
            {[
              { name: "Classroom Conflicts", val: 0 },
              { name: "Lecturer Conflicts", val: 0 },
              { name: "Student Group Conflicts", val: 0 },
              { name: "Capacity Violations", val: 0 },
              { name: "Facility Violations", val: 0 },
            ].map(c => (
              <div key={c.name} className="flex justify-between items-center p-3 rounded-lg bg-muted/50 border border-border/50">
                <span className="text-sm text-muted-foreground">{c.name}</span>
                <div className="flex items-center gap-2">
                  {c.val === 0 ? <CheckCircle2 className="w-4 h-4 text-success" /> : <AlertTriangle className="w-4 h-4 text-error" />}
                  <span className={`text-sm font-bold ${c.val === 0 ? "text-success" : "text-error"}`}>{c.val}</span>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-sm tracking-wide font-semibold">Recent Runs</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Run</TableHead>
                <TableHead>Dataset</TableHead>
                <TableHead>Algorithm</TableHead>
                <TableHead>Allocated</TableHead>
                <TableHead>Conflicts</TableHead>
                <TableHead>Time</TableHead>
                <TableHead>Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              <TableRow>
                <TableCell className="font-medium text-xs">GA-0042</TableCell>
                <TableCell><Badge variant="outline">Small</Badge></TableCell>
                <TableCell className="text-xs">Genetic Algorithm</TableCell>
                <TableCell className="text-xs">17</TableCell>
                <TableCell className="text-xs text-success">0</TableCell>
                <TableCell className="text-xs">0.32s</TableCell>
                <TableCell><Badge variant="success">Completed</Badge></TableCell>
              </TableRow>
              <TableRow>
                <TableCell className="font-medium text-xs">BL-0041</TableCell>
                <TableCell><Badge variant="outline">Small</Badge></TableCell>
                <TableCell className="text-xs">Baseline</TableCell>
                <TableCell className="text-xs">17</TableCell>
                <TableCell className="text-xs text-error">8</TableCell>
                <TableCell className="text-xs">&lt;0.01s</TableCell>
                <TableCell><Badge variant="success">Completed</Badge></TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}
