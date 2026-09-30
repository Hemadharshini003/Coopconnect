import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { apiFetch } from '../services/api';
import { Briefcase, MapPin, Sparkles, CheckCircle2, UserCheck, Award } from 'lucide-react';

export const OpportunityDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const oppId = id || 'opp-o01';

  const [opp, setOpp] = useState<any>(null);
  const [candidates, setCandidates] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [applied, setApplied] = useState(false);
  const [placementRecorded, setPlacementRecorded] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [oppRes, candRes] = await Promise.all([
          apiFetch(`/opportunities/${oppId}`),
          apiFetch(`/opportunities/${oppId}/matches`)
        ]);
        setOpp(oppRes.data);
        setCandidates(candRes.data || []);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [oppId]);

  const handleApply = async (memberId: string) => {
    try {
      await apiFetch(`/opportunities/${oppId}/apply`, {
        method: 'POST',
        body: JSON.stringify({ member_id: memberId, match_score: 92.5 })
      });
      setApplied(true);
    } catch (err) {
      console.error(err);
    }
  };

  const handleRecordPlacement = async (memberId: string) => {
    try {
      await apiFetch('/placements', {
        method: 'POST',
        body: JSON.stringify({
          application_id: 'app-001',
          member_id: memberId,
          opportunity_id: oppId,
          income_before: 8000,
          income_after: 18500
        })
      });
      setPlacementRecorded(true);
    } catch (err) {
      console.error(err);
    }
  };

  if (loading || !opp) {
    return <div className="p-8 text-center text-xs text-slate-500">Loading opportunity & AI candidate matches...</div>;
  }

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-3">
        <div className="flex items-center justify-between">
          <span className="badge badge-active text-[10px]">{opp.opportunity_type}</span>
          <span className="text-sm font-bold text-coop-dark font-mono">{opp.stipend_or_salary}</span>
        </div>
        <h1 className="text-2xl font-bold text-slate-900">{opp.title}</h1>
        <p className="text-xs text-slate-600 max-w-2xl leading-relaxed">{opp.description}</p>
        <p className="text-xs text-slate-500 flex items-center space-x-1">
          <MapPin className="w-3.5 h-3.5 text-slate-400" />
          <span>{opp.location} • {opp.number_of_positions} Open Position(s)</span>
        </p>

        {applied && (
          <div className="bg-emerald-50 border border-emerald-200 text-emerald-800 p-3 rounded-lg text-xs font-semibold flex items-center space-x-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0" />
            <span>Application submitted successfully! Recruiter notified.</span>
          </div>
        )}

        {placementRecorded && (
          <div className="bg-amber-50 border border-amber-200 text-amber-900 p-3 rounded-lg text-xs font-semibold flex items-center space-x-2">
            <Award className="w-4 h-4 text-amber-600 flex-shrink-0" />
            <span>Placement outcome recorded! Member income increased from ₹8,000 to ₹18,500/mo.</span>
          </div>
        )}
      </div>

      {/* Candidates List with Explainable AI Match Scores */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden space-y-1">
        <div className="px-5 py-4 border-b border-slate-100 font-bold text-slate-800 text-sm flex items-center justify-between">
          <span className="flex items-center space-x-2">
            <Sparkles className="w-4 h-4 text-amber-500" />
            <span>AI Matched Candidates Ranking</span>
          </span>
          <span className="text-xs text-slate-500 font-normal">Strictly Fair (No demographic biases)</span>
        </div>

        <div className="divide-y divide-slate-100">
          {candidates.map((cand) => (
            <div key={cand.member_id} className="p-5 hover:bg-slate-50 flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div className="space-y-1.5">
                <div className="flex items-center space-x-3">
                  <h4 className="text-sm font-bold text-slate-900">{cand.full_name}</h4>
                  <span className="badge badge-active text-[10px]">Match: {cand.match_score}%</span>
                </div>
                <p className="text-xs text-slate-600 leading-relaxed max-w-xl">{cand.match_explanation}</p>
                <div className="flex flex-wrap gap-1 pt-1">
                  {cand.matching_strengths?.map((str: string, idx: number) => (
                    <span key={idx} className="bg-emerald-50 text-emerald-800 border border-emerald-200 text-[10px] px-2 py-0.5 rounded">
                      ✓ {str}
                    </span>
                  ))}
                </div>
              </div>

              <div className="flex items-center space-x-2">
                <button
                  onClick={() => handleApply(cand.member_id)}
                  className="btn-primary text-xs py-1.5 px-3 flex items-center space-x-1"
                >
                  <UserCheck className="w-3.5 h-3.5" />
                  <span>Apply Candidate</span>
                </button>
                <button
                  onClick={() => handleRecordPlacement(cand.member_id)}
                  className="btn-accent text-xs py-1.5 px-3 flex items-center space-x-1"
                >
                  <Award className="w-3.5 h-3.5" />
                  <span>Record Placement</span>
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
};
