import React, { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { apiFetch } from '../services/api';
import { getRoleTheme } from '../utils/theme';
import { Link } from 'react-router-dom';
import { HQGovernancePortal } from './hq/HQGovernancePortal';
import { 
  Users, 
  Building2, 
  BrainCircuit, 
  BookOpen, 
  Briefcase, 
  Award, 
  ArrowRight, 
  CheckCircle2, 
  Sparkles,
  UserCheck,
  ShieldCheck,
  Target,
  BarChart3,
  FileCheck,
  Plus,
  Calendar,
  Clock,
  AlertTriangle,
  FileText,
  HelpCircle,
  GraduationCap
} from 'lucide-react';

export const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const theme = getRoleTheme(user?.role);
  const isHQUser = user?.role?.startsWith('NCCT_') || user?.role === 'SUPER_ADMIN';

  useEffect(() => {
    const fetchDashboard = async () => {
      setLoading(true);
      try {
        let endpoint = '/dashboard/cooperative';
        if (user?.role === 'MEMBER' || user?.role === 'TRAINEE' || user?.role === 'EMPLOYEE') {
          endpoint = '/dashboard/member';
        } else if (user?.role === 'DISTRICT_ADMIN') {
          endpoint = '/dashboard/district';
        } else if (user?.role === 'SUPER_ADMIN' || isHQUser) {
          endpoint = '/hq/dashboard';
        }

        const res = await apiFetch(endpoint);
        setData(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    if (!isHQUser) {
      fetchDashboard();
    } else {
      setLoading(false);
    }
  }, [user, isHQUser]);

  // 1. NCCT Headquarters Roles Direct Render
  if (isHQUser) {
    return <HQGovernancePortal initialTab="dashboard" />;
  }

  if (loading) {
    return (
      <div className="p-8 flex items-center justify-center space-x-3 text-slate-500">
        <BrainCircuit className="w-6 h-6 animate-spin text-coop-dark" />
        <span>Loading {theme.name} Dashboard...</span>
      </div>
    );
  }

  // 2. Institute Administrator View
  if (user?.role === 'INSTITUTE_ADMIN' || user?.role === 'COOPERATIVE_ADMIN' || user?.role === 'INSTITUTE_PROGRAMME_COORDINATOR') {
    return (
      <div className="space-y-6">
        {/* Banner */}
        <div className={`bg-gradient-to-r ${theme.bannerBg} rounded-2xl p-6 text-white shadow-lg flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border border-white/10`}>
          <div>
            <span className="bg-white/20 text-amber-300 text-[10px] font-extrabold px-3 py-1 rounded-full border border-white/20 uppercase tracking-wider">
              {theme.badge}
            </span>
            <h1 className="text-2xl font-extrabold mt-2 tracking-tight">NCCT Campus Operations • {user?.full_name}</h1>
            <p className="text-xs text-slate-200 mt-1 max-w-xl leading-relaxed">
              Managing batches, timetable schedules, trainer assignments, and trainee outcomes for this institute.
            </p>
          </div>
          <div className="flex flex-wrap gap-2">
            <Link to="/members" className="btn-primary text-xs flex items-center space-x-1.5 font-bold shadow-lg">
              <Users className="w-4 h-4" />
              <span>Trainee Roster</span>
            </Link>
            <Link to="/opportunities" className="btn-accent text-xs flex items-center space-x-1.5 font-bold shadow-lg">
              <Plus className="w-4 h-4" />
              <span>Post Opportunity</span>
            </Link>
          </div>
        </div>

        {/* Operational KPI Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-white p-5 rounded-2xl border border-emerald-500 shadow-sm flex items-center space-x-4">
            <div className="w-12 h-12 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center font-bold">
              <Users className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Enrolled Trainees</p>
              <p className="text-2xl font-extrabold text-slate-900 mt-0.5">{data?.total_members || 148}</p>
            </div>
          </div>

          <div className="bg-white p-5 rounded-2xl border border-emerald-500 shadow-sm flex items-center space-x-4">
            <div className="w-12 h-12 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center font-bold">
              <Calendar className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Active Batches</p>
              <p className="text-2xl font-extrabold text-slate-900 mt-0.5">6 Batches</p>
            </div>
          </div>

          <div className="bg-white p-5 rounded-2xl border border-emerald-500 shadow-sm flex items-center space-x-4">
            <div className="w-12 h-12 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center font-bold">
              <CheckCircle2 className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Avg Attendance</p>
              <p className="text-2xl font-extrabold text-emerald-600 mt-0.5">89.4%</p>
            </div>
          </div>

          <div className="bg-white p-5 rounded-2xl border border-emerald-500 shadow-sm flex items-center space-x-4">
            <div className="w-12 h-12 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center font-bold">
              <Award className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Certificates Issued</p>
              <p className="text-2xl font-extrabold text-slate-900 mt-0.5">124</p>
            </div>
          </div>
        </div>

        {/* Operational Modules & Activity */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm lg:col-span-2 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="text-sm font-bold text-slate-800 flex items-center space-x-2">
                <Calendar className="w-4 h-4 text-emerald-600" />
                <span>Today's Campus Timetable & Sessions</span>
              </h3>
              <span className="text-xs font-bold text-emerald-700">Live Campus Schedule</span>
            </div>
            <div className="space-y-3">
              <div className="p-3.5 bg-slate-50 border border-slate-200 rounded-xl flex items-center justify-between">
                <div>
                  <span className="text-[10px] font-extrabold px-2 py-0.5 bg-emerald-100 text-emerald-800 rounded">ROOM 101 • CLASSROOM</span>
                  <h4 className="text-xs font-bold text-slate-900 mt-1">Cooperative Accounting & Audit Standards (Batch 2026-A)</h4>
                  <p className="text-[11px] text-slate-500 mt-0.5">Trainer: Dr. S. Rao • 10:00 AM - 11:30 AM</p>
                </div>
                <span className="text-xs font-bold text-emerald-600 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200">In Progress</span>
              </div>
              <div className="p-3.5 bg-slate-50 border border-slate-200 rounded-xl flex items-center justify-between">
                <div>
                  <span className="text-[10px] font-extrabold px-2 py-0.5 bg-blue-100 text-blue-800 rounded">COMPUTER LAB 2 • DIGITAL</span>
                  <h4 className="text-xs font-bold text-slate-900 mt-1">PACS ERP Digital Inventory & Billing Hands-on</h4>
                  <p className="text-[11px] text-slate-500 mt-0.5">Trainer: Prof. K. Sharma • 02:00 PM - 03:30 PM</p>
                </div>
                <span className="text-xs font-bold text-slate-600 bg-slate-100 px-2.5 py-1 rounded-full">Scheduled</span>
              </div>
            </div>
          </div>

          <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-4">
            <h3 className="text-sm font-bold text-slate-800 flex items-center space-x-2">
              <AlertTriangle className="w-4 h-4 text-amber-500" />
              <span>Training Risk & Support Alerts</span>
            </h3>
            <div className="space-y-3">
              <div className="p-3 bg-amber-50 border border-amber-200 rounded-xl">
                <p className="text-xs font-bold text-amber-900">3 Trainees Need Support</p>
                <p className="text-[11px] text-amber-800 mt-1">Low quiz performance detected in ERP Reporting module.</p>
                <Link to="/members" className="text-[11px] font-bold text-amber-900 underline mt-2 block">
                  Assign Remedial Learning →
                </Link>
              </div>
              <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-xl">
                <p className="text-xs font-bold text-emerald-900">Data Sync Health</p>
                <p className="text-[11px] text-emerald-800 mt-1">Campus biometric and kiosk records synced 100% with NCCT HQ.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // 3. Trainer View
  if (user?.role === 'TRAINER') {
    return (
      <div className="space-y-6">
        <div className={`bg-gradient-to-r ${theme.bannerBg} rounded-2xl p-6 text-white shadow-lg flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border border-white/10`}>
          <div>
            <span className="bg-white/20 text-purple-300 text-[10px] font-extrabold px-3 py-1 rounded-full border border-white/20 uppercase tracking-wider">
              {theme.badge}
            </span>
            <h1 className="text-2xl font-extrabold mt-2 tracking-tight">Faculty Dashboard • {user?.full_name}</h1>
            <p className="text-xs text-slate-200 mt-1 max-w-xl leading-relaxed">
              Review assigned batches, conduct sessions, verify attendance, and support at-risk trainees with remedial content.
            </p>
          </div>
          <div className="flex flex-wrap gap-2">
            <Link to="/courses/course-c01" className="btn-primary text-xs flex items-center space-x-1.5 font-bold shadow-lg">
              <FileCheck className="w-4 h-4" />
              <span>AI Quiz Approvals</span>
            </Link>
            <Link to="/courses" className="btn-accent text-xs flex items-center space-x-1.5 font-bold shadow-lg">
              <BookOpen className="w-4 h-4" />
              <span>Course Modules</span>
            </Link>
          </div>
        </div>

        {/* Trainer KPIs */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-white p-5 rounded-2xl border border-purple-500 shadow-sm flex items-center space-x-4">
            <div className="w-12 h-12 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center font-bold">
              <BookOpen className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Assigned Batches</p>
              <p className="text-2xl font-extrabold text-slate-900 mt-0.5">3 Batches</p>
            </div>
          </div>

          <div className="bg-white p-5 rounded-2xl border border-purple-500 shadow-sm flex items-center space-x-4">
            <div className="w-12 h-12 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center font-bold">
              <Users className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Trainees in Roster</p>
              <p className="text-2xl font-extrabold text-slate-900 mt-0.5">76</p>
            </div>
          </div>

          <div className="bg-white p-5 rounded-2xl border border-purple-500 shadow-sm flex items-center space-x-4">
            <div className="w-12 h-12 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center font-bold">
              <Clock className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Today's Classes</p>
              <p className="text-2xl font-extrabold text-purple-600 mt-0.5">2 Sessions</p>
            </div>
          </div>

          <div className="bg-white p-5 rounded-2xl border border-purple-500 shadow-sm flex items-center space-x-4">
            <div className="w-12 h-12 rounded-xl bg-purple-50 text-purple-600 flex items-center justify-center font-bold">
              <FileCheck className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">AI Quiz Reviews</p>
              <p className="text-2xl font-extrabold text-slate-900 mt-0.5">2 Pending</p>
            </div>
          </div>
        </div>

        {/* Trainer Action Roster */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-4">
            <h3 className="text-sm font-bold text-slate-800 flex items-center space-x-2">
              <Calendar className="w-4 h-4 text-purple-600" />
              <span>Today's Teaching Schedule</span>
            </h3>
            <div className="p-3.5 bg-purple-50/50 border border-purple-100 rounded-xl space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-[10px] font-bold px-2 py-0.5 bg-purple-200 text-purple-900 rounded">10:00 AM - 11:30 AM</span>
                <span className="text-xs font-bold text-emerald-700">Classroom 101</span>
              </div>
              <p className="text-xs font-bold text-slate-900">Cooperative Accounting & Audit Standards</p>
              <div className="flex space-x-2 pt-2">
                <Link to="/courses" className="btn-primary text-[11px] py-1 px-2.5">Mark Attendance</Link>
                <Link to="/learning" className="bg-white border border-purple-200 text-purple-900 font-bold text-[11px] py-1 px-2.5 rounded-lg">Open Lesson Deck</Link>
              </div>
            </div>
          </div>

          <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-4">
            <h3 className="text-sm font-bold text-slate-800 flex items-center space-x-2">
              <BrainCircuit className="w-4 h-4 text-purple-600" />
              <span>Learners Needing Early Support</span>
            </h3>
            <div className="p-3 bg-amber-50 border border-amber-200 rounded-xl space-y-1">
              <div className="flex justify-between items-center">
                <span className="text-xs font-bold text-slate-900">Meena Patil (Batch 2026-A)</span>
                <span className="text-[10px] font-extrabold bg-amber-200 text-amber-900 px-2 py-0.5 rounded">Support Recommended</span>
              </div>
              <p className="text-[11px] text-amber-900">Weak score in ERP Reporting Basics. Consecutive absence: 1 day.</p>
              <button className="text-[11px] font-bold text-purple-700 hover:underline pt-1">
                + Assign 1-on-1 Mentoring / Remedial Quiz
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // 4. Recruiter / Placement Officer View
  if (user?.role === 'RECRUITER' || user?.role === 'EMPLOYER_OR_COOPERATIVE_RECRUITER' || user?.role === 'PLACEMENT_OFFICER') {
    return (
      <div className="space-y-6">
        <div className={`bg-gradient-to-r ${theme.bannerBg} rounded-2xl p-6 text-white shadow-lg flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border border-white/10`}>
          <div>
            <span className="bg-white/20 text-cyan-300 text-[10px] font-extrabold px-3 py-1 rounded-full border border-white/20 uppercase tracking-wider">
              {theme.badge}
            </span>
            <h1 className="text-2xl font-extrabold mt-2 tracking-tight">Cooperative Talent & Employer Portal</h1>
            <p className="text-xs text-slate-200 mt-1 max-w-xl leading-relaxed">
              Post cooperative roles, review AI-matched consented candidates with explainable scores, and log outcome follow-ups.
            </p>
          </div>
          <div className="flex flex-wrap gap-2">
            <Link to="/opportunities" className="btn-primary text-xs flex items-center space-x-1.5 font-bold shadow-lg">
              <Plus className="w-4 h-4" />
              <span>Create Opening</span>
            </Link>
            <Link to="/placements" className="btn-accent text-xs flex items-center space-x-1.5 font-bold shadow-lg">
              <Award className="w-4 h-4" />
              <span>Record Placement</span>
            </Link>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-white p-5 rounded-2xl border border-cyan-500 shadow-sm flex items-center space-x-4">
            <div className="w-12 h-12 rounded-xl bg-cyan-50 text-cyan-600 flex items-center justify-center font-bold">
              <Briefcase className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Active Openings</p>
              <p className="text-2xl font-extrabold text-slate-900 mt-0.5">3 Postings</p>
            </div>
          </div>

          <div className="bg-white p-5 rounded-2xl border border-cyan-500 shadow-sm flex items-center space-x-4">
            <div className="w-12 h-12 rounded-xl bg-cyan-50 text-cyan-600 flex items-center justify-center font-bold">
              <BrainCircuit className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">AI Recommended</p>
              <p className="text-2xl font-extrabold text-cyan-600 mt-0.5">14 Candidates</p>
            </div>
          </div>

          <div className="bg-white p-5 rounded-2xl border border-cyan-500 shadow-sm flex items-center space-x-4">
            <div className="w-12 h-12 rounded-xl bg-cyan-50 text-cyan-600 flex items-center justify-center font-bold">
              <UserCheck className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Applications</p>
              <p className="text-2xl font-extrabold text-slate-900 mt-0.5">8 Received</p>
            </div>
          </div>

          <div className="bg-white p-5 rounded-2xl border border-cyan-500 shadow-sm flex items-center space-x-4">
            <div className="w-12 h-12 rounded-xl bg-cyan-50 text-cyan-600 flex items-center justify-center font-bold">
              <Award className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Placements Made</p>
              <p className="text-2xl font-extrabold text-slate-900 mt-0.5">22</p>
            </div>
          </div>
        </div>

        {/* Opportunity Match Spotlight */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <h3 className="text-sm font-bold text-slate-800 flex items-center space-x-2">
              <Sparkles className="w-4 h-4 text-cyan-600" />
              <span>Consented Candidate Match Recommendations (Explainable AI)</span>
            </h3>
            <Link to="/opportunities/opp-o01" className="text-xs font-bold text-cyan-700 hover:underline">
              View All Candidate Rankings →
            </Link>
          </div>
          <div className="p-4 bg-cyan-50/50 border border-cyan-100 rounded-xl flex items-center justify-between">
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-bold text-slate-900 text-sm">Meena Patil</span>
                <span className="bg-emerald-100 text-emerald-800 text-[10px] font-extrabold px-2 py-0.5 rounded-full">86% MATCH</span>
              </div>
              <p className="text-xs text-slate-600 mt-1">Role: Digital Inventory & PACS Billing Assistant</p>
              <p className="text-[11px] text-slate-500 mt-0.5">Strengths: ERP Fundamentals (Certified) • Available in Nashik District</p>
            </div>
            <div className="flex space-x-2">
              <Link to="/applications" className="btn-primary text-xs py-1.5 px-3">Schedule Interview</Link>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // 5. Default: Trainee / Cooperative Member Personal Learning & Career Hub
  return (
    <div className="space-y-6">
      
      {/* Welcome Banner */}
      <div className={`bg-gradient-to-r ${theme.bannerBg} rounded-2xl p-6 text-white shadow-lg flex flex-col md:flex-row items-start md:items-center justify-between gap-4 transition-all duration-300 border border-white/10`}>
        <div>
          <span className="bg-white/20 text-amber-300 text-[10px] font-extrabold px-3 py-1 rounded-full border border-white/20 uppercase tracking-wider">
            {theme.badge}
          </span>
          <h1 className="text-2xl font-extrabold mt-2 tracking-tight">Welcome back, {user?.full_name}</h1>
          <p className="text-xs text-slate-200 mt-1 max-w-xl leading-relaxed">
            {theme.description}
          </p>
        </div>

        <div className="flex flex-wrap gap-2">
          <Link to="/assessments" className="btn-accent text-xs flex items-center space-x-1.5 font-bold shadow-lg">
            <Sparkles className="w-4 h-4" />
            <span>Take Skill Assessment</span>
          </Link>
          <Link to="/courses" className="btn-primary text-xs flex items-center space-x-1.5 font-bold shadow-lg">
            <BookOpen className="w-4 h-4" />
            <span>My Courses</span>
          </Link>
        </div>
      </div>

      {/* Guided 5-Step Trainee Pipeline */}
      <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-4">
        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
          <div className="flex items-center space-x-2">
            <Target className="w-5 h-5 text-coop-dark" />
            <h2 className="text-sm font-bold text-slate-900">CoopConnect AI Guided Learning Flow</h2>
          </div>
          <span className="text-xs text-slate-500">5-Step Capacity Building Pipeline</span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
          <Link to="/assessments" className="p-3 rounded-xl border border-amber-200 bg-amber-50/50 hover:bg-amber-100/50 transition-all flex flex-col justify-between space-y-2">
            <div>
              <span className="text-[10px] font-extrabold text-amber-800 bg-amber-200 px-2 py-0.5 rounded-full">STEP 1</span>
              <h3 className="text-xs font-bold text-amber-950 mt-1.5">Skill Assessment</h3>
              <p className="text-[11px] text-amber-800 leading-tight">Digital & smartphone questionnaire.</p>
            </div>
            <span className="text-[11px] font-bold text-amber-900 flex items-center space-x-1">
              <span>Start</span>
              <ArrowRight className="w-3 h-3" />
            </span>
          </Link>

          <Link to="/members/m4444444-4444-4444-4444-444444444444/skill-gaps" className="p-3 rounded-xl border border-rose-200 bg-rose-50/50 hover:bg-rose-100/50 transition-all flex flex-col justify-between space-y-2">
            <div>
              <span className="text-[10px] font-extrabold text-rose-800 bg-rose-200 px-2 py-0.5 rounded-full">STEP 2</span>
              <h3 className="text-xs font-bold text-rose-950 mt-1.5">AI Skill Gap Diagnosis</h3>
              <p className="text-[11px] text-rose-800 leading-tight">Explainable normalized gap scores.</p>
            </div>
            <span className="text-[11px] font-bold text-rose-900 flex items-center space-x-1">
              <span>View Gaps</span>
              <ArrowRight className="w-3 h-3" />
            </span>
          </Link>

          <Link to="/courses/course-c01" className="p-3 rounded-xl border border-purple-200 bg-purple-50/50 hover:bg-purple-100/50 transition-all flex flex-col justify-between space-y-2">
            <div>
              <span className="text-[10px] font-extrabold text-purple-800 bg-purple-200 px-2 py-0.5 rounded-full">STEP 3</span>
              <h3 className="text-xs font-bold text-purple-950 mt-1.5">Personalised LMS Path</h3>
              <p className="text-[11px] text-purple-800 leading-tight">Offline-first interactive training.</p>
            </div>
            <span className="text-[11px] font-bold text-purple-900 flex items-center space-x-1">
              <span>Enrol Path</span>
              <ArrowRight className="w-3 h-3" />
            </span>
          </Link>

          <Link to="/learning" className="p-3 rounded-xl border border-blue-200 bg-blue-50/50 hover:bg-blue-100/50 transition-all flex flex-col justify-between space-y-2">
            <div>
              <span className="text-[10px] font-extrabold text-blue-800 bg-blue-200 px-2 py-0.5 rounded-full">STEP 4</span>
              <h3 className="text-xs font-bold text-blue-950 mt-1.5">AI Quiz & Certificate</h3>
              <p className="text-[11px] text-blue-800 leading-tight">Trainer-approved quiz evaluation.</p>
            </div>
            <span className="text-[11px] font-bold text-blue-900 flex items-center space-x-1">
              <span>Take Quiz</span>
              <ArrowRight className="w-3 h-3" />
            </span>
          </Link>

          <Link to="/opportunities/opp-o01" className="p-3 rounded-xl border border-emerald-200 bg-emerald-50/50 hover:bg-emerald-100/50 transition-all flex flex-col justify-between space-y-2">
            <div>
              <span className="text-[10px] font-extrabold text-emerald-800 bg-emerald-200 px-2 py-0.5 rounded-full">STEP 5</span>
              <h3 className="text-xs font-bold text-emerald-950 mt-1.5">AI Job Matching</h3>
              <p className="text-[11px] text-emerald-800 leading-tight">Explainable match score & placement.</p>
            </div>
            <span className="text-[11px] font-bold text-emerald-900 flex items-center space-x-1">
              <span>View Matches</span>
              <ArrowRight className="w-3 h-3" />
            </span>
          </Link>
        </div>
      </div>

      {/* Trainee Metric Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        
        <div className={`bg-white p-5 rounded-2xl border ${theme.cardAccent} shadow-sm flex items-center space-x-4`}>
          <div className={`w-12 h-12 rounded-xl ${theme.lightBg} ${theme.iconColor} flex items-center justify-center font-bold`}>
            <Users className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Role Readiness Score</p>
            <p className="text-2xl font-extrabold text-slate-900 mt-0.5">{data?.skill_readiness_score || 78.5}%</p>
          </div>
        </div>

        <div className={`bg-white p-5 rounded-2xl border ${theme.cardAccent} shadow-sm flex items-center space-x-4`}>
          <div className={`w-12 h-12 rounded-xl ${theme.lightBg} ${theme.iconColor} flex items-center justify-center font-bold`}>
            <BookOpen className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Completed Modules</p>
            <p className="text-2xl font-extrabold text-slate-900 mt-0.5">{data?.completed_courses || 1}</p>
          </div>
        </div>

        <div className={`bg-white p-5 rounded-2xl border ${theme.cardAccent} shadow-sm flex items-center space-x-4`}>
          <div className={`w-12 h-12 rounded-xl ${theme.lightBg} ${theme.iconColor} flex items-center justify-center font-bold`}>
            <Briefcase className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Job Applications</p>
            <p className="text-2xl font-extrabold text-slate-900 mt-0.5">{data?.job_applications || 1}</p>
          </div>
        </div>

        <div className={`bg-white p-5 rounded-2xl border ${theme.cardAccent} shadow-sm flex items-center space-x-4`}>
          <div className={`w-12 h-12 rounded-xl ${theme.lightBg} ${theme.iconColor} flex items-center justify-center font-bold`}>
            <Award className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">Capacity Growth</p>
            <p className="text-2xl font-extrabold text-emerald-600 mt-0.5">94.2%</p>
          </div>
        </div>

      </div>

      {/* Trainee Diagnostic & Jobs Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left: Skill Gaps Diagnostic */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-slate-800 flex items-center space-x-2">
              <BrainCircuit className="w-4 h-4 text-emerald-600" />
              <span>AI Skill-Gap Diagnostic</span>
            </h3>
            <Link to="/members/m4444444-4444-4444-4444-444444444444/skill-gaps" className="text-xs font-bold text-emerald-700 hover:underline flex items-center space-x-1">
              <span>View Full Diagnostic</span>
              <ArrowRight className="w-3 h-3" />
            </Link>
          </div>

          <div className="p-4 rounded-xl border border-rose-200 bg-rose-50/40 flex items-start justify-between">
            <div>
              <span className="text-[10px] font-extrabold text-rose-700 bg-rose-200 px-2 py-0.5 rounded-full uppercase">
                Critical Gap Detected
              </span>
              <h4 className="text-xs font-bold text-rose-950 mt-1">ERP Operations & Daily Batch Entry</h4>
              <p className="text-[11px] text-rose-800 mt-0.5">Required: Level 3 • Current Assessment: Level 1.5</p>
            </div>
            <Link to="/courses/course-c01" className="btn-primary text-xs py-1.5 px-3">
              Enrol Course
            </Link>
          </div>
        </div>

        {/* Right: Quick Action Card */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-4">
          <h3 className="text-sm font-bold text-slate-800 flex items-center space-x-2">
            <Briefcase className="w-4 h-4 text-emerald-600" />
            <span>Recommended Job Matches</span>
          </h3>

          <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-xs font-bold text-slate-900">PACS Billing Assistant</span>
              <span className="text-[10px] font-bold bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded">86% Match</span>
            </div>
            <p className="text-[11px] text-slate-500">Pragati Dairy Cooperative • Nashik</p>
            <Link to="/opportunities/opp-o01" className="text-[11px] font-bold text-emerald-700 hover:underline block pt-1">
              Review & Apply →
            </Link>
          </div>
        </div>

      </div>

    </div>
  );
};
