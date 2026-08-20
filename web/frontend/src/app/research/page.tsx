"use client"
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { BookOpen, CheckCircle2, TrendingUp, Cpu, BarChart3 } from 'lucide-react';

export default function Research() {
  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div className="border-b border-border pb-6 mb-8 flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground flex items-center gap-2">
            <BookOpen className="w-6 h-6 text-accent" /> Research Findings
          </h1>
          <p className="text-sm text-muted-foreground mt-2 tracking-wide max-w-2xl">
            These findings represent the official conclusions from the Phase 6 and 7 evaluation of the Genetic Algorithm against the Baseline method.
          </p>
        </div>
        <Badge variant="outline" className="w-fit text-[10px] uppercase bg-muted/50 border-border/50">Official Conclusions</Badge>
      </div>

      <div className="grid gap-6">
        <Card className="border-border hover:border-accent/30 transition-colors">
          <CardHeader className="bg-muted/20 border-b border-border/50 pb-4">
            <CardTitle className="text-sm font-semibold tracking-wide flex items-center gap-2 text-foreground">
              <CheckCircle2 className="w-4 h-4 text-success" /> RQ1: Conflict Reduction
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-6">
            <div className="flex gap-4">
              <div className="w-1 h-full bg-success/20 rounded-full" />
              <p className="text-sm text-muted-foreground leading-relaxed">
                <strong className="text-foreground font-semibold">Observation:</strong> The Genetic Algorithm significantly reduced conflicts across all datasets compared to the baseline method. For the Large dataset, conflicts were reduced by a large margin while allocating substantially more courses.
              </p>
            </div>
          </CardContent>
        </Card>

        <Card className="border-border hover:border-accent/30 transition-colors">
          <CardHeader className="bg-muted/20 border-b border-border/50 pb-4">
            <CardTitle className="text-sm font-semibold tracking-wide flex items-center gap-2 text-foreground">
              <TrendingUp className="w-4 h-4 text-accent" /> RQ2: Classroom Utilization
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-6">
            <div className="flex gap-4">
              <div className="w-1 h-full bg-accent/20 rounded-full" />
              <p className="text-sm text-muted-foreground leading-relaxed">
                <strong className="text-foreground font-semibold">Observation:</strong> The GA improved classroom utilization rates on average, tightly packing schedules more efficiently than the greedy baseline approach.
              </p>
            </div>
          </CardContent>
        </Card>

        <Card className="border-border hover:border-accent/30 transition-colors">
          <CardHeader className="bg-muted/20 border-b border-border/50 pb-4">
            <CardTitle className="text-sm font-semibold tracking-wide flex items-center gap-2 text-foreground">
              <Cpu className="w-4 h-4 text-warning" /> RQ3: Parameter Effects
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-6">
            <div className="flex gap-4">
              <div className="w-1 h-full bg-warning/20 rounded-full" />
              <p className="text-sm text-muted-foreground leading-relaxed">
                <strong className="text-foreground font-semibold">Observation:</strong> Population size and generations directly correlate with fitness, though with diminishing returns and linear increases in execution time. A crossover rate of ~0.8 and mutation rate of ~0.1 provided the most reliable convergence.
              </p>
            </div>
          </CardContent>
        </Card>

        <Card className="border-border hover:border-accent/30 transition-colors">
          <CardHeader className="bg-muted/20 border-b border-border/50 pb-4">
            <CardTitle className="text-sm font-semibold tracking-wide flex items-center gap-2 text-foreground">
              <BarChart3 className="w-4 h-4 text-primary" /> RQ4: Baseline vs GA Performance
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-6">
            <div className="flex gap-4">
              <div className="w-1 h-full bg-primary/20 rounded-full" />
              <p className="text-sm text-muted-foreground leading-relaxed">
                <strong className="text-foreground font-semibold">Observation:</strong> The GA outperforms the Baseline across every metric except execution time. The baseline completes in &lt;1s but yields rigid, high-conflict schedules, whereas the GA takes longer but finds near-optimal, low-conflict solutions.
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
