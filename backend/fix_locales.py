import os

hi_code = """export const hi = {
  app_name: "कॉपकनेक्ट (COOPCONNECT)",
  subtitle: "एआई-सक्षम सहकारी प्रशिक्षण बुद्धिमत्ता और परिणाम मंच",
  login: "लॉग इन करें",
  register: "पंजीकरण करें",
  logout: "लॉग आउट",
  dashboard: "डैशबोर्ड",
  profile: "सदस्य प्रोफ़ाइल",
  cooperatives: "सहकारी समितियाँ",
  members: "सदस्य और प्रशिक्षु",
  skills: "कौशल और दक्षताएं",
  skill_gaps: "कौशल-अंतर निदान",
  assessments: "मूल्यांकन",
  courses: "प्रशिक्षण पाठ्यक्रम",
  opportunities: "रोज़गार अवसर",
  applications: "आवेदन",
  placements: "प्लेसमेंट और परिणाम",
  analytics: "एनालिटिक्स",
  notifications: "सूचनाएं",
  admin: "प्रशासन",
  kiosk: "डिजिटल कियोस्क मोड",
  offline_status: "ऑफ़लाइन तैयार",
  sync_pending: "सिंक लंबित",
  synced: "सभी रिकॉर्ड सिंक हुए"
};
"""

with open(r"C:\Users\ADMIN\.gemini\antigravity\scratch\coopconnect-ai\web\src\locales\hi.ts", "w", encoding="utf-8") as f:
    f.write(hi_code)

kiosk_code = """import React, { useState } from 'react';
import { Monitor, QrCode, Search, Volume2, Globe, Wifi, RefreshCw, CheckCircle2, ArrowRight, BookOpen, Award } from 'lucide-react';
import { saveOfflineCourse, enqueueOfflineAction, getPendingSyncQueue } from '../services/offlineStore';

export const KioskMode: React.FC = () => {
  const [lang, setLang] = useState<'hi' | 'en'>('hi');
  const [membershipId, setMembershipId] = useState('PRAGATI-MBR-2024-089');
  const [memberFound, setMemberFound] = useState(true);
  const [selectedModule, setSelectedModule] = useState<string | null>(null);
  const [speaking, setSpeaking] = useState(false);

  const [quizAnswer, setQuizAnswer] = useState('');
  const [quizSubmitted, setQuizSubmitted] = useState(false);
  const [syncCount, setSyncCount] = useState(0);

  const speakVoice = (text: string) => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = lang === 'hi' ? 'hi-IN' : 'en-US';
      utterance.onend = () => setSpeaking(false);
      setSpeaking(true);
      window.speechSynthesis.speak(utterance);
    }
  };

  const handleLookup = (e: React.FormEvent) => {
    e.preventDefault();
    if (membershipId.trim()) {
      setMemberFound(true);
      speakVoice(lang === 'hi' ? 'नमस्ते मीना जाधव, कॉपकनेक्ट डिजिटल कियोस्क में आपका स्वागत है।' : 'Welcome Meena Jadhav to CoopConnect Digital Kiosk.');
    }
  };

  const submitKioskQuiz = async () => {
    setQuizSubmitted(true);
    // Queue offline sync event
    await enqueueOfflineAction('KIOSK_QUIZ_ATTEMPT', {
      membership_number: membershipId,
      course_id: 'course-c01',
      score: 100,
      timestamp: new Date().toISOString()
    });

    const queue = await getPendingSyncQueue();
    setSyncCount(queue.length);
    speakVoice(lang === 'hi' ? 'प्रश्नोत्तरी पूर्ण हुई। परिणाम ऑफ़लाइन सहेजा गया।' : 'Quiz completed. Result saved offline.');
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white p-4 sm:p-8 flex flex-col justify-between font-sans">
      
      {/* Top Kiosk Header */}
      <div className="flex items-center justify-between bg-slate-800 p-4 rounded-2xl border border-slate-700 shadow-lg">
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 bg-amber-500 text-slate-900 rounded-xl flex items-center justify-center font-extrabold text-xl shadow-md">
            CC
          </div>
          <div>
            <h1 className="text-lg font-bold text-amber-300">COOPCONNECT — Digital Kiosk</h1>
            <p className="text-xs text-slate-400">Rural Hardware Touchscreen Mode (Offline Ready)</p>
          </div>
        </div>

        {/* Audio & Language controls */}
        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-1 bg-slate-700 p-1.5 rounded-xl border border-slate-600">
            <button
              onClick={() => setLang('hi')}
              className={`px-3 py-1 rounded-lg text-xs font-bold ${lang === 'hi' ? 'bg-amber-500 text-slate-900' : 'text-slate-300'}`}
            >
              हिंदी
            </button>
            <button
              onClick={() => setLang('en')}
              className={`px-3 py-1 rounded-lg text-xs font-bold ${lang === 'en' ? 'bg-amber-500 text-slate-900' : 'text-slate-300'}`}
            >
              English
            </button>
          </div>

          <button
            onClick={() => speakVoice(lang === 'hi' ? 'कॉपकनेक्ट डिजिटल कियोस्क में आपका स्वागत है। अपना सदस्य पहचान नंबर दर्ज करें।' : 'Welcome to CoopConnect Digital Kiosk. Please enter your membership ID.')}
            className={`p-2.5 rounded-xl border border-slate-600 text-amber-300 hover:bg-slate-700 transition-colors ${speaking ? 'animate-pulse bg-amber-500/20' : 'bg-slate-800'}`}
            title="Read Screen Aloud"
          >
            <Volume2 className="w-5 h-5" />
          </button>

          <div className="flex items-center space-x-1.5 bg-emerald-900/40 text-emerald-400 border border-emerald-500/30 px-3 py-1.5 rounded-xl text-xs font-bold">
            <Wifi className="w-4 h-4" />
            <span>{lang === 'hi' ? 'ऑफ़लाइन तैयार' : 'Offline Ready'}</span>
          </div>
        </div>
      </div>

      {/* Main Touch Interaction Area */}
      <div className="max-w-4xl w-full mx-auto my-6 space-y-6 flex-1">
        
        {/* Member Lookup Bar */}
        <div className="bg-slate-800/90 p-6 rounded-3xl border border-slate-700 shadow-2xl space-y-4">
          <label className="block text-sm font-bold text-slate-300 flex items-center space-x-2">
            <QrCode className="w-5 h-5 text-amber-400" />
            <span>{lang === 'hi' ? 'कृपया सदस्य पहचान या सदस्यता संख्या दर्ज करें:' : 'Enter Member ID or Membership Number:'}</span>
          </label>
          
          <form onSubmit={handleLookup} className="flex gap-3">
            <input
              type="text"
              value={membershipId}
              onChange={(e) => setMembershipId(e.target.value)}
              className="flex-1 bg-slate-900 border-2 border-slate-600 rounded-2xl px-5 py-3 text-lg font-mono text-amber-300 focus:outline-none focus:border-amber-400"
              placeholder="PRAGATI-MBR-2024-089"
            />
            <button
              type="submit"
              className="bg-amber-500 hover:bg-amber-600 text-slate-900 font-extrabold px-8 py-3 rounded-2xl text-base flex items-center space-x-2 shadow-lg transition-all"
            >
              <Search className="w-5 h-5" />
              <span>{lang === 'hi' ? 'खोजें' : 'Lookup'}</span>
            </button>
          </form>

          {/* Member Profile Confirmation Card */}
          {memberFound && (
            <div className="p-4 bg-emerald-950/40 border border-emerald-500/40 rounded-2xl flex items-center justify-between mt-4">
              <div>
                <span className="text-[10px] font-extrabold text-emerald-400 uppercase tracking-wider">
                  {lang === 'hi' ? 'सत्यापित सदस्य प्रोफ़ाइल' : 'VERIFIED MEMBER PROFILE'}
                </span>
                <h2 className="text-xl font-black text-white mt-0.5">
                  Meena Jadhav {lang === 'hi' ? '(मीना जाधव)' : ''}
                </h2>
                <p className="text-xs text-slate-300">Pragati Dairy Cooperative • Sinnar, Nashik</p>
              </div>
              <button
                onClick={() => speakVoice(lang === 'hi' ? 'मीना जाधव, प्रगति डेयरी सहकारी, नाशिक।' : 'Meena Jadhav, Pragati Dairy Cooperative, Nashik.')}
                className="p-2.5 bg-slate-800 hover:bg-slate-700 text-amber-300 rounded-xl border border-slate-600 text-xs font-bold flex items-center space-x-1.5"
              >
                <Volume2 className="w-4 h-4" />
                <span>{lang === 'hi' ? 'सुनें' : 'Listen'}</span>
              </button>
            </div>
          )}
        </div>

        {/* Modules & Micro Learning Deck */}
        {memberFound && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-base font-bold text-slate-200 flex items-center space-x-2">
                <BookOpen className="w-5 h-5 text-amber-400" />
                <span>{lang === 'hi' ? 'अनुशंसित मॉड्यूल और पाठ' : 'Recommended Learning Modules & Lessons'}</span>
              </h3>
              <span className="text-xs text-slate-400">
                {lang === 'hi' ? 'ऑफ़लाइन मोड (स्थानीय कैश)' : 'Touch to start module'}
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              
              {/* Module 1 */}
              <div 
                onClick={() => setSelectedModule('m1')}
                className={`p-5 rounded-2xl border transition-all cursor-pointer ${selectedModule === 'm1' ? 'bg-slate-800 border-amber-400 ring-2 ring-amber-400/30' : 'bg-slate-800/70 border-slate-700 hover:bg-slate-800'}`}
              >
                <span className="text-[10px] font-extrabold bg-rose-900/60 text-rose-300 border border-rose-500/30 px-2.5 py-0.5 rounded-full uppercase">
                  {lang === 'hi' ? 'महत्वपूर्ण कौशल अंतर' : 'Critical Skill Gap'}
                </span>
                <h4 className="text-base font-bold text-white mt-2">
                  {lang === 'hi' ? 'ईआरपी मूल बातें और दैनिक संग्रह लॉग' : 'ERP Fundamentals & Daily Collection Log'}
                </h4>
                <p className="text-xs text-slate-400 mt-1">
                  {lang === 'hi' ? 'अवधि: 20 मिनट • ऑडियो निर्देशित' : 'Duration: 20 Mins • Audio Guided'}
                </p>
                <button className="mt-4 w-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-2 rounded-xl text-xs flex items-center justify-center space-x-1 shadow">
                  <span>{lang === 'hi' ? 'पाठ शुरू करें (ऑफ़लाइन उपलब्ध)' : 'Start Lesson (Cached Offline)'}</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>

              {/* Module 2 */}
              <div 
                onClick={() => setSelectedModule('m2')}
                className={`p-5 rounded-2xl border transition-all cursor-pointer ${selectedModule === 'm2' ? 'bg-slate-800 border-amber-400 ring-2 ring-amber-400/30' : 'bg-slate-800/70 border-slate-700 hover:bg-slate-800'}`}
              >
                <span className="text-[10px] font-extrabold bg-blue-900/60 text-blue-300 border border-blue-500/30 px-2.5 py-0.5 rounded-full uppercase">
                  {lang === 'hi' ? 'डिजिटल साक्षरता' : 'Digital Literacy'}
                </span>
                <h4 className="text-base font-bold text-white mt-2">
                  {lang === 'hi' ? 'डिजिटल भुगतान और यूपीआई मिलान' : 'Digital Payment & UPI Reconciliation'}
                </h4>
                <p className="text-xs text-slate-400 mt-1">
                  {lang === 'hi' ? 'अवधि: 15 मिनट • स्थानीय कैश' : 'Duration: 15 Mins • Local Cache'}
                </p>
                <button className="mt-4 w-full bg-slate-700 hover:bg-slate-600 text-white font-bold py-2 rounded-xl text-xs flex items-center justify-center space-x-1 shadow">
                  <span>{lang === 'hi' ? 'पाठ शुरू करें' : 'Start Lesson'}</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>

            </div>

            {/* Offline Micro-Quiz Section */}
            {selectedModule && (
              <div className="p-6 bg-slate-800 rounded-3xl border border-amber-400/40 shadow-xl space-y-4 animate-fadeIn">
                <div className="flex items-center justify-between border-b border-slate-700 pb-3">
                  <div className="flex items-center space-x-2">
                    <Award className="w-5 h-5 text-amber-400" />
                    <h4 className="text-sm font-bold text-amber-300">
                      {lang === 'hi' ? 'त्वरित ऑफ़लाइन प्रश्नोत्तरी (100% स्कोर)' : 'Quick Offline Quiz (Module 1 Assessment)'}
                    </h4>
                  </div>
                  <button
                    onClick={() => speakVoice(lang === 'hi' ? 'प्रश्न: सहकारी समिति में दैनिक नकद मिलान के लिए कौन सा दस्तावेज़ आवश्यक है?' : 'Question: Which register is mandatory for recording daily cash in PACS?')}
                    className="p-1.5 text-amber-300 hover:bg-slate-700 rounded-lg"
                  >
                    <Volume2 className="w-4 h-4" />
                  </button>
                </div>

                <p className="text-sm font-semibold text-slate-100">
                  {lang === 'hi' 
                    ? 'प्रश्न 1: सहकारी समिति में दैनिक नकद और बैंक लेन-देन दर्ज करने के लिए कौन सी बही अनिवार्य है?' 
                    : 'Q1: Which ledger is mandatory for daily cash & bank entries in cooperative societies?'}
                </p>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <button
                    onClick={() => setQuizAnswer('A')}
                    className={`p-4 rounded-xl border font-bold text-sm text-left transition-all ${quizAnswer === 'A' ? 'bg-amber-500 text-slate-900 border-amber-400 font-extrabold shadow-lg' : 'bg-slate-700/80 border-slate-600 hover:bg-slate-700'}`}
                  >
                    {lang === 'hi' ? 'A) दैनिक रोकड़ बही (Day Book)' : 'A) PACS Day Book & Cash Ledger'}
                  </button>
                  <button
                    onClick={() => setQuizAnswer('B')}
                    className={`p-4 rounded-xl border font-bold text-sm text-left transition-all ${quizAnswer === 'B' ? 'bg-amber-500 text-slate-900 border-amber-400 font-extrabold shadow-lg' : 'bg-slate-700/80 border-slate-600 hover:bg-slate-700'}`}
                  >
                    {lang === 'hi' ? 'B) आगंतुक पुस्तिका (Visitor Book)' : 'B) Visitor Attendance Book'}
                  </button>
                </div>

                <button
                  onClick={submitKioskQuiz}
                  disabled={!quizAnswer || quizSubmitted}
                  className="w-full bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white font-black py-3 rounded-2xl text-sm flex items-center justify-center space-x-2 shadow-lg transition-all"
                >
                  <CheckCircle2 className="w-5 h-5" />
                  <span>
                    {quizSubmitted 
                      ? (lang === 'hi' ? 'परिणाम स्थानीय रूप से सहेजा गया ✓' : 'Result Saved in SQLite Queue ✓') 
                      : (lang === 'hi' ? 'प्रश्नोत्तरी सबमिट करें' : 'Submit Quiz Answer')}
                  </span>
                </button>
              </div>
            )}

          </div>
        )}

      </div>

      {/* Kiosk Footer with Auto-Sync Status */}
      <div className="bg-slate-800/80 p-4 rounded-2xl border border-slate-700 flex items-center justify-between text-xs text-slate-400">
        <div className="flex items-center space-x-2">
          <RefreshCw className="w-4 h-4 text-emerald-400 animate-spin" />
          <span>{lang === 'hi' ? 'स्थानीय SQLite ऑफ़लाइन सिंक इंजन सक्रिय' : 'Local SQLite Offline Queue Active'}</span>
        </div>
        <div className="flex items-center space-x-2">
          <span className="font-mono text-amber-300">{syncCount} {lang === 'hi' ? 'सिंक लंबित' : 'Pending Operations'}</span>
          <span>• Kiosk Device #K-MH-042</span>
        </div>
      </div>

    </div>
  );
};
"""

with open(r"C:\Users\ADMIN\.gemini\antigravity\scratch\coopconnect-ai\web\src\pages\KioskMode.tsx", "w", encoding="utf-8") as f:
    f.write(kiosk_code)

print("Locales and KioskMode.tsx successfully written with clean UTF-8 Hindi & English!")
