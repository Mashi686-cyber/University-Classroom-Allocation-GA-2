"use client"
import { useEffect, useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import Link from 'next/link';
import { useParams } from 'next/navigation';
import { AlertTriangle, CheckCircle2, CalendarDays, Loader2, PlayCircle } from 'lucide-react';

const MetricBlock = ({ label, value, error }: { label: string, value: any, error?: boolean }) => (
  <div className="p-4 rounded-xl border border-border bg-muted/20">
    <div className="text-xs font-semibold text-muted-foreground tracking-wider uppercase mb-1">{label}</div>
    <div className={`text-2xl font-bold tracking-tight ${error ? 'text-error' : 'text-foreground'}`}>{value}</div>
  </div>
);

type RunResult = {
  algorithm: string;
  total_courses: number;
  allocated_courses: number;
  unallocated_courses: number;
  classroom_conflicts: number;
  lecturer_conflicts: number;
  student_group_conflicts: number;
  capacity_violations: number;
  facility_violations: number;
  room_type_violations: number;
  availability_violations: number;
  utilization: number;
  fitness: number | null;
  execution_time: number;
  best_chromosome: any[];
};

type RunJob = {
  run_id: string;
  dataset_size: string;
  algorithm: string;
  status: 'queued' | 'running' | 'completed' | 'failed';
  progress: any;
  result?: RunResult | null;
  error?: string | null;
  timestamp: number;
};

export default function RunDetail() {
  const { runId } = useParams();
  const [job, setJob] = useState<RunJob | null>(null);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const res = await fetch(`http://localhost:8000/api/runs/${runId}`);
        const data = await res.json();
        setJob(data);
      } catch (e) {}
    };
    fetchStatus();
    const interval = setInterval(fetchStatus, 2000);
    return () => clearInterval(interval);
  }, [runId]);

  if (!job) return (
    <div className="flex h-[50vh] items-center justify-center flex-col space-y-4">
      <Loader2 className="w-8 h-8 animate-spin text-muted-foreground" />
      <span className="text-sm font-medium text-muted-foreground">Loading run details...</span>
    </div>
  );

  const getStatusVariant = (status: string) => {
    if (status === 'completed') return 'success';
    if (status === 'failed') return 'destructive';
    return 'warning';
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-border pb-6">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground flex items-center gap-2">
            Optimization Results
          </h1>
          <div className="flex items-center gap-2 mt-2">
            <span className="text-xs text-muted-foreground font-mono bg-muted px-2 py-1 rounded">Run ID: {runId}</span>
            <Badge variant="outline" className="capitalize text-[10px]">{job.dataset_size} Dataset</Badge>
            <Badge variant="outline" className="uppercase text-[10px]">{job.algorithm === 'ga' ? 'Genetic Algorithm' : 'Baseline'}</Badge>
            <Badge variant={getStatusVariant(job.status)} className="capitalize text-[10px]">
              {job.status === 'running' && <Loader2 className="w-3 h-3 mr-1 animate-spin" />}
              {job.status}
            </Badge>
          </div>
        </div>
        {job.status === 'completed' && (
           <Link href={`/results/${runId}/timetable`}>
             <Button className="font-semibold text-xs tracking-wide shadow-sm">
               <CalendarDays className="w-4 h-4 mr-2" /> Open Full Timetable
             </Button>
           </Link>
        )}
      </div>
      
      {job.status === 'running' || job.status === 'queued' ? (
         <Card className="border-accent/20 bg-accent/5">
           <CardContent className="pt-8 pb-8 flex flex-col items-center justify-center space-y-6">
             <PlayCircle className="w-12 h-12 text-accent animate-pulse" />
             <div className="text-center space-y-2">
               <h3 className="text-lg font-semibold text-foreground tracking-tight">Optimization Running</h3>
               <p className="text-sm text-muted-foreground">The algorithm is exploring the solution space.</p>
             </div>
             <div className="w-full max-w-md space-y-2">
               <Progress value={undefined} className="h-2 w-full" />
             </div>
           </CardContent>
         </Card>
      ) : job.status === 'failed' ? (
         <Card className="border-error/20 bg-error/5">
           <CardContent className="pt-6 flex items-start gap-4">
             <AlertTriangle className="w-6 h-6 text-error shrink-0 mt-1" />
             <div>
               <h3 className="font-semibold text-error mb-1">Execution Failed</h3>
               <p className="text-sm text-muted-foreground">{job.error || "Unknown error occurred."}</p>
             </div>
           </CardContent>
         </Card>
      ) : !job.result ? (
         <Card className="border-warning/20 bg-warning/5 mt-6">
           <CardContent className="pt-6 flex items-start gap-4">
             <AlertTriangle className="w-6 h-6 text-warning shrink-0 mt-1" />
             <div>
               <h3 className="font-semibold text-warning mb-1">Result Data Unavailable</h3>
               <p className="text-sm text-muted-foreground">The run is marked as completed but the result data could not be found.</p>
             </div>
           </CardContent>
         </Card>
      ) : (
         <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mt-6">
            <MetricBlock label="Allocated" value={`${job.result.allocated_courses} / ${job.result.total_courses}`} />
            <MetricBlock label="Unallocated" value={job.result.unallocated_courses} error={job.result.unallocated_courses > 0} />
            <MetricBlock label="Total Conflicts" value={job.result.classroom_conflicts + job.result.lecturer_conflicts + job.result.student_group_conflicts} error={job.result.classroom_conflicts + job.result.lecturer_conflicts + job.result.student_group_conflicts > 0} />
            <MetricBlock label="Utilization" value={`${(job.result.utilization).toFixed(1)}%`} />
            {job.algorithm === 'ga' && job.result.fitness !== null && (
              <MetricBlock label="Fitness" value={job.result.fitness.toLocaleString()} />
            )}
            <MetricBlock label="Execution Time" value={`${job.result.execution_time.toFixed(2)}s`} />
         </div>
      )}
      
      {job.status === 'completed' && job.result && (
        <Card>
          <CardHeader className="border-b border-border/50">
            <CardTitle className="text-sm tracking-wide font-semibold">Constraint Breakdown</CardTitle>
          </CardHeader>
          <CardContent className="pt-6 space-y-6">
            {[
              { label: 'Classroom Conflicts', val: job.result.classroom_conflicts },
              { label: 'Lecturer Conflicts', val: job.result.lecturer_conflicts },
              { label: 'Student Group Conflicts', val: job.result.student_group_conflicts },
              { label: 'Capacity Violations', val: job.result.capacity_violations },
              { label: 'Facility Violations', val: job.result.facility_violations },
              { label: 'Room Type Violations', val: job.result.room_type_violations },
            ].map((constraint, i) => (
              <div key={i} className="flex flex-col gap-2">
                <div className="flex justify-between items-center text-sm">
                  <span className="font-medium text-muted-foreground">{constraint.label}</span>
                  <div className="flex items-center gap-2">
                    {constraint.val === 0 ? <CheckCircle2 className="w-4 h-4 text-success" /> : <AlertTriangle className="w-4 h-4 text-error" />}
                    <span className={`font-bold ${constraint.val === 0 ? 'text-success' : 'text-error'}`}>{constraint.val}</span>
                  </div>
                </div>
                {/* Visual horizontal bar indicator (100% green if 0, small red chunk if > 0) */}
                <div className="w-full h-2 rounded-full bg-muted overflow-hidden">
                  <div 
                    className={`h-full rounded-full ${constraint.val === 0 ? 'bg-success w-full' : 'bg-error w-1/4'}`} 
                  />
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      )}
    </div>
  )
}
