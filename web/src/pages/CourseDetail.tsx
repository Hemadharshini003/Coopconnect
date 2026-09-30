import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { apiFetch } from '../services/api';
import { Course } from '../types';
import { BookOpen, Play, Sparkles, CheckCircle, Clock, ShieldCheck } from 'lucide-react';

export const CourseDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const courseId = id || 'course-c01';
  
  const [course, setCourse] = useState<Course | null>(null);
  const [loading, setLoading] = useState(true);
  const [generatingQuiz, setGeneratingQuiz] = useState(false);
  const [quizStatus, setQuizStatus] = useState<string | null>(null);

  const navigate = useNavigate();

  useEffect(() => {
    const fetchCourse = async () => {
      try {
        const res = await apiFetch(`/courses/${courseId}`);
        setCourse(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchCourse();
  }, [courseId]);

  const handleGenerateAIQuiz = async () => {
    setGeneratingQuiz(true);
    try {
      const lessonId = course?.lessons?.[0]?.id || 'lesson-l01';
      const res = await apiFetch('/quizzes/generate', {
        method: 'POST',
        body: JSON.stringify({ course_id: courseId, lesson_id: lessonId })
      });
      setQuizStatus("AI Quiz Generated! Sent to Trainer for Approval.");
    } catch (err) {
      console.error(err);
    } finally {
      setGeneratingQuiz(false);
    }
  };

  if (loading || !course) {
    return <div className="p-8 text-center text-xs text-slate-500">Loading course syllabus...</div>;
  }

  return (
    <div className="space-y-6">
      
      {/* Course Banner */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
        <div className="flex items-center space-x-2">
          <span className="badge badge-active text-[10px]">{course.category}</span>
          <span className="text-xs font-mono text-slate-400">Duration: {course.duration_minutes} Mins</span>
        </div>
        <h1 className="text-2xl font-bold text-slate-900">{course.title}</h1>
        <p className="text-xs text-slate-600 max-w-2xl leading-relaxed">{course.description}</p>
        
        <div className="flex flex-wrap items-center gap-3 pt-2">
          <button
            onClick={() => navigate(`/learning?course=${courseId}`)}
            className="btn-primary text-xs flex items-center space-x-2 font-bold px-4 py-2"
          >
            <Play className="w-4 h-4" />
            <span>Start Interactive Lesson Player</span>
          </button>

          <button
            onClick={handleGenerateAIQuiz}
            disabled={generatingQuiz}
            className="btn-accent text-xs flex items-center space-x-2 font-bold px-4 py-2 shadow-sm"
          >
            <Sparkles className="w-4 h-4" />
            <span>{generatingQuiz ? 'Synthesizing Questions...' : 'Generate AI Assessment Quiz'}</span>
          </button>
        </div>

        {quizStatus && (
          <div className="bg-emerald-50 border border-emerald-200 text-emerald-800 p-3 rounded-lg text-xs flex items-center space-x-2">
            <ShieldCheck className="w-4 h-4 text-emerald-600 flex-shrink-0" />
            <span>{quizStatus}</span>
          </div>
        )}
      </div>

      {/* Syllabus / Lessons List */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="px-5 py-4 border-b border-slate-100 font-bold text-slate-800 text-sm">
          Course Lessons Syllabus ({course.lessons?.length || 1} Modules)
        </div>

        <div className="divide-y divide-slate-100">
          {(course.lessons || [
            { id: 'lesson-l01', title: 'Module 1: Cooperative ERP Navigation & Daily Batch Entry', duration_minutes: 20, content_type: 'Text & Diagram' }
          ]).map((l: any, idx: number) => (
            <div key={l.id} className="p-4 hover:bg-slate-50 flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 rounded-full bg-emerald-100 text-coop-dark font-bold text-xs flex items-center justify-center">
                  {idx + 1}
                </div>
                <div>
                  <h4 className="text-xs font-bold text-slate-900">{l.title}</h4>
                  <p className="text-[10px] text-slate-500">{l.content_type} • {l.duration_minutes} Mins</p>
                </div>
              </div>
              <Link to={`/learning?course=${courseId}&lesson=${l.id}`} className="btn-secondary text-xs py-1 px-3">
                Launch
              </Link>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
};
