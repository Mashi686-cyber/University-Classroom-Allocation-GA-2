"use client"
import { useEffect, useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { ArrowRight, CheckCircle2, Clock, XCircle } from 'lucide-react';
import Link from 'next/link';

export default function Results() {
  const [runs, setRuns] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8000/api/runs').then(r => r.json()).then(setRuns).catch(() => {});
  }, []);

  const getStatusIcon = (status: string) => {
    if (status === 'completed') return <CheckCircle2 className="w-3 h-3 mr-1" />;
    if (status === 'failed') return <XCircle className="w-3 h-3 mr-1" />;
    return <Clock className="w-3 h-3 mr-1" />;
  }

  const getStatusVariant = (status: string) => {
    if (status === 'completed') return 'success';
    if (status === 'failed') return 'destructive';
    return 'warning';
  }

  return (
    <div className="space-y-6">
      <div className="border-b border-border pb-6 mb-6">
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Optimization Results</h1>
        <p className="text-sm text-muted-foreground mt-1 tracking-wide">Historical logs of baseline and genetic algorithm executions.</p>
      </div>

      <Card>
        <CardContent className="p-0">
          <Table>
            <TableHeader>
              <TableRow className="bg-muted/30">
                <TableHead className="w-[150px]">Run ID</TableHead>
                <TableHead>Algorithm</TableHead>
                <TableHead>Dataset</TableHead>
                <TableHead>Execution Date</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">Action</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {runs.map((r: any) => (
                <TableRow key={r.run_id} className="group hover:bg-muted/10 cursor-pointer">
                  <TableCell className="font-mono text-xs text-muted-foreground">{r.run_id.substring(0, 8)}...</TableCell>
                  <TableCell>
                    <div className="flex items-center gap-2">
                      <span className="font-medium text-sm text-foreground uppercase tracking-wider">{r.algorithm === 'ga' ? 'Genetic Algorithm' : 'Baseline'}</span>
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge variant="outline" className="capitalize text-[10px]">{r.dataset_size}</Badge>
                  </TableCell>
                  <TableCell className="text-xs text-muted-foreground">
                    {new Date(r.timestamp * 1000).toLocaleString(undefined, {
                      year: 'numeric', month: 'short', day: 'numeric',
                      hour: '2-digit', minute: '2-digit'
                    })}
                  </TableCell>
                  <TableCell>
                    <Badge variant={getStatusVariant(r.status)} className="capitalize text-[10px] flex w-fit items-center">
                      {getStatusIcon(r.status)}
                      {r.status}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right">
                    <Link href={`/results/${r.run_id}`}>
                      <Button size="sm" variant="ghost" className="opacity-0 group-hover:opacity-100 transition-opacity">
                        View Details <ArrowRight className="w-4 h-4 ml-1" />
                      </Button>
                    </Link>
                  </TableCell>
                </TableRow>
              ))}
              {runs.length === 0 && (
                <TableRow>
                  <TableCell colSpan={6} className="h-32 text-center">
                    <div className="flex flex-col items-center justify-center space-y-3">
                      <p className="text-muted-foreground text-sm">No optimization runs found in history.</p>
                      <Link href="/allocation"><Button variant="secondary" size="sm">Run Allocation</Button></Link>
                    </div>
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}
