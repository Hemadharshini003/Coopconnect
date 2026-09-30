import React, { useEffect, useState } from 'react';
import { apiFetch } from '../services/api';
import { Opportunity } from '../types';
import { Briefcase, MapPin, DollarSign, Plus, Sparkles, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';

export const Opportunities: React.FC = () => {
  const [opportunities, setOpportunities] = useState<Opportunity[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchOpps = async () => {
      try {
        const res = await apiFetch('/opportunities');
        setOpportunities(res.data || []);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchOpps();
  }, []);

  return (
    <div className="space-y-6">
      
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-900 flex items-center space-x-2">
            <Briefcase className="w-5 h-5 text-coop-dark" />
            <span>Cooperative Employment & Task Opportunities</span>
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            AI-matched job positions, apprenticeships, and task assignments across cooperative societies.
          </p>
        </div>
        <button className="btn-primary text-xs flex items-center space-x-1.5 self-start">
          <Plus className="w-4 h-4" />
          <span>Post New Opportunity</span>
        </button>
      </div>

      {loading ? (
        <div className="p-8 text-center text-xs text-slate-500">Loading opportunities...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {opportunities.map((opp) => (
            <div key={opp.id} className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm hover:border-coop-dark transition-all flex flex-col justify-between space-y-4">
              <div>
                <div className="flex items-center justify-between">
                  <span className="badge badge-active text-[10px]">{opp.opportunity_type}</span>
                  <span className="text-[10px] font-mono text-emerald-700 font-bold bg-emerald-50 px-2 py-0.5 rounded-full">
                    92.5% AI Match
                  </span>
                </div>
                <h3 className="text-base font-bold text-slate-900 mt-2">
                  <Link to={`/opportunities/${opp.id}`} className="hover:text-coop-dark">{opp.title}</Link>
                </h3>
                <p className="text-xs text-slate-600 mt-1 line-clamp-2">{opp.description}</p>
              </div>

              <div className="space-y-2 border-t border-slate-100 pt-3 text-xs text-slate-500">
                <div className="flex items-center justify-between">
                  <span className="flex items-center space-x-1">
                    <MapPin className="w-3.5 h-3.5 text-slate-400" />
                    <span>{opp.location}</span>
                  </span>
                  <span className="font-bold text-slate-800">{opp.stipend_or_salary}</span>
                </div>

                <div className="bg-emerald-50 p-2.5 rounded-lg border border-emerald-100 flex items-center justify-between">
                  <div className="flex items-center space-x-1.5 text-[11px] text-emerald-900">
                    <Sparkles className="w-3.5 h-3.5 text-amber-500 flex-shrink-0" />
                    <span>Explainable Match: Skill L4 met, Location proximal</span>
                  </div>
                  <Link to={`/opportunities/${opp.id}`} className="btn-primary text-xs py-1 px-3">
                    View Candidates
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

    </div>
  );
};
