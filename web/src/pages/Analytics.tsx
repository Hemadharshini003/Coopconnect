import React from 'react';
import { CoopAnalyticsChart } from '../components/charts/CoopAnalyticsChart';
import { DistrictMap } from '../components/maps/DistrictMap';
import { BarChart3, MapPin, Building2, Users } from 'lucide-react';

export const Analytics: React.FC = () => {
  return (
    <div className="space-y-6">
      
      <div>
        <h1 className="text-xl font-bold text-slate-900 flex items-center space-x-2">
          <BarChart3 className="w-5 h-5 text-coop-dark" />
          <span>District Capacity & Employment Analytics</span>
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Real-time GIS mapping, skill-gap breakdown by category, and placement outcomes for district administrators.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <CoopAnalyticsChart />
        <DistrictMap />
      </div>

      {/* Skill Gap Breakdown Category Table */}
      <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-4">
        <h3 className="text-sm font-bold text-slate-800">Skill Gap Distribution by Category (Nashik District)</h3>
        <div className="space-y-3">
          <div>
            <div className="flex justify-between text-xs font-semibold mb-1">
              <span>Digital Payments & ERP Operation</span>
              <span className="text-rose-600">42% Gap</span>
            </div>
            <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden">
              <div className="bg-rose-500 h-2.5 rounded-full" style={{ width: '42%' }} />
            </div>
          </div>

          <div>
            <div className="flex justify-between text-xs font-semibold mb-1">
              <span>Inventory Management & Stock Ledger</span>
              <span className="text-amber-600">28% Gap</span>
            </div>
            <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden">
              <div className="bg-amber-500 h-2.5 rounded-full" style={{ width: '28%' }} />
            </div>
          </div>

          <div>
            <div className="flex justify-between text-xs font-semibold mb-1">
              <span>Financial Accounting & Reconciliation</span>
              <span className="text-blue-600">18% Gap</span>
            </div>
            <div className="w-full bg-slate-100 h-2.5 rounded-full overflow-hidden">
              <div className="bg-blue-500 h-2.5 rounded-full" style={{ width: '18%' }} />
            </div>
          </div>
        </div>
      </div>

    </div>
  );
};
