"use client"
import { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { useRouter } from 'next/navigation';
import { Play, Settings2, Zap, Beaker } from 'lucide-react';

export default function Allocation() {
  const router = useRouter();
  const [config, setConfig] = useState<any>({
    population_size: 50, generations: 50, crossover_rate: 0.8, mutation_rate: 0.1, elitism: 2, random_seed: 42
  });
  const [dataset, setDataset] = useState('small');
  const [algo, setAlgo] = useState('ga');

  const run = async () => {
    const res = await fetch('http://localhost:8000/api/runs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        dataset_size: dataset,
        algorithm: algo,
        ...config
      })
    });
    const data = await res.json();
    router.push(`/results/${data.run_id}`);
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div className="border-b border-border pb-6 mb-6">
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Classroom Allocation</h1>
        <p className="text-sm text-muted-foreground mt-1 tracking-wide">Configure and execute an allocation algorithm.</p>
      </div>

      <div className="flex gap-2 bg-muted p-1 rounded-md w-fit mb-8">
        {['small', 'medium', 'large'].map(s => (
          <Button 
            key={s} 
            variant={dataset === s ? "default" : "ghost"} 
            size="sm" 
            className="capitalize text-xs h-8 px-6"
            onClick={() => setDataset(s)}
          >
            {s} Dataset
          </Button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card 
          className={`cursor-pointer transition-all ${algo === 'baseline' ? 'border-accent shadow-sm shadow-accent/20' : 'hover:border-muted-foreground/30'}`}
          onClick={() => setAlgo('baseline')}
        >
          <CardHeader className="pb-3 border-b border-border/50">
            <div className="flex justify-between items-start">
              <div className="space-y-1">
                <CardTitle className="text-sm font-semibold tracking-wide flex items-center gap-2">
                  <Zap className="w-4 h-4 text-warning" /> BASELINE
                </CardTitle>
              </div>
            </div>
          </CardHeader>
          <CardContent className="pt-4 pb-6">
            <h3 className="font-semibold text-foreground mb-1">Sequential Greedy Allocation</h3>
            <p className="text-sm text-muted-foreground">Fast deterministic heuristic. Uses a standard sorting and assignment pipeline. Suitable for comparison baselines.</p>
          </CardContent>
        </Card>

        <Card 
          className={`cursor-pointer transition-all ${algo === 'ga' ? 'border-accent bg-accent/5 shadow-sm shadow-accent/20' : 'hover:border-muted-foreground/30'}`}
          onClick={() => setAlgo('ga')}
        >
          <CardHeader className="pb-3 border-b border-border/50">
            <div className="flex justify-between items-start">
              <div className="space-y-1">
                <CardTitle className="text-sm font-semibold tracking-wide flex items-center gap-2">
                  <Beaker className="w-4 h-4 text-accent" /> GENETIC ALGORITHM
                </CardTitle>
              </div>
              <Badge variant="default" className="text-[10px] uppercase bg-accent text-accent-foreground">Research Method</Badge>
            </div>
          </CardHeader>
          <CardContent className="pt-4 pb-6">
            <h3 className="font-semibold text-foreground mb-1">Population-based Optimization</h3>
            <p className="text-sm text-muted-foreground">Evolves high-quality timetables through selection, crossover, and mutation over multiple generations.</p>
          </CardContent>
        </Card>
      </div>

      {algo === 'ga' && (
        <Card className="border-accent/20 shadow-sm mt-6">
          <CardHeader className="border-b border-border/50 bg-muted/20 pb-4">
            <CardTitle className="text-sm font-semibold flex items-center gap-2">
              <Settings2 className="w-4 h-4 text-muted-foreground" /> GA Configuration
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-6">
            <div className="grid grid-cols-2 lg:grid-cols-3 gap-6">
              <div className="space-y-2">
                <label className="text-xs font-semibold text-muted-foreground tracking-wide uppercase">Population Size</label>
                <Input type="number" value={config.population_size} onChange={e => setConfig({...config, population_size: parseInt(e.target.value)})} />
              </div>
              <div className="space-y-2">
                <label className="text-xs font-semibold text-muted-foreground tracking-wide uppercase">Generations</label>
                <Input type="number" value={config.generations} onChange={e => setConfig({...config, generations: parseInt(e.target.value)})} />
              </div>
              <div className="space-y-2">
                <label className="text-xs font-semibold text-muted-foreground tracking-wide uppercase">Crossover Rate</label>
                <Input type="number" step="0.1" value={config.crossover_rate} onChange={e => setConfig({...config, crossover_rate: parseFloat(e.target.value)})} />
              </div>
              <div className="space-y-2">
                <label className="text-xs font-semibold text-muted-foreground tracking-wide uppercase">Mutation Rate</label>
                <Input type="number" step="0.01" value={config.mutation_rate} onChange={e => setConfig({...config, mutation_rate: parseFloat(e.target.value)})} />
              </div>
              <div className="space-y-2">
                <label className="text-xs font-semibold text-muted-foreground tracking-wide uppercase">Elite Count</label>
                <Input type="number" value={config.elitism} onChange={e => setConfig({...config, elitism: parseInt(e.target.value)})} />
              </div>
              <div className="space-y-2">
                <label className="text-xs font-semibold text-muted-foreground tracking-wide uppercase">Random Seed</label>
                <Input type="number" value={config.random_seed} onChange={e => setConfig({...config, random_seed: parseInt(e.target.value)})} />
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      <div className="pt-6 border-t border-border mt-8 flex flex-col sm:flex-row justify-between items-center gap-4">
        <p className="text-xs text-muted-foreground">
          {algo === 'ga' ? "Parameters can affect convergence, runtime, and solution quality." : "Deterministic algorithm runs instantly without configuration."}
        </p>
        <Button onClick={run} size="lg" className="w-full sm:w-auto font-semibold tracking-wide">
          <Play className="w-4 h-4 mr-2" /> 
          Run {algo === 'ga' ? 'Genetic Algorithm' : 'Baseline'}
        </Button>
      </div>
    </div>
  )
}
