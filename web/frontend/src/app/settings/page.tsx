"use client"
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Settings, Save, Database, Server } from 'lucide-react';

export default function SettingsPage() {
  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div className="border-b border-border pb-6 mb-8 flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-foreground flex items-center gap-2">
            <Settings className="w-6 h-6 text-accent" /> System Settings
          </h1>
          <p className="text-sm text-muted-foreground mt-2 tracking-wide max-w-2xl">
            Configure system parameters and default dataset paths for UniClass-GA.
          </p>
        </div>
        <Button className="font-semibold text-xs tracking-wide">
          <Save className="w-4 h-4 mr-2" /> Save Configuration
        </Button>
      </div>

      <div className="grid gap-6">
        <Card className="border-border">
          <CardHeader className="bg-muted/20 border-b border-border/50 pb-4">
            <CardTitle className="text-sm font-semibold tracking-wide flex items-center gap-2 text-foreground">
              <Server className="w-4 h-4 text-muted-foreground" /> API Configuration
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-6 space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Backend URL</label>
                <Input defaultValue="http://localhost:8000" />
              </div>
              <div className="space-y-2">
                <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Timeout (ms)</label>
                <Input type="number" defaultValue="30000" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-border">
          <CardHeader className="bg-muted/20 border-b border-border/50 pb-4">
            <CardTitle className="text-sm font-semibold tracking-wide flex items-center gap-2 text-foreground">
              <Database className="w-4 h-4 text-muted-foreground" /> Dataset Paths
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-6 space-y-4">
            <div className="grid grid-cols-1 gap-4">
              <div className="space-y-2">
                <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Small Dataset Directory</label>
                <Input defaultValue="data/generated/small" />
              </div>
              <div className="space-y-2">
                <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Medium Dataset Directory</label>
                <Input defaultValue="data/generated/medium" />
              </div>
              <div className="space-y-2">
                <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Large Dataset Directory</label>
                <Input defaultValue="data/generated/large" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
