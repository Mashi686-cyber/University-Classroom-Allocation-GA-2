import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

interface OptimizationChartProps {
  data: any;
}

export function OptimizationChart({ data }: OptimizationChartProps) {
  if (!data) return <div className="text-sm text-muted-foreground flex items-center justify-center h-[300px]">No data available</div>;

  const chartData = [
    {
      name: "Conflicts",
      Baseline: data.Baseline?.conflicts || 0,
      GA: data.GA?.conflicts || 0,
    },
    {
      name: "Unallocated",
      Baseline: (data.Baseline?.total_courses || 0) - (data.Baseline?.allocated_courses || 0),
      GA: (data.GA?.total_courses || 0) - (data.GA?.allocated_courses || 0),
    }
  ];

  return (
    <div className="w-full h-[300px] mt-4">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={chartData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" vertical={false} />
          <XAxis dataKey="name" stroke="var(--muted-foreground)" fontSize={12} tickLine={false} axisLine={false} />
          <YAxis stroke="var(--muted-foreground)" fontSize={12} tickLine={false} axisLine={false} />
          <Tooltip 
            cursor={{ fill: 'var(--muted)' }}
            contentStyle={{ backgroundColor: 'var(--card)', borderColor: 'var(--border)', borderRadius: '8px', color: 'var(--foreground)' }}
            itemStyle={{ fontSize: '13px' }}
          />
          <Legend wrapperStyle={{ fontSize: '13px', paddingTop: '10px' }} />
          <Bar dataKey="Baseline" fill="var(--muted-foreground)" radius={[4, 4, 0, 0]} barSize={40} />
          <Bar dataKey="GA" fill="var(--accent)" radius={[4, 4, 0, 0]} barSize={40} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
