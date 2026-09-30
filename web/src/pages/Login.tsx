import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LogIn, Key, Mail, ShieldAlert, Monitor, Sparkles } from 'lucide-react';
import { API_BASE } from '../services/api';
export const Login: React.FC = () => {
  const [email, setEmail] = useState('hqadmin@ncct.gov.in');
  const [password, setPassword] = useState('ChangeMe123!');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);

      const res = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: formData,
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || 'Login failed');
      }

      login(data.access_token, data.user);

      // Role-Based Routing
      const userRole = data.user?.role || '';
      if (userRole.startsWith('NCCT_') || userRole === 'SUPER_ADMIN') {
        navigate('/hq/dashboard');
      } else {
        navigate('/dashboard');
      }
    } catch (err: any) {
      setError(err.message || 'Invalid email or password');
    } finally {
      setLoading(false);
    }
  };

  const setQuickUser = (sampleEmail: string) => {
    setEmail(sampleEmail);
    setPassword('ChangeMe123!');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-950 via-slate-900 to-indigo-950 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white rounded-2xl shadow-2xl overflow-hidden border border-emerald-500/20">

        {/* Header */}
        <div className="bg-slate-950 p-6 text-center text-white relative border-b border-emerald-500/30">
          <div className="w-16 h-16 bg-amber-400 text-slate-950 rounded-2xl border border-amber-300 flex items-center justify-center mx-auto mb-3 shadow-lg font-black text-2xl">
            CC
          </div>
          <h1 className="text-2xl font-bold tracking-tight">COOPCONNECT</h1>
          <p className="text-xs text-emerald-300 mt-1">Training Intelligence & Outcome Ecosystem (20 Institutes)</p>
        </div>

        {/* Form Body */}
        <div className="p-6 space-y-5">
          {error && (
            <div className="bg-rose-50 border border-rose-200 text-rose-700 px-4 py-3 rounded-lg text-xs flex items-center space-x-2">
              <ShieldAlert className="w-4 h-4 flex-shrink-0 text-rose-500" />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Email Address</label>
              <div className="relative">
                <Mail className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className="w-full pl-9 pr-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-emerald-600 focus:outline-none"
                  placeholder="hqadmin@ncct.gov.in"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Password</label>
              <div className="relative">
                <Key className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  className="w-full pl-9 pr-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-emerald-600 focus:outline-none"
                  placeholder="•••••••••"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-emerald-700 hover:bg-emerald-800 text-white py-2.5 rounded-lg flex items-center justify-center space-x-2 text-sm font-bold shadow-md transition-all"
            >
              <LogIn className="w-4 h-4" />
              <span>{loading ? 'Authenticating...' : 'Sign In to COOPCONNECT'}</span>
            </button>
          </form>

          {/* Quick Demo Role Switcher */}
          <div className="bg-slate-50 border border-slate-200 p-3 rounded-xl space-y-2">
            <div className="flex items-center space-x-1.5 text-[11px] font-bold text-slate-600">
              <Sparkles className="w-3.5 h-3.5 text-amber-500" />
              <span>Demo Quick Sign-In</span>
            </div>
            <div className="grid grid-cols-2 gap-1.5 text-[10px]">
              <button
                type="button"
                onClick={() => setQuickUser('hqadmin@ncct.gov.in')}
                className="bg-indigo-50 hover:bg-indigo-100 text-indigo-900 border border-indigo-200 p-1.5 rounded font-semibold text-left transition-colors truncate"
              >
                🏢 NCCT HQ Admin
              </button>
              <button
                type="button"
                onClick={() => setQuickUser('admin.blr@ricm.ncct.gov.in')}
                className="bg-emerald-50 hover:bg-emerald-100 text-emerald-900 border border-emerald-200 p-1.5 rounded font-semibold text-left transition-colors truncate"
              >
                🏫 Institute Admin (BLR)
              </button>
              <button
                type="button"
                onClick={() => setQuickUser('trainer.blr@ricm.ncct.gov.in')}
                className="bg-purple-50 hover:bg-purple-100 text-purple-900 border border-purple-200 p-1.5 rounded font-semibold text-left transition-colors truncate"
              >
                👨‍🏫 Faculty / Trainer
              </button>
              <button
                type="button"
                onClick={() => setQuickUser('meena.patil@ruralcoop.in')}
                className="bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-200 p-1.5 rounded font-semibold text-left transition-colors truncate"
              >
                🎓 Trainee (Meena)
              </button>
            </div>
          </div>

          {/* Kiosk direct link */}
          <div className="bg-amber-50 border border-amber-200 p-2.5 rounded-lg text-center">
            <Link to="/kiosk" className="text-xs font-bold text-amber-900 flex items-center justify-center space-x-1 hover:underline">
              <Monitor className="w-4 h-4 text-amber-700" />
              <span>Launch Shared Tablet Kiosk Mode</span>
            </Link>
          </div>

        </div>
      </div>
    </div>
  );
};
