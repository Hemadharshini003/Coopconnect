import React from 'react';
import { ShieldCheck, Plus, Lock } from 'lucide-react';

export const AdminUsers: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-xl font-bold text-slate-900 flex items-center space-x-2">
            <ShieldCheck className="w-5 h-5 text-coop-dark" />
            <span>User & RBAC Role Management</span>
          </h1>
          <p className="text-xs text-slate-500 mt-1">Manage system accounts, roles, and district permissions.</p>
        </div>
        <button className="btn-primary text-xs flex items-center space-x-1">
          <Plus className="w-4 h-4" />
          <span>Add System User</span>
        </button>
      </div>

      <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-4 text-xs space-y-2">
        <p className="font-bold text-slate-800">8 Supported System Roles & Isolation Bounds:</p>
        <ul className="grid grid-cols-2 md:grid-cols-4 gap-2 text-slate-600 font-mono">
          <li className="bg-slate-50 p-2 rounded border border-slate-200">1. SUPER_ADMIN</li>
          <li className="bg-slate-50 p-2 rounded border border-slate-200">2. DISTRICT_ADMIN</li>
          <li className="bg-slate-50 p-2 rounded border border-slate-200">3. COOPERATIVE_ADMIN</li>
          <li className="bg-slate-50 p-2 rounded border border-slate-200">4. TRAINER</li>
          <li className="bg-slate-50 p-2 rounded border border-slate-200">5. MEMBER</li>
          <li className="bg-slate-50 p-2 rounded border border-slate-200">6. EMPLOYEE</li>
          <li className="bg-slate-50 p-2 rounded border border-slate-200">7. RECRUITER</li>
          <li className="bg-slate-50 p-2 rounded border border-slate-200">8. AUDITOR</li>
        </ul>
      </div>
    </div>
  );
};
