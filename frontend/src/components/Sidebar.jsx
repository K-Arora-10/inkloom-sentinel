import React, { useState, useEffect } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { 
  ShieldCheck, 
  BookOpen, 
  FileEdit, 
  History, 
  CheckCircle2, 
  LayoutDashboard, 
  Send,
  Milestone,
  UserCheck,
  RefreshCw
} from 'lucide-react';
import { switchRole } from '../api';

export default function Sidebar({ currentRole, onRoleChange }) {
  const navigate = useNavigate();

  const handleRoleToggle = async () => {
    const nextRole = currentRole === 'CREATOR' ? 'REVIEWER' : 'CREATOR';
    try {
      await switchRole(nextRole);
      localStorage.setItem('inkloom_user_role', nextRole);
      onRoleChange(nextRole);
    } catch (e) {
      console.error(e);
    }
  };

  const navItems = [
    { name: 'Overview', path: '/', icon: LayoutDashboard },
    { name: 'Brand Vault', path: '/brand-vault', icon: BookOpen },
    { name: 'Content Studio', path: '/new-review', icon: FileEdit },
    { name: 'Approval Hub', path: '/approvals', icon: CheckCircle2 },
    { name: 'Review History', path: '/history', icon: History },
    { name: 'Product Roadmap', path: '/roadmap', icon: Milestone }
  ];

  return (
    <aside className="w-64 bg-white border-r border-[#E8E6DF] flex flex-col justify-between shrink-0 h-screen sticky top-0 select-none">
      {/* Brand Header */}
      <div>
        <div className="p-5 border-b border-[#E8E6DF]">
          <div className="flex items-center space-x-2.5">
            <div className="w-8 h-8 rounded bg-[#405746] flex items-center justify-center text-white font-serif font-bold text-lg">
              S
            </div>
            <div>
              <h1 className="text-base font-semibold text-[#242522] tracking-tight leading-none">
                Inkloom Sentinel
              </h1>
              <p className="text-[11px] text-[#77766F] font-mono mt-1">
                v1.0.0 • Enterprise Edition
              </p>
            </div>
          </div>
          <div className="mt-3 text-[11px] text-[#405746] font-medium tracking-wide bg-[#F4F6F4] px-2.5 py-1 rounded border border-[#E1E7E2]">
            Version. Test. Approve. Protect.
          </div>
        </div>

        {/* Navigation Links */}
        <nav className="p-3 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `flex items-center space-x-3 px-3 py-2.5 text-xs font-medium rounded transition-colors ${
                    isActive
                      ? 'bg-[#405746] text-white shadow-xs'
                      : 'text-[#242522] hover:bg-[#F8F7F4] hover:text-[#405746]'
                  }`
                }
              >
                <Icon className="w-4 h-4 shrink-0" />
                <span>{item.name}</span>
              </NavLink>
            );
          })}
        </nav>
      </div>

      {/* Identity & User Role Switcher */}
      <div className="p-4 border-t border-[#E8E6DF] bg-[#FAF9F6]">
        {/* Organization Label */}
        <div className="mb-3">
          <div className="flex items-center justify-between text-[11px] text-[#77766F] uppercase tracking-wider font-semibold">
            <span>Organization</span>
            <span className="text-[10px] text-emerald-700 bg-emerald-50 px-1.5 py-0.5 rounded border border-emerald-200">Verified</span>
          </div>
          <div className="text-xs font-semibold text-[#242522] mt-0.5 flex items-center space-x-1.5">
            <span className="w-2 h-2 rounded-full bg-[#405746]"></span>
            <span>NexaPay Technologies</span>
          </div>
        </div>

        {/* Active Role Card */}
        <div className="bg-white border border-[#E8E6DF] rounded p-2.5 shadow-2xs">
          <div className="flex items-center justify-between">
            <span className="text-[10px] font-semibold text-[#77766F] uppercase tracking-wider">
              Active Profile
            </span>
            <span
              className={`text-[10px] font-medium px-1.5 py-0.2 rounded border ${
                currentRole === 'CREATOR'
                  ? 'bg-blue-50 text-blue-700 border-blue-200'
                  : 'bg-emerald-50 text-emerald-700 border-emerald-200'
              }`}
            >
              {currentRole}
            </span>
          </div>

          <div className="text-xs font-medium text-[#242522] mt-1">
            {currentRole === 'CREATOR' ? 'Krish Arora' : 'Sanchita Sharma'}
          </div>
          <div className="text-[11px] text-[#77766F] truncate">
            {currentRole === 'CREATOR' ? 'Creator (Submissions & Edits)' : 'Reviewer (Sign-off & Sealing)'}
          </div>

          <button
            onClick={handleRoleToggle}
            className="w-full mt-2.5 flex items-center justify-center space-x-1.5 bg-[#F8F7F4] hover:bg-[#EAE8E1] text-[#242522] text-[11px] font-medium py-1.5 px-2 rounded border border-[#E8E6DF] transition-colors cursor-pointer"
          >
            <RefreshCw className="w-3 h-3 text-[#77766F]" />
            <span>Switch to {currentRole === 'CREATOR' ? 'Reviewer' : 'Creator'}</span>
          </button>
        </div>

        <div className="mt-2.5 text-[10px] text-[#77766F] text-center font-mono">
          Enterprise Security Authority • Active Session
        </div>
      </div>
    </aside>
  );
}
