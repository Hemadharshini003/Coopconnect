export type UserRole = 
  | 'NCCT_SUPER_ADMIN'
  | 'NCCT_PROGRAMME_ADMIN'
  | 'NCCT_ANALYTICS_OFFICER'
  | 'NCCT_CERTIFICATE_AUTHORITY'
  | 'NCCT_AUDITOR'
  | 'INSTITUTE_ADMIN'
  | 'INSTITUTE_PROGRAMME_COORDINATOR'
  | 'TRAINER'
  | 'ATTENDANCE_OPERATOR'
  | 'PLACEMENT_OFFICER'
  | 'RECRUITER'
  | 'KIOSK_OPERATOR'
  | 'INSTITUTE_AUDITOR'
  | 'TRAINEE'
  | 'SUPER_ADMIN' 
  | 'DISTRICT_ADMIN' 
  | 'COOPERATIVE_ADMIN' 
  | 'MEMBER' 
  | 'EMPLOYEE' 
  | 'EMPLOYER_OR_COOPERATIVE_RECRUITER' 
  | 'AUDITOR';

export interface User {
  id: string;
  email: string;
  full_name: string;
  phone?: string;
  role: UserRole;
  preferred_language: string;
  district_id?: string;
  cooperative_id?: string;
  institute_id?: string;
}

export interface MemberProfile {
  id: string;
  user_id: string;
  full_name?: string;
  email?: string;
  phone?: string;
  membership_number?: string;
  education_level?: string;
  occupation?: string;
  years_of_experience?: number;
  profile_completion_percentage?: number;
  user?: User;
}

export interface Cooperative {
  id: string;
  name: string;
  registration_number: string;
  cooperative_type: string;
  description?: string;
  state: string;
  district_id?: string;
  institute_id?: string;
  block?: string;
  village?: string;
  address?: string;
  phone?: string;
  email?: string;
  health_score?: number;
  is_active: boolean;
}

export interface Skill {
  id: string;
  name: string;
  code: string;
  category: string;
  description?: string;
}

export interface Course {
  id: string;
  title: string;
  description: string;
  category: string;
  level?: string;
  difficulty?: string;
  language?: string;
  duration_minutes: number;
  is_published: boolean;
  institute_id?: string;
  lessons?: any[];
}

export interface Opportunity {
  id: string;
  title: string;
  description: string;
  opportunity_type: string;
  location: string;
  remote_allowed: boolean;
  status: string;
  institute_id?: string;
  stipend_or_salary?: string;
  created_at?: string;
}
