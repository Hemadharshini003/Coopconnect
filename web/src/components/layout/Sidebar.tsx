import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { useLanguage } from '../../context/LanguageContext';
import { getRoleTheme } from '../../utils/theme';
import { 
  LayoutDashboard, 
  Building2, 
  Users, 
  BrainCircuit, 
  CheckSquare, 
  BookOpen, 
  Briefcase, 
  Award, 
  BarChart3, 
  Bell, 
  ShieldCheck, 
  UserCheck,
  User,
  GraduationCap,
  FileCheck,
  Settings,
  Database,
  Layers,
  FileText,
  Calendar,
  Lock
} from 'lucide-react';

export const Sidebar: React.FC = () => {
  const { user } = useAuth();
  const { t } = useLanguage();
  const theme = getRoleTheme(user?.role);

  const isHQUser = user?.role?.startsWith('NCCT_') || user?.role === 'SUPER_ADMIN';

  // Role-specific navigation menus
  const getNavItems = () => {
    if (isHQUser) {
      return [
        { to: '/hq/dashboard', label: 'NCCT HQ Dashboard', icon: LayoutDashboard },
        { to: '/hq/institutes', label: '20 NCCT Institutes', icon: Building2 },
        { to: '/hq/programme-approvals', label: 'Programme Approvals', icon: FileText },
        { to: '/hq/national-calendar', label: 'National Schedule', icon: Calendar },
        { to: '/hq/certificates', label: 'Certificate Registry', icon: Award },
        { to: '/hq/certificate-verification', label: 'QR Verification', icon: ShieldCheck },
        { to: '/hq/settings', label: 'National Templates', icon: Layers },
        { to: '/hq/audit-logs', label: 'Audit Trail', icon: Lock },
        { to: '/notifications', label: 'Notifications', icon: Bell },
      ];
    }

    switch (user?.role) {
      case 'MEMBER':
      case 'TRAINEE':
      case 'EMPLOYEE':
        return [
          { to: '/dashboard', label: 'My Learning Hub', icon: LayoutDashboard },
          { to: '/members/m4444444-4444-4444-4444-444444444444/skill-gaps', label: 'AI Skill-Gap Analysis', icon: BrainCircuit },
          { to: '/assessments', label: 'Take Skill Assessment', icon: CheckSquare },
          { to: '/courses', label: 'Learning Modules', icon: BookOpen },
          { to: '/learning', label: 'Interactive Player', icon: GraduationCap },
          { to: '/opportunities', label: 'Job Opportunities', icon: Briefcase },
          { to: '/applications', label: 'My Applications', icon: UserCheck },
          { to: '/notifications', label: 'Notifications', icon: Bell },
        ];

      case 'COOPERATIVE_ADMIN':
      case 'INSTITUTE_ADMIN':
        return [
          { to: '/dashboard', label: 'Institute Dashboard', icon: LayoutDashboard },
          { to: '/cooperatives', label: 'Cooperative Profile', icon: Building2 },
          { to: '/members', label: 'Member Roster', icon: Users },
          { to: '/opportunities', label: 'Job Postings', icon: Briefcase },
          { to: '/applications', label: 'Applications', icon: UserCheck },
          { to: '/placements', label: 'Placements', icon: Award },
          { to: '/notifications', label: 'Notifications', icon: Bell },
        ];

      case 'EMPLOYER_OR_COOPERATIVE_RECRUITER':
        return [
          { to: '/dashboard', label: 'Recruiter Dashboard', icon: LayoutDashboard },
          { to: '/opportunities', label: 'Manage Job Openings', icon: Briefcase },
          { to: '/opportunities/opp-o01', label: 'AI Candidate Matches', icon: BrainCircuit },
          { to: '/applications', label: 'Review Applications', icon: UserCheck },
          { to: '/placements', label: 'Record Placements', icon: Award },
          { to: '/notifications', label: 'Notifications', icon: Bell },
        ];

      case 'TRAINER':
        return [
          { to: '/dashboard', label: 'Trainer Dashboard', icon: LayoutDashboard },
          { to: '/courses', label: 'Manage Courses', icon: BookOpen },
          { to: '/courses/course-c01', label: 'AI Quiz Approvals', icon: FileCheck },
          { to: '/notifications', label: 'Notifications', icon: Bell },
        ];

      case 'DISTRICT_ADMIN':
        return [
          { to: '/dashboard', label: 'District Dashboard', icon: LayoutDashboard },
          { to: '/cooperatives', label: 'District Societies', icon: Building2 },
          { to: '/analytics', label: 'GIS Map & Analytics', icon: BarChart3 },
          { to: '/placements', label: 'Placement Outcomes', icon: Award },
          { to: '/notifications', label: 'Notifications', icon: Bell },
        ];

      default:
        return [
          { to: '/dashboard', label: 'System Overview', icon: LayoutDashboard },
          { to: '/cooperatives', label: 'All Cooperatives', icon: Building2 },
          { to: '/members', label: 'All Members', icon: Users },
          { to: '/analytics', label: 'System Analytics', icon: BarChart3 },
          { to: '/admin/users', label: 'User RBAC Admin', icon: ShieldCheck },
          { to: '/admin/audit-logs', label: 'Audit Logs', icon: Database },
          { to: '/notifications', label: 'Notifications', icon: Bell },
        ];
    }
  };

  const navItems = getNavItems();

  return (
    <aside className="w-64 bg-white border-r border-slate-200 min-h-[calc(100vh-4rem)] p-4 flex flex-col justify-between hidden md:flex">
      <div className="space-y-1">
        <div className="px-3 mb-3 pb-2 border-b border-slate-100">
          <p className="text-[10px] font-extrabold text-indigo-600 uppercase tracking-wider">
            {user?.role || 'MEMBER'} NAVIGATION
          </p>
          <p className="text-xs font-bold text-slate-800 mt-0.5 truncate">
            {isHQUser ? 'NCCT HQ Governance' : theme.name}
          </p>
        </div>

        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? `bg-indigo-50 text-indigo-900 border-l-4 border-indigo-600 font-bold shadow-sm`
                    : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                }`
              }
            >
              <Icon className={`w-5 h-5 ${isHQUser ? 'text-indigo-600' : theme.iconColor}`} />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </div>

      {/* AI Engine Status Badge */}
      <div className="bg-indigo-50/70 p-3.5 rounded-xl border border-indigo-200 mt-6 space-y-1">
        <div className="flex items-center space-x-2 text-xs font-bold text-indigo-950">
          <BrainCircuit className="w-4 h-4 text-indigo-600 animate-spin" />
          <span>NCCT Governance Active</span>
        </div>
        <p className="text-[11px] text-indigo-800 leading-tight">
          20 Institutes multi-tenant scope guards & national analytics enabled.
        </p>
      </div>
    </aside>
  );
};
