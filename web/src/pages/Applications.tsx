import React, { useEffect, useState } from 'react';
import { apiFetch } from '../services/api';
import { UserCheck, Clock, CheckCircle, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';

export const Applications: React.FC = () => {
  const [applications, setApplications] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchApps = async () => {
      try {
        const res = await apiFetch('/applications/me');
        setApplications(res.data || []);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchApps();
  }, []);

  return (
    <div className="space-y-6">
      
      <div>
        <h1 className="text-xl font-bold text-slate-900 flex items-center space-x-2">
          <UserCheck className="w-5 h-5 text-coop-dark" />
          <span>My Job & Task Applications</span>
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Track application status, match compatibility scores, and recruiter responses.
        </p>
      </div>

      {loading ? (
        <div className="p-8 text-center text-xs text-slate-500">Loading applications...</div>
      ) : (
        <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
          {applications.length === 0 ? (
            <div className="p-8 text-center text-xs text-slate-500 space-y-3">
              <p>No active job applications found.</p>
              <Link to="/opportunities" className="btn-primary text-xs py-1.5 px-4 inline-block font-bold">
                Browse Available Opportunities
              </Link>
            </div>
          ) : (
            <div className="divide-y divide-slate-100">
              {applications.map((app) => (
                <div key={app.id} className="p-5 flex items-center justify-between">
                  <div>
                    <span className="badge badge-active text-[10px]">Match: {app.match_score}%</span>
                    <h3 className="text-sm font-bold text-slate-900 mt-1">{app.opportunity_title || 'Digital Inventory Assistant'}</h3>
                    <p className="text-xs text-slate-500 mt-0.5">Applied: {new Date(app.applied_at).toLocaleDateString()}</p>
                  </div>

                  <div className="flex items-center space-x-3">
                    <span className="badge badge-pending text-xs">{app.status}</span>
                    <Link to={`/opportunities/${app.opportunity_id}`} className="btn-secondary text-xs py-1 px-3">
                      View Details
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

    </div>
  );
};
