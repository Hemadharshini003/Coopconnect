import React from 'react';
import { useAuth } from '../../context/AuthContext';
import { useLanguage } from '../../context/LanguageContext';
import { getRoleTheme } from '../../utils/theme';
import { Globe, LogOut, Wifi, Monitor, Sparkles } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';

export const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  const { language, setLanguage, t } = useLanguage();
  const navigate = useNavigate();

  const theme = getRoleTheme(user?.role);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className={`${theme.headerBg} text-white shadow-md sticky top-0 z-40 transition-colors duration-300`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Brand Logo & Name */}
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-lg bg-amber-400 text-slate-900 border border-white/20 flex items-center justify-center font-extrabold text-xl shadow-inner">
            CC
          </div>
          <div>
            <Link to="/dashboard" className="font-bold text-lg leading-none hover:text-amber-200 flex items-center space-x-2">
              <span>COOPCONNECT</span>
            </Link>
            <p className={`text-[11px] ${theme.headerText} font-medium mt-0.5 hidden md:block`}>
              {theme.name} View • 20 Institutes Ecosystem
            </p>
          </div>
        </div>

        {/* Right Nav Actions */}
        <div className="flex items-center space-x-3">
          
          {/* Role Color Badge */}
          <div className="hidden sm:flex items-center space-x-1.5 bg-white/10 px-2.5 py-1 rounded-full text-[10px] font-extrabold uppercase border border-white/20 tracking-wider">
            <Sparkles className="w-3 h-3 text-amber-400" />
            <span className={theme.headerText}>{user?.role || 'MEMBER'}</span>
          </div>

          {/* Digital Kiosk Mode Link */}
          <Link
            to="/kiosk"
            className="flex items-center space-x-1 text-xs bg-amber-500 hover:bg-amber-600 text-slate-900 font-bold px-3 py-1.5 rounded-full transition-all shadow-sm"
          >
            <Monitor className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">{t('kiosk')}</span>
          </Link>

          {/* Online/Offline Status Indicator */}
          <div className="flex items-center space-x-1 text-xs bg-black/20 border border-white/10 px-2.5 py-1 rounded-full text-slate-200">
            <Wifi className="w-3 h-3 text-emerald-400 animate-pulse" />
            <span className="text-[11px]">Online</span>
          </div>

          {/* Language Switcher */}
          <div className="flex items-center space-x-1 bg-black/20 px-2 py-1 rounded-lg text-xs border border-white/10">
            <Globe className="w-3.5 h-3.5 text-amber-300" />
            <button
              onClick={() => setLanguage('en')}
              className={`px-1.5 py-0.5 rounded font-bold ${language === 'en' ? 'bg-amber-400 text-slate-900' : 'text-slate-200 hover:text-white'}`}
            >
              EN
            </button>
            <span className="text-slate-500">|</span>
            <button
              onClick={() => setLanguage('hi')}
              className={`px-1.5 py-0.5 rounded font-bold ${language === 'hi' ? 'bg-amber-400 text-slate-900' : 'text-slate-200 hover:text-white'}`}
            >
              हिंदी
            </button>
          </div>

          {/* User Profile Info & Logout */}
          {user && (
            <div className="flex items-center space-x-2 border-l border-white/20 pl-3">
              <div className="text-right hidden lg:block">
                <p className="text-xs font-bold leading-tight">{user.full_name}</p>
                <p className="text-[10px] text-slate-300 font-mono leading-tight">{user.email}</p>
              </div>
              <button
                onClick={handleLogout}
                title="Logout"
                className="p-2 hover:bg-white/10 rounded-lg text-slate-200 hover:text-white transition-colors"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          )}

        </div>
      </div>
    </header>
  );
};
