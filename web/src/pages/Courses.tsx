import React, { useEffect, useState } from 'react';
import { apiFetch } from '../services/api';
import { Course } from '../types';
import { BookOpen, Clock, Globe, Plus, Sparkles, CheckCircle2 } from 'lucide-react';
import { Link } from 'react-router-dom';

export const Courses: React.FC = () => {
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const res = await apiFetch('/courses');
        setCourses(res.data || []);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchCourses();
  }, []);

  return (
    <div className="space-y-6">
      
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-900 flex items-center space-x-2">
            <BookOpen className="w-5 h-5 text-coop-dark" />
            <span>Cooperative Capacity Building LMS</span>
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Multilingual offline-first interactive training modules and AI quiz assessments.
          </p>
        </div>
        <button className="btn-primary text-xs flex items-center space-x-1.5 self-start">
          <Plus className="w-4 h-4" />
          <span>Create New Course</span>
        </button>
      </div>

      {loading ? (
        <div className="p-8 text-center text-xs text-slate-500">Loading learning modules...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {courses.map((c) => (
            <div key={c.id} className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden flex flex-col justify-between hover:border-coop-dark transition-all">
              <div className="p-5">
                <div className="flex items-center justify-between">
                  <span className="badge badge-active text-[10px]">{c.category}</span>
                  <span className="text-[10px] font-mono text-slate-400 uppercase">{c.difficulty}</span>
                </div>
                <h3 className="text-sm font-bold text-slate-900 mt-3 line-clamp-1">
                  <Link to={`/courses/${c.id}`} className="hover:text-coop-dark">{c.title}</Link>
                </h3>
                <p className="text-xs text-slate-600 mt-2 line-clamp-2">{c.description}</p>
              </div>

              <div className="px-5 py-3 bg-slate-50 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                <div className="flex items-center space-x-3">
                  <span className="flex items-center space-x-1">
                    <Clock className="w-3.5 h-3.5 text-slate-400" />
                    <span>{c.duration_minutes}m</span>
                  </span>
                  <span className="flex items-center space-x-1">
                    <Globe className="w-3.5 h-3.5 text-slate-400" />
                    <span>{c.language.toUpperCase()}</span>
                  </span>
                </div>
                <Link to={`/courses/${c.id}`} className="btn-primary text-xs py-1 px-3">
                  View Lessons
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}

    </div>
  );
};
