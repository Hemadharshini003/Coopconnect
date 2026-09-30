export interface RoleTheme {
  name: string;
  badge: string;
  headerBg: string;
  headerText: string;
  bannerBg: string;
  cardAccent: string;
  btnPrimary: string;
  iconColor: string;
  lightBg: string;
  description: string;
}

export const getRoleTheme = (role?: string): RoleTheme => {
  switch (role) {
    case 'NCCT_SUPER_ADMIN':
    case 'SUPER_ADMIN':
      return {
        name: 'NCCT National Super Admin',
        badge: 'NATIONAL HEADQUARTERS COMMAND',
        headerBg: 'bg-indigo-950',
        headerText: 'text-indigo-200',
        bannerBg: 'from-indigo-950 via-slate-900 to-indigo-900',
        cardAccent: 'border-indigo-500',
        btnPrimary: 'bg-indigo-700 hover:bg-indigo-800 text-white',
        iconColor: 'text-indigo-400',
        lightBg: 'bg-indigo-50/60',
        description: 'National training intelligence, 20 institutes oversight, programme governance, and central registry.'
      };

    case 'NCCT_PROGRAMME_ADMIN':
      return {
        name: 'NCCT National Programme Admin',
        badge: 'PROGRAMME GOVERNANCE & CALENDAR',
        headerBg: 'bg-blue-950',
        headerText: 'text-blue-200',
        bannerBg: 'from-blue-950 via-slate-900 to-indigo-900',
        cardAccent: 'border-blue-500',
        btnPrimary: 'bg-blue-700 hover:bg-blue-800 text-white',
        iconColor: 'text-blue-400',
        lightBg: 'bg-blue-50/60',
        description: 'Institute programme review, national calendar orchestration, and template standardization.'
      };

    case 'NCCT_ANALYTICS_OFFICER':
    case 'NCCT_AUDITOR':
      return {
        name: 'NCCT National Analytics & Auditor',
        badge: 'INTELLIGENCE & AUDIT REGISTRY',
        headerBg: 'bg-slate-950',
        headerText: 'text-slate-300',
        bannerBg: 'from-slate-950 via-slate-900 to-zinc-900',
        cardAccent: 'border-slate-500',
        btnPrimary: 'bg-slate-700 hover:bg-slate-800 text-white',
        iconColor: 'text-slate-400',
        lightBg: 'bg-slate-100',
        description: 'Cross-institute analytics, early warning trends, compliance verification, and audit logs.'
      };

    case 'NCCT_CERTIFICATE_AUTHORITY':
      return {
        name: 'NCCT Certificate Authority',
        badge: 'CENTRAL CERTIFICATE REGISTRY',
        headerBg: 'bg-amber-950',
        headerText: 'text-amber-200',
        bannerBg: 'from-amber-950 via-slate-900 to-amber-900',
        cardAccent: 'border-amber-500',
        btnPrimary: 'bg-amber-700 hover:bg-amber-800 text-white',
        iconColor: 'text-amber-400',
        lightBg: 'bg-amber-50/60',
        description: 'National certificate issuance, tamper-proof QR verification, and revocation authority.'
      };

    case 'INSTITUTE_ADMIN':
    case 'INSTITUTE_PROGRAMME_COORDINATOR':
    case 'COOPERATIVE_ADMIN':
      return {
        name: 'NCCT Institute Administrator',
        badge: 'INSTITUTE OPERATIONS & TIMETABLE',
        headerBg: 'bg-emerald-950',
        headerText: 'text-emerald-200',
        bannerBg: 'from-emerald-950 via-teal-900 to-slate-900',
        cardAccent: 'border-emerald-500',
        btnPrimary: 'bg-emerald-700 hover:bg-emerald-800 text-white',
        iconColor: 'text-emerald-400',
        lightBg: 'bg-emerald-50/60',
        description: 'Campus programme execution, batch timetable, trainer allocation, and local training outcomes.'
      };

    case 'TRAINER':
      return {
        name: 'NCCT Faculty / Master Trainer',
        badge: 'FACULTY & SESSION MANAGEMENT',
        headerBg: 'bg-purple-950',
        headerText: 'text-purple-200',
        bannerBg: 'from-purple-950 via-violet-900 to-slate-900',
        cardAccent: 'border-purple-500',
        btnPrimary: 'bg-purple-700 hover:bg-purple-800 text-white',
        iconColor: 'text-purple-400',
        lightBg: 'bg-purple-50/60',
        description: 'Class sessions, attendance check-in, trainee support recommendations, and quiz authoring.'
      };

    case 'RECRUITER':
    case 'PLACEMENT_OFFICER':
    case 'EMPLOYER_OR_COOPERATIVE_RECRUITER':
      return {
        name: 'Cooperative Recruiter & Employer Partner',
        badge: 'TALENT & OPPORTUNITY ECOSYSTEM',
        headerBg: 'bg-cyan-950',
        headerText: 'text-cyan-200',
        bannerBg: 'from-cyan-950 via-slate-900 to-teal-900',
        cardAccent: 'border-cyan-500',
        btnPrimary: 'bg-cyan-700 hover:bg-cyan-800 text-white',
        iconColor: 'text-cyan-400',
        lightBg: 'bg-cyan-50/60',
        description: 'Job postings, AI candidate match analysis, candidate review, and 30/60/90-day outcome follow-ups.'
      };

    case 'DISTRICT_ADMIN':
      return {
        name: 'District Cooperative Officer',
        badge: 'DISTRICT GOVERNANCE & GIS',
        headerBg: 'bg-indigo-950',
        headerText: 'text-indigo-200',
        bannerBg: 'from-indigo-950 via-slate-900 to-indigo-900',
        cardAccent: 'border-indigo-500',
        btnPrimary: 'bg-indigo-700 hover:bg-indigo-800 text-white',
        iconColor: 'text-indigo-400',
        lightBg: 'bg-indigo-50/60',
        description: 'District PACS oversight, cooperative health monitoring, and local skilling demand.'
      };

    case 'MEMBER':
    case 'TRAINEE':
    case 'EMPLOYEE':
    default:
      return {
        name: 'NCCT Trainee / Cooperative Member',
        badge: 'PERSONAL LEARNING & CAREER HUB',
        headerBg: 'bg-teal-950',
        headerText: 'text-amber-300',
        bannerBg: 'from-teal-950 via-emerald-900 to-slate-900',
        cardAccent: 'border-amber-400',
        btnPrimary: 'bg-amber-600 hover:bg-amber-700 text-white',
        iconColor: 'text-amber-400',
        lightBg: 'bg-amber-50/60',
        description: 'Skill profile, AI gap diagnosis, timetable schedule, personalized learning, and job applications.'
      };
  }
};
