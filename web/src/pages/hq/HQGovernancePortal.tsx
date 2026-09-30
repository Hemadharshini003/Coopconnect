import React, { useState, useEffect } from 'react';
import { 
  Building2, ShieldCheck, CheckCircle2, XCircle, AlertCircle, FileText, 
  Users, Award, Calendar, BarChart3, Clock, RefreshCw, Filter, Search,
  Download, ExternalLink, Check, Eye, Lock, Layers, Cpu, Database
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export const HQGovernancePortal: React.FC<{ initialTab?: string }> = ({ initialTab = 'dashboard' }) => {
  const [activeTab, setActiveTab] = useState(initialTab);
  const [loading, setLoading] = useState(true);
  const [dashboardData, setDashboardData] = useState<any>(null);
  const [institutes, setInstitutes] = useState<any[]>([]);
  const [programmeApprovals, setProgrammeApprovals] = useState<any[]>([]);
  const [certificates, setCertificates] = useState<any[]>([]);
  const [auditLogs, setAuditLogs] = useState<any[]>([]);
  const [templates, setTemplates] = useState<any[]>([]);
  const [selectedInst, setSelectedInst] = useState<any>(null);

  // Verification state
  const [verifyCertNo, setVerifyCertNo] = useState('');
  const [verifyResult, setVerifyResult] = useState<any>(null);
  const [verifying, setVerifying] = useState(false);

  // Revoke state
  const [revokeCertId, setRevokeCertId] = useState<string | null>(null);
  const [revokeReason, setRevokeReason] = useState('');

  const { token } = useAuth();

  useEffect(() => {
    fetchHQData();
  }, [token]);

  useEffect(() => {
    if (initialTab) {
      setActiveTab(initialTab);
    }
  }, [initialTab]);

  const fetchHQData = async () => {
    setLoading(true);
    try {
      const headers = { Authorization: `Bearer ${token || ''}` };

      const [dashRes, instRes, progRes, certRes, auditRes, tmplRes] = await Promise.all([
        fetch('/api/v1/hq/dashboard', { headers }).then(r => r.json()),
        fetch('/api/v1/hq/institutes', { headers }).then(r => r.json()),
        fetch('/api/v1/hq/programme-approvals', { headers }).then(r => r.json()),
        fetch('/api/v1/hq/certificates', { headers }).then(r => r.json()),
        fetch('/api/v1/hq/audit-logs', { headers }).then(r => r.json()),
        fetch('/api/v1/hq/templates', { headers }).then(r => r.json()),
      ]);

      if (dashRes.data) setDashboardData(dashRes.data);
      if (instRes.data) setInstitutes(instRes.data);
      if (progRes.data) setProgrammeApprovals(progRes.data);
      if (certRes.data) setCertificates(certRes.data);
      if (auditRes.data) setAuditLogs(auditRes.data);
      if (tmplRes.data) setTemplates(tmplRes.data);
    } catch (err) {
      console.error('Failed to fetch HQ governance data', err);
    } finally {
      setLoading(false);
    }
  };

  const handleApprovalAction = async (programmeId: string, status: string, comments: string) => {
    try {
      const res = await fetch(`/api/v1/hq/programme-approvals/${programmeId}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ status, approval_comments: comments })
      });
      if (res.ok) {
        fetchHQData();
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleVerifyCertificate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!verifyCertNo.trim()) return;
    setVerifying(true);
    setVerifyResult(null);
    try {
      const res = await fetch(`/api/v1/hq/certificates/verify/${encodeURIComponent(verifyCertNo)}`);
      const data = await res.json();
      setVerifyResult(data.data || data);
    } catch (e) {
      setVerifyResult({ is_valid: false, message: 'Verification API network error' });
    } finally {
      setVerifying(false);
    }
  };

  const handleRevokeCertificate = async (certId: string) => {
    if (!revokeReason.trim()) return;
    try {
      const res = await fetch(`/api/v1/hq/certificates/${certId}/revoke`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ reason: revokeReason })
      });
      if (res.ok) {
        setRevokeCertId(null);
        setRevokeReason('');
        fetchHQData();
      }
    } catch (e) {
      console.error(e);
    }
  };

  const metrics = dashboardData?.metrics || {
    total_institutes: 20,
    active_institutes: 20,
    total_programmes: 48,
    programmes_completed: 34,
    trainees_enrolled: 2450,
    trainees_completed: 1890,
    attendance_rate: 92.4,
    assessment_completion: 88.6,
    certificates_issued: 1890,
    placement_outcomes: 1420
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white p-6 shadow-xl border border-indigo-500/30">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 relative z-10">
          <div>
            <div className="flex items-center space-x-3 mb-1">
              <span className="px-3 py-1 rounded-full text-xs font-semibold bg-indigo-500/20 text-indigo-300 border border-indigo-400/30 flex items-center gap-1.5">
                <ShieldCheck className="w-3.5 h-3.5 text-indigo-400" />
                NCCT National Governance Layer
              </span>
              <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-amber-500/20 text-amber-300 border border-amber-400/30">
                Demo Data
              </span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-slate-50">
              National Council for Cooperative Training (NCCT)
            </h1>
            <p className="text-xs sm:text-sm text-slate-300 mt-1 max-w-2xl">
              Consolidated Headquarters Control & Governance over 20 Regional & State Cooperative Management Institutes across India.
            </p>
          </div>
          <button
            onClick={fetchHQData}
            className="flex items-center space-x-2 px-4 py-2 rounded-xl bg-indigo-600/40 hover:bg-indigo-600/60 border border-indigo-400/40 text-xs font-bold transition shadow-md"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            <span>Refresh HQ Data</span>
          </button>
        </div>
      </div>

      {/* TAB 1: NATIONAL DASHBOARD */}
      {activeTab === 'dashboard' && (
        <div className="space-y-6">
          {/* Key Metric Grid */}
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            <div className="bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
              <div className="flex items-center justify-between text-indigo-600 mb-2">
                <span className="text-xs font-semibold text-slate-500">NCCT Institutes</span>
                <Building2 className="w-5 h-5" />
              </div>
              <div className="text-2xl font-extrabold text-slate-900 dark:text-white">
                {metrics.active_institutes} / {metrics.total_institutes}
              </div>
              <span className="text-[10px] text-emerald-600 font-medium">100% Operational Health</span>
            </div>

            <div className="bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
              <div className="flex items-center justify-between text-blue-600 mb-2">
                <span className="text-xs font-semibold text-slate-500">Total Programmes</span>
                <FileText className="w-5 h-5" />
              </div>
              <div className="text-2xl font-extrabold text-slate-900 dark:text-white">
                {metrics.total_programmes}
              </div>
              <span className="text-[10px] text-blue-600 font-medium">{metrics.programmes_completed} Completed</span>
            </div>

            <div className="bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
              <div className="flex items-center justify-between text-amber-600 mb-2">
                <span className="text-xs font-semibold text-slate-500">Trainees Enrolled</span>
                <Users className="w-5 h-5" />
              </div>
              <div className="text-2xl font-extrabold text-slate-900 dark:text-white">
                {metrics.trainees_enrolled}
              </div>
              <span className="text-[10px] text-amber-600 font-medium">{metrics.trainees_completed} Certified</span>
            </div>

            <div className="bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
              <div className="flex items-center justify-between text-emerald-600 mb-2">
                <span className="text-xs font-semibold text-slate-500">Attendance Rate</span>
                <CheckCircle2 className="w-5 h-5" />
              </div>
              <div className="text-2xl font-extrabold text-slate-900 dark:text-white">
                {metrics.attendance_rate}%
              </div>
              <span className="text-[10px] text-emerald-600 font-medium">Biometric & Kiosk Verified</span>
            </div>

            <div className="bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
              <div className="flex items-center justify-between text-purple-600 mb-2">
                <span className="text-xs font-semibold text-slate-500">Placements</span>
                <Award className="w-5 h-5" />
              </div>
              <div className="text-2xl font-extrabold text-slate-900 dark:text-white">
                {metrics.placement_outcomes}
              </div>
              <span className="text-[10px] text-purple-600 font-medium">75.1% Career Outcome Rate</span>
            </div>
          </div>

          {/* 20 Institutes Comparison Table */}
          <div className="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
            <h3 className="text-base font-bold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
              <Building2 className="w-5 h-5 text-indigo-600" />
              National 20 NCCT Institutes Overview & Sync Health
            </h3>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-slate-200 dark:border-slate-800 text-slate-500 font-semibold uppercase">
                    <th className="py-2.5 px-3">Code</th>
                    <th className="py-2.5 px-3">Institute Name</th>
                    <th className="py-2.5 px-3">State / Region</th>
                    <th className="py-2.5 px-3">Sync Status</th>
                    <th className="py-2.5 px-3 text-right">Programmes</th>
                    <th className="py-2.5 px-3 text-right">Trainees</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-slate-800/60 font-medium">
                  {institutes.slice(0, 10).map((inst) => (
                    <tr key={inst.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/40">
                      <td className="py-3 px-3 font-mono font-bold text-indigo-600">{inst.code}</td>
                      <td className="py-3 px-3 font-bold text-slate-900 dark:text-white">{inst.name}</td>
                      <td className="py-3 px-3 text-slate-500">{inst.state} ({inst.region})</td>
                      <td className="py-3 px-3">
                        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-semibold bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800">
                          <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                          HEALTHY
                        </span>
                      </td>
                      <td className="py-3 px-3 text-right font-bold text-slate-700 dark:text-slate-300">2 - 4</td>
                      <td className="py-3 px-3 text-right font-bold text-slate-700 dark:text-slate-300">120+</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: INSTITUTES DIRECTORY */}
      {activeTab === 'institutes' && (
        <div className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {institutes.map((inst) => (
              <div key={inst.id} className="bg-white dark:bg-slate-900 p-5 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm hover:border-indigo-500/40 transition">
                <div className="flex items-start justify-between">
                  <span className="px-2.5 py-1 rounded-lg text-xs font-mono font-bold bg-indigo-50 dark:bg-indigo-950/50 text-indigo-600 dark:text-indigo-400 border border-indigo-200 dark:border-indigo-800">
                    {inst.code}
                  </span>
                  <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300">
                    Active
                  </span>
                </div>
                <h4 className="font-bold text-sm text-slate-900 dark:text-white mt-3">{inst.name}</h4>
                <p className="text-xs text-slate-500 mt-1">{inst.city}, {inst.state} â€¢ {inst.region} Region</p>
                <div className="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 text-[11px] text-slate-500 space-y-1">
                  <div>Email: <span className="font-semibold text-slate-700 dark:text-slate-300">{inst.contact_email}</span></div>
                  <div>Phone: <span className="font-semibold text-slate-700 dark:text-slate-300">{inst.contact_phone}</span></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB 3: PROGRAMME APPROVALS */}
      {activeTab === 'programme-approvals' && (
        <div className="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
          <h3 className="text-base font-bold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
            <FileText className="w-5 h-5 text-indigo-600" />
            National Programme Proposals & Approval Workflow
          </h3>
          <div className="space-y-4">
            {programmeApprovals.map((p) => (
              <div key={p.id} className="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-800/30 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
                <div>
                  <div className="flex items-center space-x-2">
                    <span className="font-mono text-xs font-bold text-indigo-600">{p.code}</span>
                    <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
                      p.status === 'APPROVED' ? 'bg-emerald-100 text-emerald-800' :
                      p.status === 'REJECTED' ? 'bg-rose-100 text-rose-800' : 'bg-amber-100 text-amber-800'
                    }`}>
                      {p.status}
                    </span>
                  </div>
                  <h4 className="font-bold text-sm text-slate-900 dark:text-white mt-1">{p.title}</h4>
                  <p className="text-xs text-slate-500">Institute: {p.institute_name} | Target Capacity: {p.target_capacity} Trainees</p>
                </div>
                {p.status === 'PENDING_APPROVAL' && (
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => handleApprovalAction(p.id, 'APPROVED', 'Approved by NCCT HQ Academic Board.')}
                      className="px-3 py-1.5 rounded-lg bg-emerald-600 text-white text-xs font-bold hover:bg-emerald-700 transition"
                    >
                      Approve Programme
                    </button>
                    <button
                      onClick={() => handleApprovalAction(p.id, 'REJECTED', 'Requires syllabus restructuring.')}
                      className="px-3 py-1.5 rounded-lg bg-rose-600 text-white text-xs font-bold hover:bg-rose-700 transition"
                    >
                      Reject
                    </button>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB 4: NATIONAL SCHEDULE */}
      {activeTab === 'national-calendar' && (
        <div className="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
          <h3 className="text-base font-bold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
            <Calendar className="w-5 h-5 text-indigo-600" />
            NCCT National Training Calendar Across 20 Institutes
          </h3>
          <p className="text-xs text-slate-500 mb-4">
            Centralized calendar tracking upcoming, ongoing, and completed training batches across all Regional Institutes of Cooperative Management.
          </p>
          <div className="p-4 bg-indigo-50 dark:bg-indigo-950/30 rounded-xl border border-indigo-200 dark:border-indigo-800 text-xs text-indigo-900 dark:text-indigo-300">
            <strong>National Batch Sync:</strong> 20 NCCT Institutes have published 48 batches scheduled for Q3/Q4. All batches automatically enforce biometric kiosk attendance logging.
          </div>
        </div>
      )}

      {/* TAB 5: CERTIFICATE REGISTRY */}
      {activeTab === 'certificates' && (
        <div className="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <Award className="w-5 h-5 text-indigo-600" />
            NCCT Central Certificate Registry
          </h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-200 dark:border-slate-800 text-slate-500 font-semibold uppercase">
                  <th className="py-2.5 px-3">Cert Number</th>
                  <th className="py-2.5 px-3">Trainee Name</th>
                  <th className="py-2.5 px-3">Institute</th>
                  <th className="py-2.5 px-3">Status</th>
                  <th className="py-2.5 px-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800/60 font-medium">
                {certificates.map((c) => (
                  <tr key={c.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/40">
                    <td className="py-3 px-3 font-mono font-bold text-indigo-600">{c.certificate_number}</td>
                    <td className="py-3 px-3 text-slate-900 dark:text-white font-bold">{c.trainee_name}</td>
                    <td className="py-3 px-3 text-slate-500">{c.institute_name}</td>
                    <td className="py-3 px-3">
                      <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold ${
                        c.status === 'VALID' ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'
                      }`}>
                        {c.status}
                      </span>
                    </td>
                    <td className="py-3 px-3 text-right">
                      {c.status === 'VALID' && (
                        <button
                          onClick={() => {
                            setRevokeCertId(c.id);
                            setRevokeReason('Administrative Audit Discrepancy');
                          }}
                          className="px-2.5 py-1 bg-rose-50 text-rose-600 hover:bg-rose-100 border border-rose-200 rounded text-[10px] font-bold"
                        >
                          Revoke Cert
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Revoke modal */}
          {revokeCertId && (
            <div className="p-4 bg-rose-50 dark:bg-rose-950/40 rounded-xl border border-rose-200 dark:border-rose-800 text-xs space-y-3">
              <h4 className="font-bold text-rose-900 dark:text-rose-200">Revoke Certificate Authority Authorization</h4>
              <input
                type="text"
                value={revokeReason}
                onChange={(e) => setRevokeReason(e.target.value)}
                placeholder="Reason for revocation..."
                className="w-full px-3 py-2 border border-slate-300 dark:border-slate-700 rounded-lg text-xs"
              />
              <div className="flex space-x-2">
                <button
                  onClick={() => handleRevokeCertificate(revokeCertId)}
                  className="px-3 py-1.5 bg-rose-600 text-white rounded font-bold"
                >
                  Confirm Revocation
                </button>
                <button
                  onClick={() => setRevokeCertId(null)}
                  className="px-3 py-1.5 bg-slate-200 text-slate-700 rounded font-bold"
                >
                  Cancel
                </button>
              </div>
            </div>
          )}
        </div>
      )}

      {/* TAB 6: QR CERTIFICATE VERIFICATION */}
      {activeTab === 'certificate-verification' && (
        <div className="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm max-w-xl mx-auto space-y-6">
          <div className="text-center space-y-2">
            <ShieldCheck className="w-10 h-10 text-indigo-600 mx-auto" />
            <h3 className="text-xl font-bold text-slate-900 dark:text-white">
              NCCT Central QR Certificate Verification Portal
            </h3>
            <p className="text-xs text-slate-500">
              Verify official training certificates issued across all 20 NCCT Regional Institutes.
            </p>
          </div>

          <form onSubmit={handleVerifyCertificate} className="flex gap-2">
            <input
              type="text"
              value={verifyCertNo}
              onChange={(e) => setVerifyCertNo(e.target.value)}
              placeholder="e.g. CERT--2026-RAMESH-ERP"
              className="flex-1 px-4 py-2.5 border border-slate-300 dark:border-slate-700 rounded-xl text-sm focus:ring-2 focus:ring-indigo-600 focus:outline-none"
            />
            <button
              type="submit"
              disabled={verifying}
              className="px-5 py-2.5 bg-indigo-600 text-white rounded-xl text-xs font-bold shadow-md hover:bg-indigo-700 transition"
            >
              {verifying ? 'Verifying...' : 'Verify Now'}
            </button>
          </form>

          {verifyResult && (
            <div className={`p-4 rounded-xl border text-xs space-y-2 ${
              verifyResult.is_valid 
                ? 'bg-emerald-50 dark:bg-emerald-950/40 border-emerald-300 dark:border-emerald-800 text-emerald-900 dark:text-emerald-200'
                : 'bg-rose-50 dark:bg-rose-950/40 border-rose-300 dark:border-rose-800 text-rose-900 dark:text-rose-200'
            }`}>
              <div className="flex items-center space-x-2 font-bold text-sm">
                {verifyResult.is_valid ? <CheckCircle2 className="w-5 h-5 text-emerald-600" /> : <XCircle className="w-5 h-5 text-rose-600" />}
                <span>{verifyResult.status || 'Verification Result'}</span>
              </div>
              <div>Certificate Number: <strong>{verifyResult.certificate_number}</strong></div>
              <div>Trainee Name: <strong>{verifyResult.trainee_name}</strong></div>
              <div>Issuing Authority: <strong>{verifyResult.institute_name}</strong></div>
            </div>
          )}
        </div>
      )}

      {/* TAB 7: TEMPLATES */}
      {activeTab === 'templates' && (
        <div className="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <Layers className="w-5 h-5 text-indigo-600" />
            NCCT National Governance Templates
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {templates.map((t) => (
              <div key={t.id} className="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-800/30">
                <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-indigo-100 text-indigo-800">
                  {t.template_type}
                </span>
                <h4 className="font-bold text-sm text-slate-900 dark:text-white mt-2">{t.title}</h4>
                <p className="text-xs text-slate-500 mt-1">{t.description}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB 8: AUDIT LOGS */}
      {activeTab === 'audit-logs' && (
        <div className="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 shadow-sm space-y-4">
          <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <Lock className="w-5 h-5 text-indigo-600" />
            National Security & Operational Audit Log Trail
          </h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-mono">
              <thead>
                <tr className="border-b border-slate-200 dark:border-slate-800 text-slate-500 font-semibold uppercase">
                  <th className="py-2.5 px-3">Timestamp</th>
                  <th className="py-2.5 px-3">User ID</th>
                  <th className="py-2.5 px-3">Action</th>
                  <th className="py-2.5 px-3">Resource</th>
                  <th className="py-2.5 px-3">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800/60">
                {auditLogs.map((log) => (
                  <tr key={log.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/40">
                    <td className="py-2.5 px-3 text-slate-500">{log.timestamp}</td>
                    <td className="py-2.5 px-3 font-bold text-indigo-600">{log.user_id || 'System'}</td>
                    <td className="py-2.5 px-3 text-slate-900 dark:text-white">{log.action}</td>
                    <td className="py-2.5 px-3 text-slate-500">{log.resource}</td>
                    <td className="py-2.5 px-3">
                      <span className="px-2 py-0.5 bg-emerald-100 text-emerald-800 rounded text-[10px] font-bold">
                        {log.status}
                      </span>
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

export default HQGovernancePortal;

