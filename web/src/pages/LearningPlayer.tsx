import React, { useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { Volume2, CheckCircle2, ArrowRight, ShieldCheck, Award } from 'lucide-react';

export const LearningPlayer: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const [activeTab, setActiveTab] = useState<'lesson' | 'quiz'>('lesson');
  const [speaking, setSpeaking] = useState(false);
  
  // Quiz states
  const [q1Ans, setQ1Ans] = useState('');
  const [q2Ans, setQ2Ans] = useState('');
  const [quizSubmitted, setQuizSubmitted] = useState(false);
  const [score, setScore] = useState<number | null>(null);

  const lessonTitle = "Module 1: Cooperative ERP Navigation & Daily Batch Entry";
  const lessonBody = `
  Welcome to the ERP Fundamentals Module.
  In this lesson, cooperative members and inventory staff learn how to log into the ERP portal, record incoming daily milk batches, verify fat percentage data, and generate shift reconciliation reports.
  
  Key Operational Steps:
  1. Open the CoopConnect AI Kiosk or Mobile app interface.
  2. Input Member ID or scan member QR code.
  3. Enter milk volume in liters and fat reading.
  4. Tap 'Synchronize' to submit the batch to the central cooperative ledger.
  `;

  const speakText = () => {
    if ('speechSynthesis' in window) {
      if (speaking) {
        window.speechSynthesis.cancel();
        setSpeaking(false);
      } else {
        const utterance = new SpeechSynthesisUtterance(lessonBody);
        utterance.onend = () => setSpeaking(false);
        setSpeaking(true);
        window.speechSynthesis.speak(utterance);
      }
    }
  };

  const handleQuizSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    let calculated = 0;
    if (q1Ans.includes("operational steps")) calculated += 50;
    if (q2Ans === "True") calculated += 50;

    setScore(calculated);
    setQuizSubmitted(true);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      
      {/* Header Tabs */}
      <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
        <div>
          <span className="badge badge-active text-[10px]">ERP FUNDAMENTALS</span>
          <h2 className="text-base font-bold text-slate-900 mt-0.5">{lessonTitle}</h2>
        </div>

        <div className="flex space-x-2">
          <button
            onClick={() => setActiveTab('lesson')}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
              activeTab === 'lesson' ? 'bg-coop-dark text-white' : 'bg-slate-100 text-slate-700'
            }`}
          >
            Lesson Content
          </button>
          <button
            onClick={() => setActiveTab('quiz')}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
              activeTab === 'quiz' ? 'bg-coop-dark text-white' : 'bg-slate-100 text-slate-700'
            }`}
          >
            Take AI Quiz
          </button>
        </div>
      </div>

      {/* Content Area */}
      {activeTab === 'lesson' ? (
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-6">
          <div className="flex items-center justify-between border-b border-slate-100 pb-4">
            <h3 className="text-sm font-bold text-slate-800">Lesson Material & Instructions</h3>
            <button
              onClick={speakText}
              className={`flex items-center space-x-1.5 text-xs px-3 py-1.5 rounded-full border transition-all ${
                speaking ? 'bg-amber-100 text-amber-900 border-amber-300 animate-pulse' : 'bg-emerald-50 text-emerald-800 border-emerald-300 hover:bg-emerald-100'
              }`}
            >
              <Volume2 className="w-4 h-4 text-emerald-700" />
              <span>{speaking ? 'Stop Voice Assistant' : 'Listen Audio Instruction'}</span>
            </button>
          </div>

          <div className="prose prose-sm max-w-none text-slate-700 leading-relaxed font-sans whitespace-pre-line bg-slate-50 p-4 rounded-xl border border-slate-200">
            {lessonBody}
          </div>

          <div className="flex justify-end pt-4">
            <button
              onClick={() => setActiveTab('quiz')}
              className="btn-accent text-xs py-2 px-4 flex items-center space-x-1.5 font-bold"
            >
              <span>Proceed to Assessment Quiz</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      ) : (
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-6">
          <div className="border-b border-slate-100 pb-4">
            <span className="badge badge-active text-[10px]">TRAINER APPROVED QUIZ</span>
            <h3 className="text-base font-bold text-slate-900 mt-1">Quiz: ERP Operation & Data Entry</h3>
          </div>

          {!quizSubmitted ? (
            <form onSubmit={handleQuizSubmit} className="space-y-6">
              
              <div className="space-y-2">
                <p className="text-xs font-bold text-slate-900">Q1: What is the primary objective of this lesson?</p>
                <div className="space-y-1.5 text-xs text-slate-700">
                  <label className="flex items-center space-x-2 p-2 rounded hover:bg-slate-50 border border-slate-200">
                    <input type="radio" name="q1" value="operational steps" onChange={(e) => setQ1Ans(e.target.value)} required />
                    <span>To understand key operational steps in ERP navigation and batch entry</span>
                  </label>
                  <label className="flex items-center space-x-2 p-2 rounded hover:bg-slate-50 border border-slate-200">
                    <input type="radio" name="q1" value="skip" onChange={(e) => setQ1Ans(e.target.value)} />
                    <span>To bypass daily cooperative quality logging</span>
                  </label>
                </div>
              </div>

              <div className="space-y-2">
                <p className="text-xs font-bold text-slate-900">Q2: True or False: Daily digital logging ensures cooperative transparency.</p>
                <div className="space-y-1.5 text-xs text-slate-700">
                  <label className="flex items-center space-x-2 p-2 rounded hover:bg-slate-50 border border-slate-200">
                    <input type="radio" name="q2" value="True" onChange={(e) => setQ2Ans(e.target.value)} required />
                    <span>True</span>
                  </label>
                  <label className="flex items-center space-x-2 p-2 rounded hover:bg-slate-50 border border-slate-200">
                    <input type="radio" name="q2" value="False" onChange={(e) => setQ2Ans(e.target.value)} />
                    <span>False</span>
                  </label>
                </div>
              </div>

              <button type="submit" className="btn-primary text-xs py-2.5 px-6 font-bold">
                Submit Quiz Answers
              </button>
            </form>
          ) : (
            <div className="text-center py-6 space-y-4">
              <div className="w-16 h-16 bg-emerald-100 rounded-full flex items-center justify-center mx-auto text-coop-dark">
                <Award className="w-8 h-8 text-emerald-700" />
              </div>
              <h3 className="text-lg font-bold text-slate-900">Quiz Completed Successfully!</h3>
              <p className="text-2xl font-extrabold text-coop-dark">Score: {score}%</p>
              <p className="text-xs text-emerald-700 font-medium">
                {score! >= 60 ? "✓ Passed! Skill Readiness Score updated and Certificate generated." : "Please review lesson and try again."}
              </p>
              <div className="flex justify-center space-x-3 pt-4">
                <button onClick={() => navigate('/opportunities')} className="btn-accent text-xs py-2 px-4 font-bold">
                  View Matching Job Opportunities
                </button>
                <button onClick={() => navigate('/dashboard')} className="btn-secondary text-xs py-2 px-4">
                  Return to Dashboard
                </button>
              </div>
            </div>
          )}

        </div>
      )}

    </div>
  );
};
