"use client"
import { useEffect, useState, useMemo } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { useParams } from 'next/navigation';
import { Clock, Users, User, ArrowLeft, AlertTriangle } from 'lucide-react';
import Link from 'next/link';

type TimetableEntry = {
  Course_ID: string;
  Course_Name: string;
  Classroom_ID: string;
  Lecturer_ID: string;
  Student_Group: string;
  Number_of_Students: number;
  Time_Slot_ID: string;
  Classroom_Capacity?: number;
  Required_Room_Type?: string;
  Required_Facilities?: string;
  Duration?: number;
};

type TimeSlot = {
  Time_Slot_ID: string;
  Day: string;
  Start_Time: string;
  End_Time: string;
};

export default function Timetable() {
  const { runId } = useParams();
  const [timetable, setTimetable] = useState<TimetableEntry[]>([]);
  const [timeslots, setTimeslots] = useState<TimeSlot[]>([]);
  const [loading, setLoading] = useState(true);
  const [errorType, setErrorType] = useState<"network" | "format" | "empty" | "not_found" | null>(null);
  const [debugMsg, setDebugMsg] = useState<string>("");

  useEffect(() => {
    const fetchTimetableData = async () => {
      try {
        setLoading(true);
        let runData;
        try {
          const runRes = await fetch(`http://localhost:8000/api/runs/${runId}`);
          if (!runRes.ok) {
            if (runRes.status === 404) {
              setErrorType("not_found");
              setLoading(false);
              return;
            }
            throw new Error("Failed to fetch run details");
          }
          runData = await runRes.json();
        } catch (err: any) {
          setErrorType("network");
          setDebugMsg(err.message);
          setLoading(false);
          return;
        }

        let ttData;
        try {
          // Fetch timetable data
          const ttRes = await fetch(`http://localhost:8000/api/runs/${runId}/timetable`);
          if (!ttRes.ok) throw new Error("Failed to fetch timetable");
          ttData = await ttRes.json();
        } catch (err: any) {
          setErrorType("network");
          setDebugMsg(err.message);
          setLoading(false);
          return;
        }

        if (!Array.isArray(ttData)) {
          setErrorType("format");
          setDebugMsg("Timetable API did not return an array. Backend response may be malformed.");
          setLoading(false);
          return;
        }
        
        if (ttData.length === 0) {
           setErrorType("empty");
           setLoading(false);
           return;
        }

        setTimetable(ttData);

        let tsData;
        try {
          // Fetch timeslots for mapping
          const tsRes = await fetch(`http://localhost:8000/api/datasets/${runData.dataset_size}/timeslots`);
          if (!tsRes.ok) throw new Error("Failed to fetch timeslots");
          tsData = await tsRes.json();
          setTimeslots(tsData);
        } catch (err: any) {
          setErrorType("network");
          setDebugMsg(err.message);
        }
      } catch (err: any) {
        console.error("Error in timetable:", err);
        setErrorType("format");
        setDebugMsg(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchTimetableData();
  }, [runId]);

  const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];
  const times = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"];

  const tsMap = useMemo(() => {
    const map = new Map<string, TimeSlot>();
    timeslots.forEach(ts => map.set(ts.Time_Slot_ID, ts));
    return map;
  }, [timeslots]);

  const getClasses = (day: string, time: string) => {
    if (!Array.isArray(timetable)) return [];
    
    return timetable.filter((t: TimetableEntry) => {
      if (!t.Time_Slot_ID) return false;
      const slotIds = t.Time_Slot_ID.split(',');
      return slotIds.some(slotId => {
        const slot = tsMap.get(slotId);
        return slot && slot.Day === day && slot.Start_Time === time;
      });
    });
  };

  return (
    <div className="space-y-6 max-w-[1400px] mx-auto">
      <div className="border-b border-border pb-6 mb-6">
        <Link href={`/results/${runId}`} className="text-xs text-muted-foreground hover:text-foreground flex items-center gap-1 mb-4 w-fit">
          <ArrowLeft className="w-3 h-3" /> Back to Run Details
        </Link>
        <h1 className="text-2xl font-bold tracking-tight text-foreground">Optimized Timetable</h1>
        <p className="text-sm text-muted-foreground mt-1 tracking-wide">Allocated schedule for run {runId}</p>
      </div>

      {loading ? (
        <div className="flex justify-center p-12 text-muted-foreground">Loading timetable data...</div>
      ) : errorType === "not_found" ? (
        <Card className="border-border bg-card/50">
          <CardContent className="pt-6 flex flex-col items-center gap-2 text-center text-muted-foreground">
            <AlertTriangle className="w-8 h-8 text-muted-foreground/50 mb-2" />
            <h3 className="font-semibold text-foreground">Run Not Found</h3>
            <p className="text-sm">We could not find the requested allocation run (ID: {runId}).</p>
            <Link href="/results">
              <Button variant="outline" className="mt-4">Return to Results</Button>
            </Link>
          </CardContent>
        </Card>
      ) : errorType === "network" ? (
        <Card className="border-error/20 bg-error/5">
          <CardContent className="pt-6 flex items-start gap-4">
            <AlertTriangle className="w-6 h-6 text-error shrink-0 mt-1" />
            <div>
              <h3 className="font-semibold text-error mb-1">API Unreachable</h3>
              <p className="text-sm text-muted-foreground">The application could not reach the backend server to load timetable data. Ensure the backend is running.</p>
              <p className="text-xs text-error mt-2 font-mono">DEBUG: {debugMsg}</p>
            </div>
          </CardContent>
        </Card>
      ) : errorType === "format" ? (
        <Card className="border-error/20 bg-error/5">
          <CardContent className="pt-6 flex items-start gap-4">
            <AlertTriangle className="w-6 h-6 text-error shrink-0 mt-1" />
            <div>
              <h3 className="font-semibold text-error mb-1">Invalid Timetable Response</h3>
              <p className="text-sm text-muted-foreground">The timetable data received from the backend is malformed or in an unexpected format.</p>
              <p className="text-xs text-error mt-2 font-mono">DEBUG: {debugMsg}</p>
            </div>
          </CardContent>
        </Card>
      ) : errorType === "empty" || timetable.length === 0 ? (
        <Card>
          <CardContent className="pt-6 text-center text-muted-foreground">
            No classes have been allocated for this run.
          </CardContent>
        </Card>
      ) : (

      <Card className="border-border bg-card/50">
        <CardContent className="p-0 overflow-x-auto custom-scrollbar">
          <table className="w-full min-w-[1000px] border-collapse text-left">
            <thead>
              <tr>
                <th className="border-b border-r border-border p-3 w-20 bg-muted/50 sticky left-0 z-10 text-center text-xs font-semibold text-muted-foreground uppercase tracking-wider">Time</th>
                {days.map(d => <th key={d} className="border-b border-border p-4 text-sm font-semibold text-foreground tracking-wide">{d}</th>)}
              </tr>
            </thead>
            <tbody>
              {times.map((t, index) => (
                <tr key={t} className="group hover:bg-muted/10 transition-colors">
                  <td className="border-b border-r border-border p-3 align-top sticky left-0 z-10 bg-card/95 text-center">
                    <span className="text-xs font-medium text-muted-foreground">{t}</span>
                  </td>
                  {days.map(d => {
                    const classes = getClasses(d, t);
                    return (
                      <td key={`${d}-${t}`} className="border-b border-border p-2 align-top h-32 relative min-w-[200px]">
                        <div className="flex flex-col gap-2 absolute inset-2 overflow-y-auto custom-scrollbar">
                          {classes.map((c: any, i: number) => (
                            <div key={i} className="p-3 border border-border/60 rounded-lg bg-[#151517] shadow-sm hover:border-accent transition-colors flex flex-col gap-1.5 cursor-pointer">
                              <div className="flex justify-between items-start">
                                <span className="font-bold text-sm tracking-tight text-foreground">{c.Course_ID}</span>
                                <Badge variant="outline" className="text-[9px] bg-background border-border/50">{c.Classroom_ID}</Badge>
                              </div>
                              <div className="text-xs text-muted-foreground font-medium truncate">{c.Course_Name || "Course"}</div>
                              <div className="flex items-center gap-3 mt-1 pt-2 border-t border-border/50 text-[10px] text-muted-foreground">
                                <div className="flex items-center gap-1" title="Lecturer"><User className="w-3 h-3" /> {c.Lecturer_ID}</div>
                                <div className="flex items-center gap-1" title="Student Group"><Users className="w-3 h-3" /> {c.Student_Group}</div>
                              </div>
                            </div>
                          ))}
                        </div>
                      </td>
                    )
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </CardContent>
      </Card>
      )}
    </div>
  )
}
