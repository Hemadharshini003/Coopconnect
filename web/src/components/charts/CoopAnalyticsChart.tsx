import React from 'react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, Legend } from 'recharts';

const sampleData = [
  { month: 'Jan', trained: 45, placed: 38, skillScore: 72 },
  { month: 'Feb', trained: 60, placed: 52, skillScore: 76 },
  { month: 'Mar', trained: 80, placed: 74, skillScore: 82 },
  { month: 'Apr', trained: 95, placed: 88, skillScore: 85 },
  { month: 'May', trained: 120, placed: 105, skillScore: 89 },
  { month: 'Jun', trained: 142, placed: 128, skillScore: 92 },
];

export const CoopAnalyticsChart: React.FC = () => {
  return (
    <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
      <h3 className="text-sm font-bold text-slate-800 mb-4 flex items-center justify-between">
        <span>Capacity Building & Placement Outcomes (Nashik District)</span>
        <span className="text-xs font-normal text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full">Monthly Progress</span>
      </h3>
      <div className="h-64 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={sampleData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
            <XAxis dataKey="month" tick={{ fontSize: 12 }} />
            <YAxis tick={{ fontSize: 12 }} />
            <Tooltip contentStyle={{ backgroundColor: '#ffffff', borderRadius: '8px', border: '1px solid #cbd5e1' }} />
            <Legend wrapperStyle={{ fontSize: 12 }} />
            <Bar dataKey="trained" name="Trained Members" fill="#0F5A47" radius={[4, 4, 0, 0]} />
            <Bar dataKey="placed" name="Matched Placements" fill="#D97706" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
