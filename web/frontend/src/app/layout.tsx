import "./globals.css";
import { Sidebar } from "@/components/layout/Sidebar";
import { TopHeader } from "@/components/layout/TopHeader";
import { Inter } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
});

export const metadata = {
  title: "UniClass GA",
  description: "University Classroom Allocation Optimization",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${inter.variable}`}>
      <body className="flex min-h-screen bg-background text-foreground antialiased selection:bg-accent/30 overflow-hidden">
        <Sidebar />
        <div className="flex-1 flex flex-col h-screen">
          <TopHeader />
          <main className="flex-1 p-6 md:p-8 overflow-auto">
            <div className="mx-auto max-w-7xl">
              {children}
            </div>
          </main>
        </div>
      </body>
    </html>
  );
}
