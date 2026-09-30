import React, { useEffect, useState } from 'react';
import { apiFetch } from '../services/api';
import { MemberProfile } from '../types';
import { Users, Plus, BrainCircuit, Search, Award } from 'lucide-react';
import { Link } from 'react-router-dom';

export const Members: React.FC = () => {
  const [members, setMembers] = useState<MemberProfile[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const fetchMembers = async () => {
      try {
        const res = await apiFetch('/members');
        setMembers(res.data || []);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchMembers();
  }, []);

  const filtered = members.filter(m =>
    m.full_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    m.membership_number?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-900 flex items-center space-x-2">
            <Users className="w-5 h-5 text-coop-dark" />
            <span>Cooperative Members Directory</span>
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Registered society members, skill readiness scores, and training progress.
          </p>
        </div>
        <Link to="/members/new" className="btn-primary text-xs flex items-center space-x-1.5 self-start">
          <Plus className="w-4 h-4" />
          <span>Add New Member</span>
        </Link>
      </div>

      <div className="relative max-w-md">
        <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Search member by name or ID..."
          className="w-full pl-9 pr-3 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-coop-dark focus:outline-none bg-white"
        />
      </div>

      {loading ? (
        <div className="p-8 text-center text-xs text-slate-500">Loading members...</div>
      ) : (
        <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-xs">
              <thead>
                <tr className="bg-slate-50 border-b border-slate-200 text-slate-600 font-semibold uppercase text-[10px]">
                  <th className="py-3 px-4">Member Name</th>
                  <th className="py-3 px-4">Membership No.</th>
                  <th className="py-3 px-4">Education & Occupation</th>
                  <th className="py-3 px-4">Experience</th>
                  <th className="py-3 px-4">Profile Completion</th>
                  <th className="py-3 px-4 text-right">AI Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filtered.map((m) => (
                  <tr key={m.id} className="hover:bg-slate-50">
                    <td className="py-3 px-4 font-bold text-slate-900">
                      <Link to={`/members/${m.id}`} className="hover:text-coop-dark">
                        {m.full_name || 'Meena Jadhav'}
                      </Link>
                    </td>
                    <td className="py-3 px-4 font-mono text-slate-600">{m.membership_number}</td>
                    <td className="py-3 px-4 text-slate-700">
                      <p className="font-semibold">{m.occupation || 'Dairy Farming'}</p>
                      <p className="text-[10px] text-slate-400">{m.education_level}</p>
                    </td>
                    <td className="py-3 px-4 text-slate-700">{m.years_of_experience} Yrs</td>
                    <td className="py-3 px-4">
                      <div className="w-32 bg-slate-100 rounded-full h-2 overflow-hidden">
                        <div
                          className="bg-coop-emerald h-2 rounded-full"
                          style={{ width: `${m.profile_completion_percentage || 85}%` }}
                        />
                      </div>
                      <span className="text-[10px] font-mono text-slate-500 mt-0.5 block">
                        {m.profile_completion_percentage || 85}%
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right space-x-2">
                      <Link
                        to={`/members/${m.id}/skill-gaps`}
                        className="btn-secondary text-[11px] py-1 px-2.5 inline-flex items-center space-x-1"
                      >
                        <BrainCircuit className="w-3.5 h-3.5 text-coop-dark" />
                        <span>AI Skill Gaps</span>
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

    </div>
  );
};
