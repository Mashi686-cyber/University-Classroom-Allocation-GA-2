"use client"
import { useEffect, useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Users, MonitorPlay, Presentation } from 'lucide-react';
import Link from 'next/link';

type Classroom = {
  Classroom_ID: string;
  Capacity: string | number;
  Room_Type: string;
  Facilities: string;
  Availability: string;
};

export default function ClassroomsPage() {
  const [classrooms, setClassrooms] = useState<Classroom[]>([]);
  const [size, setSize] = useState('small');

  useEffect(() => {
    fetch(`http://localhost:8000/api/datasets/${size}/classrooms`)
      .then(r => r.json())
      .then(setClassrooms)
      .catch(() => {});
  }, [size]);

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-border pb-6">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground">Classrooms</h1>
          <p className="text-sm text-muted-foreground mt-1 tracking-wide">University campus infrastructure and utilization.</p>
        </div>
        <div className="flex gap-2 bg-muted p-1 rounded-md">
           {['small', 'medium', 'large'].map(s => (
             <Button 
               key={s} 
               variant={size === s ? "default" : "ghost"} 
               size="sm" 
               className="capitalize text-xs h-8"
               onClick={() => setSize(s)}
             >
               {s}
             </Button>
           ))}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {classrooms.map((c: Classroom) => (
          <Card key={c.Classroom_ID} className="flex flex-col hover:border-accent/50 transition-colors">
            <CardHeader className="pb-3 border-b border-border bg-muted/20">
              <div className="flex justify-between items-center">
                <CardTitle className="text-lg tracking-tight font-bold text-foreground">{c.Classroom_ID}</CardTitle>
                <Badge variant="outline" className="text-[10px] bg-background">{c.Room_Type}</Badge>
              </div>
            </CardHeader>
            <CardContent className="pt-4 flex-1 space-y-4">
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground flex items-center gap-2"><Users className="w-4 h-4" /> Capacity</span>
                <span className="font-semibold">{c.Capacity} seats</span>
              </div>
              
              <div className="space-y-2">
                <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Facilities</span>
                <div className="flex flex-wrap gap-2">
                  <Badge variant="secondary" className="text-[10px]"><Presentation className="w-3 h-3 mr-1" /> Whiteboard</Badge>
                  {Number(c.Capacity) > 40 && <Badge variant="secondary" className="text-[10px]"><MonitorPlay className="w-3 h-3 mr-1" /> Projector</Badge>}
                </div>
              </div>

              <div className="pt-4 mt-auto border-t border-border/50">
                <Link href={`/results/latest/timetable?room=${c.Classroom_ID}`}>
                  <Button variant="secondary" className="w-full text-xs h-8">View Schedule →</Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
