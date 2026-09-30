import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { apiFetch } from '../services/api';
import { BrainCircuit, BookOpen, CheckCircle, AlertOctagon, ArrowRight, RefreshCw, Sparkles } from 'lucide-react';

export const SkillGaps: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const memberId = id || 'm4444444-4444-4444-4444-444444444444';
  
  const [gapsData, setGapsData] = useState<any>(null);
  const [recs, setRecs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);

  const loadData = async () => {
    try {
      const [gapsRes, recsRes] = await Promise.all([
        apiFetch(`/members/${memberId}/skill-gaps`),
        apiFetch(`/members/${memberId}/recommendations`)
      ]);
      setGapsData(gapsRes.data || []);
      setRecs(recsRes.data || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [memberId]);

  const runAnalysis = async () => {
    setAnalyzing(true);
    try {
      await apiFetch(`/ai/skill-gap-analysis/${memberId}`, { method: 'POST' });
      await loadData();
    } catch (err) {
      console.error(err);
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <div>
          <div className="flex items-center space-x-2">
            <span className="badge badge-active text-[10px]">AI ENGINE ANALYZER</span>
            <span className="text-xs font-mono text-slate-400">Target Role: Digital Inventory Assistant</span>
          </div>
          <h1 className="text-xl font-bold text-slate-900 mt-1 flex items-center space-x-2">
            <BrainCircuit className="w-5 h-5 text-coop-dark" />
            <span>Meena Jadhav - AI Skill Gap Analysis</span>
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Explainable gap score normalized against required competency levels.
          </p>
        </div>

        <button
          onClick={runAnalysis}
          disabled={analyzing}
          className="btn-primary text-xs flex items-center space-x-2 font-bold shadow-md"
        >
          <RefreshCw className={`w-4 h-4 ${analyzing ? 'animate-spin' : ''}`} />
          <span>{analyzing ? 'Calculating Gaps...' : 'Recalculate AI Gaps'}</span>
        </button>
      </div>

      {/* Readiness Overview Banner */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-gradient-to-br from-coop-dark to-emerald-900 text-white p-5 rounded-xl shadow-md">
          <p className="text-xs font-semibold text-emerald-200 uppercase">Overall Role Readiness</p>
          <p className="text-3xl font-extrabold text-amber-300 mt-1">78.5%</p>
          <p className="text-[11px] text-emerald-200 mt-1">3 of 5 Required Competencies Met</p>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <p className="text-xs font-semibold text-slate-500 uppercase">Highest Priority Skill Gap</p>
          <p className="text-lg font-bold text-rose-700 mt-1">ERP Operation & Daily Entry</p>
          <p className="text-xs text-slate-500 mt-0.5">Required: Level 4 | Current: Level 1</p>
        </div>

        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
          <p className="text-xs font-semibold text-slate-500 uppercase">Recommended Learning Path</p>
          <p className="text-lg font-bold text-coop-dark mt-1">ERP Fundamentals (90 Min)</p>
          <p className="text-xs text-emerald-600 mt-0.5 font-medium">Covers 100% of Critical Gaps</p>
        </div>
      </div>

      {/* Skill Gaps Breakdown Table */}
      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
        <div className="px-5 py-4 border-b border-slate-100 font-bold text-slate-800 text-sm">
          Identified Skill Gaps & Explainable Diagnostic
        </div>
        
        {loading ? (
          <div className="p-8 text-center text-xs text-slate-500">Loading skill gap diagnostic...</div>
        ) : (
          <div className="divide-y divide-slate-100">
            {gapsData.map((gap: any) => (
              <div key={gap.id || gap.skill_id} className="p-5 hover:bg-slate-50 transition-colors flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div className="space-y-1 max-w-xl">
                  <div className="flex items-center space-x-2">
                    <span className={`badge ${gap.priority === 'Critical' ? 'badge-danger' : 'badge-pending'} text-[10px]`}>
                      {gap.priority} PRIORITY
                    </span>
                    <span className="text-xs font-bold text-slate-900">{gap.skill_name || 'ERP Operation'}</span>
                    <span className="text-[10px] text-slate-400 font-mono">({gap.category})</span>
                  </div>
                  <p className="text-xs text-slate-600 leading-relaxed">
                    {gap.explanation || `Required level is ${gap.required_level}, current level is ${gap.current_level}.`}
                  </p>
                </div>

                <div className="flex items-center space-x-4 min-w-[240px] justify-between md:justify-end">
                  <div className="text-right">
                    <p className="text-[11px] text-slate-500 font-medium">Current / Target</p>
                    <p className="text-sm font-bold text-slate-800">L{gap.current_level} / L{gap.required_level}</p>
                  </div>
                  <Link
                    to="/courses/course-c01"
                    className="btn-primary text-xs py-1.5 px-3 flex items-center space-x-1"
                  >
                    <span>Enrol Path</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* AI Course Recommendations section */}
      <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-4">
        <h3 className="text-sm font-bold text-slate-800 flex items-center space-x-2">
          <Sparkles className="w-4 h-4 text-amber-500" />
          <span>Personalised Learning Path Recommendations</span>
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {recs.map((r: any) => (
            <div key={r.course_id} className="p-4 rounded-lg border border-slate-200 bg-slate-50 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between">
                  <span className="badge badge-active text-[10px]">Relevance: {r.relevance_score}%</span>
                  <span className="text-[10px] font-mono text-slate-500">{r.duration_minutes} Mins</span>
                </div>
                <h4 className="text-sm font-bold text-slate-900 mt-2">{r.title}</h4>
                <ul className="text-xs text-slate-600 mt-2 space-y-1">
                  {r.recommendation_reasons?.map((reason: string, idx: number) => (
                    <li key={idx} className="flex items-center space-x-1">
                      <span className="text-emerald-600">✓</span>
                      <span>{reason}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-200 flex justify-end">
                <Link to={`/courses/${r.course_id}`} className="btn-accent text-xs py-1 px-3">
                  Start Course & Lessons
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
};
