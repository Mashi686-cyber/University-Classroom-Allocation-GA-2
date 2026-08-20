"use client"
import { useEffect, useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { CheckCircle2, AlertTriangle, Search, Filter } from 'lucide-react';
import { Input } from '@/components/ui/input';

type Course = {
  Course_ID: string;
  Course_Name: string;
  Student_Group: string;
  Number_of_Students: number | string;
  Duration: number | string;
};

type Classroom = {
  Classroom_ID: string;
  Capacity: number | string;
  Room_Type: string;
};

export default function Datasets() {
  const [size, setSize] = useState('small');
  const [courses, setCourses] = useState<Course[]>([]);
  const [classrooms, setClassrooms] = useState<Classroom[]>([]);
  const [search, setSearch] = useState('');
  const [validation, setValidation] = useState<any>(null);

  useEffect(() => {
    fetch(`http://localhost:8000/api/datasets/${size}/courses`).then(r => r.json()).then(setCourses).catch(() => {});
    fetch(`http://localhost:8000/api/datasets/${size}/classrooms`).then(r => r.json()).then(setClassrooms).catch(() => {});
    setValidation(null);
  }, [size]);

  const validate = async () => {
    try {
      const res = await fetch(`http://localhost:8000/api/datasets/${size}/validate`, { method: 'POST' });
      const data = await res.json();
      setValidation(data);
    } catch (e) {
      setValidation({ status: 'ERROR', message: 'Could not connect to backend' });
    }
  };

  const filteredCourses = courses.filter((c: Course) => 
    c.Course_ID.toLowerCase().includes(search.toLowerCase()) || 
    c.Course_Name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-border pb-6">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground">Datasets</h1>
          <p className="text-sm text-muted-foreground mt-1 tracking-wide">Manage and inspect university scheduling datasets.</p>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="secondary" onClick={validate} className="font-semibold text-xs tracking-wide">
            Validate Integrity
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {['small', 'medium', 'large'].map((s) => (
          <Card 
            key={s} 
            className={`cursor-pointer transition-colors ${size === s ? 'border-accent bg-accent/5' : 'hover:border-muted-foreground/30'}`}
            onClick={() => setSize(s)}
          >
            <CardHeader className="pb-3">
              <div className="flex justify-between items-center">
                <CardTitle className="capitalize text-lg font-semibold tracking-tight">{s} Dataset</CardTitle>
                {size === s && <Badge variant="default" className="text-[10px] uppercase">Active</Badge>}
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between text-muted-foreground"><span className="font-medium">Courses</span> <span>{s === 'small' ? '20' : s === 'medium' ? '50' : '100'}</span></div>
                <div className="flex justify-between text-muted-foreground"><span className="font-medium">Classrooms</span> <span>{s === 'small' ? '5' : s === 'medium' ? '12' : '20'}</span></div>
                <div className="flex justify-between text-muted-foreground"><span className="font-medium">Lecturers</span> <span>{s === 'small' ? '10' : s === 'medium' ? '25' : '50'}</span></div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {validation && (
        <Card className={validation.status === 'PASS' ? 'border-success bg-success/5' : 'border-error bg-error/5'}>
           <CardContent className="pt-6">
             <div className="flex items-center gap-3">
                {validation.status === 'PASS' ? <CheckCircle2 className="w-5 h-5 text-success" /> : <AlertTriangle className="w-5 h-5 text-error" />}
                <span className={`text-sm font-medium ${validation.status === 'PASS' ? 'text-success' : 'text-error'}`}>{validation.message}</span>
             </div>
           </CardContent>
        </Card>
      )}

      <Tabs defaultValue="courses" className="w-full">
        <TabsList className="mb-4">
          <TabsTrigger value="courses">Courses</TabsTrigger>
          <TabsTrigger value="classrooms">Classrooms</TabsTrigger>
          <TabsTrigger value="lecturers">Lecturers</TabsTrigger>
          <TabsTrigger value="students">Student Groups</TabsTrigger>
        </TabsList>
        
        <TabsContent value="courses">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between py-4 border-b border-border">
              <CardTitle className="text-sm font-semibold tracking-wide text-foreground">Course Data</CardTitle>
              <div className="relative w-64">
                <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                <Input placeholder="Search courses..." className="pl-8 h-9 text-xs" value={search} onChange={(e) => setSearch(e.target.value)} />
              </div>
            </CardHeader>
            <CardContent className="p-0">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="w-[100px]">Course ID</TableHead>
                    <TableHead>Course Name</TableHead>
                    <TableHead>Student Group</TableHead>
                    <TableHead>Students</TableHead>
                    <TableHead>Duration</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredCourses.map((c: Course) => (
                    <TableRow key={c.Course_ID}>
                      <TableCell className="font-medium">{c.Course_ID}</TableCell>
                      <TableCell>{c.Course_Name}</TableCell>
                      <TableCell><Badge variant="outline">{c.Student_Group}</Badge></TableCell>
                      <TableCell>{c.Number_of_Students}</TableCell>
                      <TableCell>{c.Duration} hours</TableCell>
                    </TableRow>
                  ))}
                  {filteredCourses.length === 0 && (
                    <TableRow>
                      <TableCell colSpan={5} className="h-24 text-center text-muted-foreground">
                        No courses found.
                      </TableCell>
                    </TableRow>
                  )}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="classrooms">
          <Card>
            <CardHeader className="py-4 border-b border-border">
              <CardTitle className="text-sm font-semibold tracking-wide text-foreground">Classroom Data</CardTitle>
            </CardHeader>
            <CardContent className="p-0">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="w-[120px]">Room ID</TableHead>
                    <TableHead>Capacity</TableHead>
                    <TableHead>Room Type</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {classrooms.map((c: Classroom) => (
                    <TableRow key={c.Classroom_ID}>
                      <TableCell className="font-medium">{c.Classroom_ID}</TableCell>
                      <TableCell>{c.Capacity}</TableCell>
                      <TableCell><Badge variant="outline">{c.Room_Type}</Badge></TableCell>
                    </TableRow>
                  ))}
                  {classrooms.length === 0 && (
                    <TableRow>
                      <TableCell colSpan={3} className="h-24 text-center text-muted-foreground">
                        No classrooms loaded.
                      </TableCell>
                    </TableRow>
                  )}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
