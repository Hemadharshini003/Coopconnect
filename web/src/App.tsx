import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { LanguageProvider } from './context/LanguageContext';
import { Navbar } from './components/layout/Navbar';
import { Sidebar } from './components/layout/Sidebar';

// Pages
import { Login } from './pages/Login';
import { Dashboard } from './pages/Dashboard';
import { Cooperatives } from './pages/Cooperatives';
import { Members } from './pages/Members';
import { SkillGaps } from './pages/SkillGaps';
import { Courses } from './pages/Courses';
import { CourseDetail } from './pages/CourseDetail';
import { LearningPlayer } from './pages/LearningPlayer';
import { Opportunities } from './pages/Opportunities';
import { OpportunityDetail } from './pages/OpportunityDetail';
import { Applications } from './pages/Applications';
import { Placements } from './pages/Placements';
import { Analytics } from './pages/Analytics';
import { Notifications } from './pages/Notifications';
import { AdminUsers } from './pages/AdminUsers';
import { KioskMode } from './pages/KioskMode';
import { HQGovernancePortal } from './pages/hq/HQGovernancePortal';

const ProtectedLayout = () => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <div className="p-8 text-center text-xs text-slate-500">Loading CoopConnect AI App...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="min-h-screen flex flex-col bg-coop-greyBg">
      <Navbar />
      <div className="flex flex-1 max-w-7xl w-full mx-auto">
        <Sidebar />
        <main className="flex-1 p-4 sm:p-6 lg:p-8 overflow-y-auto">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export const App: React.FC = () => {
  return (
    <AuthProvider>
      <LanguageProvider>
        <Router future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/kiosk" element={<KioskMode />} />

            {/* Protected Routes */}
            <Route element={<ProtectedLayout />}>
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/cooperatives" element={<Cooperatives />} />
              <Route path="/cooperatives/:id" element={<Cooperatives />} />
              <Route path="/members" element={<Members />} />
              <Route path="/members/:id" element={<Members />} />
              <Route path="/members/:id/skills" element={<SkillGaps />} />
              <Route path="/members/:id/skill-gaps" element={<SkillGaps />} />
              <Route path="/assessments" element={<SkillGaps />} />
              <Route path="/courses" element={<Courses />} />
              <Route path="/courses/:id" element={<CourseDetail />} />
              <Route path="/learning" element={<LearningPlayer />} />
              <Route path="/opportunities" element={<Opportunities />} />
              <Route path="/opportunities/:id" element={<OpportunityDetail />} />
              <Route path="/applications" element={<Applications />} />
              <Route path="/placements" element={<Placements />} />
              <Route path="/analytics" element={<Analytics />} />
              <Route path="/notifications" element={<Notifications />} />
              <Route path="/admin/users" element={<AdminUsers />} />
              <Route path="/admin/audit-logs" element={<AdminUsers />} />

              {/* NCCT Headquarters Routes */}
              <Route path="/hq" element={<Navigate to="/hq/dashboard" replace />} />
              <Route path="/hq/dashboard" element={<HQGovernancePortal initialTab="dashboard" />} />
              <Route path="/hq/institutes" element={<HQGovernancePortal initialTab="institutes" />} />
              <Route path="/hq/institutes/:id" element={<HQGovernancePortal initialTab="institutes" />} />
              <Route path="/hq/programmes" element={<HQGovernancePortal initialTab="programme-approvals" />} />
              <Route path="/hq/programme-approvals" element={<HQGovernancePortal initialTab="programme-approvals" />} />
              <Route path="/hq/national-calendar" element={<HQGovernancePortal initialTab="national-calendar" />} />
              <Route path="/hq/analytics" element={<HQGovernancePortal initialTab="dashboard" />} />
              <Route path="/hq/reports" element={<HQGovernancePortal initialTab="dashboard" />} />
              <Route path="/hq/certificates" element={<HQGovernancePortal initialTab="certificates" />} />
              <Route path="/hq/certificate-verification" element={<HQGovernancePortal initialTab="certificate-verification" />} />
              <Route path="/hq/audit-logs" element={<HQGovernancePortal initialTab="audit-logs" />} />
              <Route path="/hq/users" element={<HQGovernancePortal initialTab="institutes" />} />
              <Route path="/hq/settings" element={<HQGovernancePortal initialTab="templates" />} />
            </Route>

            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </Router>
      </LanguageProvider>
    </AuthProvider>
  );
};

export default App;
