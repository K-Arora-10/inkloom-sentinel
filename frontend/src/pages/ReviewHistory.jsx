import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  History, 
  FileText, 
  CheckCircle2, 
  AlertCircle, 
  ArrowRight, 
  ShieldCheck,
  Search
} from 'lucide-react';
import { getHistory } from '../api';

export default function ReviewHistory() {
  const navigate = useNavigate();
  const [history, setHistory] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getHistory()
      .then((data) => {
        setHistory(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  const filtered = history.filter(h =>
    h.title.toLowerCase().includes(search.toLowerCase()) ||
    h.content_type.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="p-8 max-w-6xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-[11px] font-semibold text-[#405746] uppercase tracking-wider">
            <span>Audit Trail</span>
            <span>•</span>
            <span>Submission Registry</span>
          </div>
          <h2 className="text-xl font-semibold text-[#242522] tracking-tight mt-1">
            Review History & Version Archive
          </h2>
          <p className="text-xs text-[#77766F] mt-1">
            Immutable log of all content submissions, revisions, review findings, and cryptographic approval seals.
          </p>
        </div>

        <div className="relative w-64">
          <Search className="w-3.5 h-3.5 absolute left-2.5 top-2.5 text-[#77766F]" />
          <input
            type="text"
            placeholder="Search history..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-8 pr-3 py-1.5 text-xs bg-white border border-[#E8E6DF] rounded focus:outline-none focus:border-[#405746]"
          />
        </div>
      </div>

      {/* Table */}
      <div className="bg-white border border-[#E8E6DF] rounded-md overflow-hidden shadow-2xs">
        <table className="w-full text-left text-xs">
          <thead className="bg-[#FAF9F6] border-b border-[#E8E6DF] text-[#77766F]">
            <tr>
              <th className="py-3 px-6 font-medium">Submission Title</th>
              <th className="py-3 px-6 font-medium">Type</th>
              <th className="py-3 px-6 font-medium">Versions</th>
              <th className="py-3 px-6 font-medium">Findings</th>
              <th className="py-3 px-6 font-medium">Approval Status</th>
              <th className="py-3 px-6 font-medium">Last Updated</th>
              <th className="py-3 px-6 font-medium text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[#E8E6DF]">
            {filtered.length > 0 ? (
              filtered.map((item) => {
                const latestVer = item.versions?.[item.versions.length - 1];
                const latestRev = latestVer?.reviews?.[0];
                const findingsCount = latestRev?.findings_count || 0;

                return (
                  <tr key={item.id} className="hover:bg-[#FAF9F6] transition-colors">
                    <td className="py-3.5 px-6 font-semibold text-[#242522]">
                      {item.title}
                    </td>
                    <td className="py-3.5 px-6 text-[#77766F] font-mono text-[11px]">
                      {item.content_type}
                    </td>
                    <td className="py-3.5 px-6 font-mono text-[#242522]">
                      v{item.versions?.length || 1}
                    </td>
                    <td className="py-3.5 px-6">
                      <span className={`px-2 py-0.5 rounded text-[11px] font-semibold ${
                        findingsCount > 0 ? 'bg-amber-50 text-amber-700 border border-amber-200' : 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                      }`}>
                        {findingsCount} findings
                      </span>
                    </td>
                    <td className="py-3.5 px-6">
                      <span className={`px-2 py-0.5 rounded text-[11px] font-semibold border ${
                        item.current_status === 'APPROVED' || item.current_status === 'PUBLISHED'
                          ? 'bg-emerald-50 text-emerald-800 border-emerald-300'
                          : item.current_status === 'BLOCKED'
                          ? 'bg-red-50 text-red-800 border-red-300'
                          : item.current_status === 'CHANGES_REQUESTED'
                          ? 'bg-amber-50 text-amber-800 border-amber-300'
                          : 'bg-blue-50 text-blue-800 border-blue-300'
                      }`}>
                        {item.current_status}
                      </span>
                    </td>
                    <td className="py-3.5 px-6 text-[#77766F] font-mono text-[11px]">
                      {new Date(item.updated_at).toLocaleDateString()}
                    </td>
                    <td className="py-3.5 px-6 text-right space-x-2">
                      <button
                        onClick={() => navigate(`/workspace/${item.id}`)}
                        className="px-2.5 py-1 text-[11px] font-medium text-[#405746] bg-[#F8F7F4] hover:bg-[#EAE8E1] border border-[#E8E6DF] rounded"
                      >
                        Workspace
                      </button>
                      {item.current_status === 'APPROVED' && (
                        <button
                          onClick={() => navigate(`/release/${item.id}`)}
                          className="px-2.5 py-1 text-[11px] font-medium text-white bg-[#405746] hover:bg-[#344739] rounded"
                        >
                          Seal & Publish
                        </button>
                      )}
                    </td>
                  </tr>
                );
              })
            ) : (
              <tr>
                <td colSpan="7" className="py-8 text-center text-[#77766F]">
                  No historical submissions found.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
