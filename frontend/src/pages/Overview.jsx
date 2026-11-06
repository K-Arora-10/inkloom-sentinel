import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  FileText, 
  CheckCircle2, 
  Clock, 
  AlertTriangle, 
  ShieldAlert, 
  ArrowRight,
  ShieldCheck,
  Check,
  ExternalLink,
  BookOpen
} from 'lucide-react';
import { getAnalytics } from '../api';

export default function Overview() {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getAnalytics()
      .then((res) => {
        setData(res);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[400px]">
        <div className="text-xs text-[#77766F] font-mono">Loading governance analytics...</div>
      </div>
    );
  }

  const statCards = [
    {
      label: 'Total Submissions',
      value: data?.total_submissions || 0,
      description: 'Audited content drafts & releases',
      icon: FileText
    },
    {
      label: 'Pending Human Review',
      value: data?.pending_reviews || 0,
      description: 'Requiring reviewer signoff',
      icon: Clock,
      highlight: data?.pending_reviews > 0 ? 'text-amber-700' : ''
    },
    {
      label: 'Cryptographically Approved',
      value: data?.approved_content || 0,
      description: 'Ed25519 sealed & release-ready',
      icon: CheckCircle2,
      highlight: 'text-emerald-700'
    },
    {
      label: 'Publish Tamper Blocked',
      value: data?.blocked_submissions || 0,
      description: 'Rejected due to digest mismatch',
      icon: ShieldAlert,
      highlight: data?.blocked_submissions > 0 ? 'text-red-700' : ''
    }
  ];

  return (
    <div className="p-8 max-w-6xl mx-auto space-y-8">
      {/* Top Banner: Governance Mission */}
      <div className="bg-white border border-[#E8E6DF] rounded-md p-6 shadow-2xs">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2 text-[11px] font-semibold text-[#405746] uppercase tracking-wider">
              <span>Governance Dashboard</span>
              <span>•</span>
              <span>NexaPay Brand Integrity Engine</span>
            </div>
            <h2 className="text-xl font-semibold text-[#242522] tracking-tight mt-1">
              Active Brand Compliance Pipeline
            </h2>
            <p className="text-xs text-[#77766F] mt-1 max-w-2xl leading-relaxed">
              Inkloom Sentinel continuously verifies external communications against approved brand guidelines, financial facts, and claim passports. Cryptographic Ed25519 signatures protect published content from silent tampering.
            </p>
          </div>
          <div className="flex items-center space-x-2 shrink-0">
            <button
              onClick={() => navigate('/brand-vault')}
              className="flex items-center space-x-1.5 px-3 py-2 text-xs font-medium text-[#242522] bg-[#F8F7F4] hover:bg-[#EAE8E1] border border-[#E8E6DF] rounded transition-colors"
            >
              <BookOpen className="w-3.5 h-3.5 text-[#405746]" />
              <span>Brand Vault</span>
            </button>
            <button
              onClick={() => navigate('/new-review')}
              className="flex items-center space-x-1.5 px-3.5 py-2 text-xs font-medium text-white bg-[#405746] hover:bg-[#344739] rounded transition-colors shadow-2xs"
            >
              <span>Audit New Content</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>

      {/* Numerical Metrics Summary */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map((card, idx) => {
          const Icon = card.icon;
          return (
            <div
              key={idx}
              className="bg-white border border-[#E8E6DF] rounded-md p-4 shadow-2xs flex flex-col justify-between"
            >
              <div className="flex items-center justify-between text-[#77766F]">
                <span className="text-xs font-medium">{card.label}</span>
                <Icon className="w-4 h-4" />
              </div>
              <div className="mt-3">
                <div className={`text-2xl font-bold tracking-tight text-[#242522] ${card.highlight}`}>
                  {card.value}
                </div>
                <div className="text-[11px] text-[#77766F] mt-0.5">
                  {card.description}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Core Workflow Stages Banner */}
      <div className="bg-[#FAF9F6] border border-[#E8E6DF] rounded-md p-4">
        <div className="text-[11px] font-semibold text-[#77766F] uppercase tracking-wider mb-2">
          End-to-End Governance Lifecycle
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-6 gap-2 text-center text-xs">
          <div className="bg-white p-2.5 rounded border border-[#E8E6DF]">
            <div className="font-semibold text-[#242522]">1. Submit</div>
            <div className="text-[10px] text-[#77766F] mt-0.5">Text, PDF, DOCX</div>
          </div>
          <div className="bg-white p-2.5 rounded border border-[#E8E6DF]">
            <div className="font-semibold text-[#242522]">2. Verify</div>
            <div className="text-[10px] text-[#77766F] mt-0.5">Rules & Facts</div>
          </div>
          <div className="bg-white p-2.5 rounded border border-[#E8E6DF]">
            <div className="font-semibold text-[#242522]">3. Explain</div>
            <div className="text-[10px] text-[#77766F] mt-0.5">Citations & Why</div>
          </div>
          <div className="bg-white p-2.5 rounded border border-[#E8E6DF]">
            <div className="font-semibold text-[#242522]">4. Fix</div>
            <div className="text-[10px] text-[#77766F] mt-0.5">Minimal corrections</div>
          </div>
          <div className="bg-white p-2.5 rounded border border-[#E8E6DF]">
            <div className="font-semibold text-[#242522]">5. Approve</div>
            <div className="text-[10px] text-[#77766F] mt-0.5">Ed25519 signed seal</div>
          </div>
          <div className="bg-white p-2.5 rounded border border-[#E8E6DF]">
            <div className="font-semibold text-[#242522]">6. Protect</div>
            <div className="text-[10px] text-[#77766F] mt-0.5">Tamper verification</div>
          </div>
        </div>
      </div>

      {/* Recent Audit Trail Table */}
      <div className="bg-white border border-[#E8E6DF] rounded-md overflow-hidden shadow-2xs">
        <div className="px-6 py-4 border-b border-[#E8E6DF] flex items-center justify-between">
          <div>
            <h3 className="text-sm font-semibold text-[#242522]">System Audit Trail</h3>
            <p className="text-[11px] text-[#77766F]">Chronological immutable log of actions and cryptographic events</p>
          </div>
          <button
            onClick={() => navigate('/history')}
            className="text-xs text-[#405746] hover:underline font-medium flex items-center space-x-1"
          >
            <span>View Full History</span>
            <ArrowRight className="w-3 h-3" />
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-[#FAF9F6] border-b border-[#E8E6DF] text-[#77766F]">
              <tr>
                <th className="py-2.5 px-6 font-medium">Timestamp</th>
                <th className="py-2.5 px-6 font-medium">Action</th>
                <th className="py-2.5 px-6 font-medium">Actor</th>
                <th className="py-2.5 px-6 font-medium">Role</th>
                <th className="py-2.5 px-6 font-medium">Details</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#E8E6DF]">
              {data?.recent_activity?.length > 0 ? (
                data.recent_activity.map((log) => (
                  <tr key={log.id} className="hover:bg-[#FAF9F6] transition-colors">
                    <td className="py-3 px-6 text-[#77766F] font-mono text-[11px]">
                      {new Date(log.timestamp).toLocaleString()}
                    </td>
                    <td className="py-3 px-6 font-semibold text-[#242522]">
                      <span className="bg-[#F4F6F4] text-[#405746] px-2 py-0.5 rounded border border-[#E1E7E2] text-[11px]">
                        {log.action}
                      </span>
                    </td>
                    <td className="py-3 px-6 text-[#242522] font-medium">
                      {log.actor_name}
                    </td>
                    <td className="py-3 px-6 text-[#77766F]">
                      {log.actor_role}
                    </td>
                    <td className="py-3 px-6 text-[#77766F] max-w-md truncate">
                      {log.details || '—'}
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="5" className="py-6 text-center text-[#77766F]">
                    No activity recorded yet.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
