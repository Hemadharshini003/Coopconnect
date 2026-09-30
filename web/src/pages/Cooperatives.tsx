import React, { useEffect, useState } from 'react';
import { apiFetch } from '../services/api';
import { Cooperative } from '../types';
import { Building2, Plus, MapPin, Phone, Mail, CheckCircle, Search } from 'lucide-react';
import { Link } from 'react-router-dom';

export const Cooperatives: React.FC = () => {
  const [cooperatives, setCooperatives] = useState<Cooperative[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const fetchCoops = async () => {
      try {
        const res = await apiFetch('/cooperatives');
        setCooperatives(res.data || []);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchCoops();
  }, []);

  const filtered = cooperatives.filter(c => 
    c.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    c.cooperative_type.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-900 flex items-center space-x-2">
            <Building2 className="w-5 h-5 text-coop-dark" />
            <span>Cooperative Societies Directory</span>
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Registered cooperative societies under Nashik District Administration.
          </p>
        </div>
        <button className="btn-primary text-xs flex items-center space-x-1.5 self-start">
          <Plus className="w-4 h-4" />
          <span>Register New Cooperative</span>
        </button>
      </div>

      {/* Search Bar */}
      <div className="relative max-w-md">
        <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Search by society name or category..."
          className="w-full pl-9 pr-3 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-coop-dark focus:outline-none bg-white"
        />
      </div>

      {/* Cooperatives Cards */}
      {loading ? (
        <div className="p-8 text-center text-xs text-slate-500">Loading cooperatives...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map((coop) => (
            <div key={coop.id} className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm hover:border-coop-dark transition-all flex flex-col justify-between">
              <div>
                <div className="flex items-start justify-between">
                  <span className="badge badge-active text-[10px]">{coop.cooperative_type}</span>
                  <span className="text-[10px] font-mono text-slate-400">{coop.registration_number}</span>
                </div>
                <h3 className="text-sm font-bold text-slate-900 mt-2 hover:text-coop-dark">
                  <Link to={`/cooperatives/${coop.id}`}>{coop.name}</Link>
                </h3>
                <p className="text-xs text-slate-600 mt-1 line-clamp-2">{coop.description || 'Cooperative society promoting local economic capacity.'}</p>
              </div>

              <div className="border-t border-slate-100 pt-3 mt-4 text-xs text-slate-500 space-y-1">
                <p className="flex items-center space-x-1.5">
                  <MapPin className="w-3.5 h-3.5 text-slate-400" />
                  <span>{coop.village || coop.block || 'Nashik'}, {coop.state}</span>
                </p>
                {coop.phone && (
                  <p className="flex items-center space-x-1.5">
                    <Phone className="w-3.5 h-3.5 text-slate-400" />
                    <span>{coop.phone}</span>
                  </p>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

    </div>
  );
};
