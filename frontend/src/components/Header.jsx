import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ShieldCheck, Plus, CheckCircle, AlertCircle, FileText } from 'lucide-react';
import { getHealth } from '../api';

export default function Header({ title, subtitle, onSelectScenario }) {
  const navigate = useNavigate();
  const [health, setHealth] = useState(null);

  useEffect(() => {
    getHealth()
      .then(setHealth)
      .catch((e) => console.error("Health check error", e));
  }, []);

  return (
    <header className="h-16 bg-white border-b border-[#E8E6DF] px-8 flex items-center justify-between sticky top-0 z-10">
      <div>
        <h2 className="text-sm font-semibold text-[#242522] tracking-tight">{title}</h2>
        {subtitle && <p className="text-[12px] text-[#77766F]">{subtitle}</p>}
      </div>

      <div className="flex items-center space-x-3">
        {/* System Status Pill */}
        <div className="hidden lg:flex items-center space-x-2 text-[11px] font-mono px-2.5 py-1 bg-[#FAF9F6] border border-[#E8E6DF] rounded text-[#405746]">
          <span className="w-2 h-2 rounded-full bg-emerald-600 animate-pulse"></span>
          <span>Ed25519 & Deterministic Engine Ready</span>
        </div>

        {/* Quick Compliance Audit Presets */}
        {onSelectScenario && (
          <div className="flex items-center space-x-1.5">
            <span className="text-[11px] font-medium text-[#77766F] hidden sm:inline">Audit Presets:</span>
            <button
              onClick={() => onSelectScenario('A')}
              className="px-2 py-1 text-[11px] font-medium bg-[#F8F7F4] hover:bg-[#EFECE6] border border-[#E8E6DF] rounded text-[#242522] transition-colors cursor-pointer"
              title="Promotional ad with pricing and superlative checks"
            >
              Ad Copy
            </button>
            <button
              onClick={() => onSelectScenario('B')}
              className="px-2 py-1 text-[11px] font-medium bg-[#F8F7F4] hover:bg-[#EFECE6] border border-[#E8E6DF] rounded text-[#242522] transition-colors cursor-pointer"
              title="Product brochure with superseded fee checks"
            >
              Brochure
            </button>
            <button
              onClick={() => onSelectScenario('C')}
              className="px-2 py-1 text-[11px] font-medium bg-[#F8F7F4] hover:bg-[#EFECE6] border border-[#E8E6DF] rounded text-[#242522] transition-colors cursor-pointer"
              title="Customer communication with tone and warranty checks"
            >
              Customer Notice
            </button>
          </div>
        )}

        <button
          onClick={() => navigate('/new-review')}
          className="flex items-center space-x-1.5 bg-[#405746] hover:bg-[#344739] text-white text-xs font-medium py-1.5 px-3 rounded shadow-xs transition-colors cursor-pointer"
        >
          <Plus className="w-3.5 h-3.5" />
          <span>New Review</span>
        </button>
      </div>
    </header>
  );
}
