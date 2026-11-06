import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  CheckCircle2, 
  Clock, 
  AlertCircle, 
  FileText, 
  MessageSquare, 
  ShieldCheck, 
  Send,
  X,
  ExternalLink,
  UserCheck
} from 'lucide-react';
import { 
  getSubmissions, 
  approveSubmission, 
  requestChanges, 
  addComment,
  switchRole 
} from '../api';

export default function ApprovalHub({ currentRole, onRoleChange }) {
  const navigate = useNavigate();
  const [submissions, setSubmissions] = useState([]);
  const [selectedSub, setSelectedSub] = useState(null);
  const [loading, setLoading] = useState(true);
  const [reviewNotes, setReviewNotes] = useState('');
  const [commentText, setCommentText] = useState('');
  const [actionError, setActionError] = useState('');
  const [actionSuccess, setActionSuccess] = useState('');

  const loadData = async () => {
    setLoading(true);
    try {
      const data = await getSubmissions();
      setSubmissions(data);
      if (data.length > 0 && !selectedSub) {
        setSelectedSub(data[0]);
      } else if (selectedSub) {
        const refreshed = data.find(s => s.id === selectedSub.id);
        if (refreshed) setSelectedSub(refreshed);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleApprove = async () => {
    if (!selectedSub) return;
    setActionError('');
    setActionSuccess('');

    try {
      await approveSubmission(selectedSub.id, reviewNotes || "Approved for release.");
      setActionSuccess("Content approved successfully! Cryptographic Ed25519 seal generated.");
      setReviewNotes('');
      await loadData();
    } catch (err) {
      setActionError(err.message);
    }
  };

  const handleRequestChanges = async () => {
    if (!selectedSub) return;
    if (!reviewNotes.trim()) {
      setActionError("Please provide change request notes explaining what must be modified.");
      return;
    }
    setActionError('');
    setActionSuccess('');

    try {
      await requestChanges(selectedSub.id, reviewNotes);
      setActionSuccess("Change request submitted to Creator.");
      setReviewNotes('');
      await loadData();
    } catch (err) {
      setActionError(err.message);
    }
  };

  const handleAddComment = async (e) => {
    e.preventDefault();
    if (!commentText.trim() || !selectedSub) return;

    try {
      await addComment(selectedSub.id, commentText);
      setCommentText('');
      await loadData();
    } catch (err) {
      alert(`Comment failed: ${err.message}`);
    }
  };

  const latestVersion = selectedSub?.versions?.[selectedSub.versions.length - 1];
  const latestReview = latestVersion?.reviews?.[0];

  return (
    <div className="p-8 max-w-6xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-[11px] font-semibold text-[#405746] uppercase tracking-wider">
            <span>Governance Gate</span>
            <span>•</span>
            <span>Human Approval Hub</span>
          </div>
          <h2 className="text-xl font-semibold text-[#242522] tracking-tight mt-1">
            Sign-Off & Cryptographic Release
          </h2>
          <p className="text-xs text-[#77766F] mt-1">
            Authorized reviewers evaluate findings, request changes, or generate verifiable Ed25519 digital signatures.
          </p>
        </div>

        {/* Active Role Indicator */}
        <div className="flex items-center space-x-2 text-xs bg-white border border-[#E8E6DF] p-2 rounded shadow-2xs">
          <span className="text-[#77766F]">Active Role:</span>
          <span className={`font-semibold px-2 py-0.5 rounded text-[11px] ${
            currentRole === 'REVIEWER' 
              ? 'bg-emerald-50 text-emerald-800 border border-emerald-200' 
              : 'bg-blue-50 text-blue-800 border border-blue-200'
          }`}>
            {currentRole === 'REVIEWER' ? 'Sanchita Sharma (Reviewer)' : 'Krish Arora (Creator)'}
          </span>
          {currentRole !== 'REVIEWER' && (
            <button
              onClick={async () => {
                await switchRole('REVIEWER');
                localStorage.setItem('inkloom_user_role', 'REVIEWER');
                onRoleChange('REVIEWER');
              }}
              className="text-[11px] text-[#405746] font-medium underline ml-1 cursor-pointer"
            >
              Switch to Reviewer to Approve
            </button>
          )}
        </div>
      </div>

      {/* Main Split Layout: Submissions Queue + Approval Inspector */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Submissions List Queue (1 column) */}
        <div className="bg-white border border-[#E8E6DF] rounded-md overflow-hidden shadow-2xs flex flex-col h-[650px]">
          <div className="p-3.5 bg-[#FAF9F6] border-b border-[#E8E6DF] text-xs font-semibold text-[#242522]">
            Submissions Queue ({submissions.length})
          </div>

          <div className="flex-1 overflow-y-auto divide-y divide-[#E8E6DF]">
            {submissions.map((sub) => {
              const isSelected = selectedSub?.id === sub.id;
              const vCount = sub.versions?.length || 1;
              return (
                <div
                  key={sub.id}
                  onClick={() => {
                    setSelectedSub(sub);
                    setActionError('');
                    setActionSuccess('');
                  }}
                  className={`p-4 cursor-pointer transition-colors ${
                    isSelected ? 'bg-[#FAF9F6] border-l-3 border-[#405746]' : 'hover:bg-[#FAF9F6]'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-mono text-[#77766F] uppercase">
                      {sub.content_type} • v{vCount}
                    </span>
                    <span
                      className={`text-[10px] font-semibold px-2 py-0.5 rounded border ${
                        sub.current_status === 'APPROVED'
                          ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                          : sub.current_status === 'CHANGES_REQUESTED'
                          ? 'bg-amber-50 text-amber-700 border-amber-200'
                          : 'bg-blue-50 text-blue-700 border-blue-200'
                      }`}
                    >
                      {sub.current_status}
                    </span>
                  </div>

                  <h4 className="text-xs font-semibold text-[#242522] mt-1.5 truncate">
                    {sub.title}
                  </h4>

                  <div className="flex items-center justify-between text-[11px] text-[#77766F] mt-2">
                    <span>Target: {sub.target_audience || 'General'}</span>
                    <span>{new Date(sub.updated_at).toLocaleDateString()}</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Selected Submission Inspector & Reviewer Actions (2 columns) */}
        <div className="lg:col-span-2 bg-white border border-[#E8E6DF] rounded-md shadow-2xs flex flex-col h-[650px] overflow-hidden">
          {selectedSub ? (
            <div className="flex flex-col h-full overflow-hidden">
              {/* Header */}
              <div className="p-4 border-b border-[#E8E6DF] bg-[#FAF9F6] flex items-center justify-between shrink-0">
                <div>
                  <div className="text-[10px] font-mono text-[#77766F] uppercase">
                    Version {latestVersion?.version_number} • SHA-256: {latestVersion?.content_hash?.slice(0, 16)}...
                  </div>
                  <h3 className="text-sm font-semibold text-[#242522]">
                    {selectedSub.title}
                  </h3>
                </div>

                <button
                  onClick={() => navigate(`/workspace/${selectedSub.id}`)}
                  className="text-xs text-[#405746] hover:underline font-medium flex items-center space-x-1"
                >
                  <span>Open in Workspace</span>
                  <ExternalLink className="w-3 h-3" />
                </button>
              </div>

              {/* Scrollable Detail Body */}
              <div className="flex-1 overflow-y-auto p-6 space-y-5">
                {actionError && (
                  <div className="p-3 bg-red-50 border border-red-200 rounded text-xs text-red-700 flex items-center space-x-2">
                    <AlertCircle className="w-4 h-4 shrink-0" />
                    <span>{actionError}</span>
                  </div>
                )}

                {actionSuccess && (
                  <div className="p-3 bg-emerald-50 border border-emerald-200 rounded text-xs text-emerald-800 flex items-center space-x-2">
                    <CheckCircle2 className="w-4 h-4 shrink-0" />
                    <span>{actionSuccess}</span>
                  </div>
                )}

                {/* Content Box */}
                <div>
                  <div className="text-xs font-semibold text-[#242522] mb-1">
                    Canonical Text Body (for Release):
                  </div>
                  <div className="p-3.5 bg-[#FAF9F6] border border-[#E8E6DF] rounded font-mono text-xs text-[#242522] whitespace-pre-wrap leading-relaxed">
                    {latestVersion?.raw_text}
                  </div>
                </div>

                {/* Audit Findings Summary */}
                <div className="p-3 bg-[#FAF9F6] border border-[#E8E6DF] rounded text-xs flex items-center justify-between">
                  <div>
                    <span className="font-semibold text-[#242522]">Audit Engine Status: </span>
                    <span className="text-[#77766F]">{latestReview?.summary || 'No review records'}</span>
                  </div>
                  <div className="flex items-center space-x-1.5 font-semibold text-[11px]">
                    <span className="text-red-700">{latestReview?.critical_count || 0} Critical</span>
                    <span>•</span>
                    <span className="text-amber-700">{latestReview?.warning_count || 0} Warnings</span>
                  </div>
                </div>

                {/* Reviewer Action Controls */}
                <div className="border border-[#E8E6DF] rounded-md p-4 bg-white space-y-3">
                  <div className="text-xs font-semibold text-[#242522]">
                    Reviewer Sign-off & Cryptographic Action
                  </div>

                  <textarea
                    rows={2}
                    placeholder="Enter review decision notes (required for requesting changes)..."
                    value={reviewNotes}
                    onChange={(e) => setReviewNotes(e.target.value)}
                    className="w-full p-2.5 text-xs border border-[#E8E6DF] rounded focus:outline-none focus:border-[#405746]"
                  />

                  <div className="flex items-center justify-between pt-1">
                    <div className="text-[11px] text-[#77766F]">
                      Approving generates a persistent Ed25519 digital signature.
                    </div>

                    <div className="flex items-center space-x-2">
                      <button
                        onClick={handleRequestChanges}
                        className="px-3 py-1.5 text-xs font-medium text-amber-800 bg-amber-50 hover:bg-amber-100 border border-amber-200 rounded transition-colors cursor-pointer"
                      >
                        Request Changes
                      </button>

                      <button
                        onClick={handleApprove}
                        className="px-4 py-1.5 text-xs font-semibold text-white bg-[#405746] hover:bg-[#344739] rounded shadow-xs transition-colors flex items-center space-x-1.5 cursor-pointer"
                      >
                        <ShieldCheck className="w-4 h-4" />
                        <span>Approve & Sign Release</span>
                      </button>
                    </div>
                  </div>
                </div>

                {/* Approval Seal Details if already Approved */}
                {selectedSub.current_status === 'APPROVED' && (
                  <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-md text-xs text-emerald-900 space-y-2">
                    <div className="font-semibold flex items-center space-x-1.5 text-emerald-800">
                      <CheckCircle2 className="w-4 h-4" />
                      <span>Release Cryptographically Sealed</span>
                    </div>
                    <div className="text-[11px]">
                      This content is signed with NexaPay's server-side Ed25519 private key. Any post-approval tampering will block release.
                    </div>
                    <button
                      onClick={() => navigate(`/release/${selectedSub.id}`)}
                      className="px-3 py-1.5 bg-emerald-700 hover:bg-emerald-800 text-white rounded text-xs font-medium"
                    >
                      Verify Seal & Publish Content →
                    </button>
                  </div>
                )}

                {/* Comments Thread */}
                <div className="border-t border-[#E8E6DF] pt-4 space-y-3">
                  <div className="text-xs font-semibold text-[#242522]">
                    Governance Thread ({selectedSub.comments?.length || 0})
                  </div>

                  <div className="space-y-2 max-h-40 overflow-y-auto">
                    {selectedSub.comments?.map((c) => (
                      <div key={c.id} className="p-2.5 bg-[#FAF9F6] border border-[#E8E6DF] rounded text-xs">
                        <div className="flex items-center justify-between text-[11px] text-[#77766F]">
                          <span className="font-semibold text-[#242522]">{c.author_name} ({c.author_role})</span>
                          <span>{new Date(c.created_at).toLocaleTimeString()}</span>
                        </div>
                        <div className="mt-1 text-[#242522]">{c.comment_text}</div>
                      </div>
                    ))}
                  </div>

                  <form onSubmit={handleAddComment} className="flex items-center space-x-2">
                    <input
                      type="text"
                      placeholder="Add an internal governance comment..."
                      value={commentText}
                      onChange={(e) => setCommentText(e.target.value)}
                      className="flex-1 px-3 py-1.5 text-xs border border-[#E8E6DF] rounded focus:outline-none focus:border-[#405746]"
                    />
                    <button
                      type="submit"
                      className="px-3 py-1.5 bg-[#FAF9F6] hover:bg-[#EAE8E1] text-[#242522] border border-[#E8E6DF] rounded text-xs font-medium"
                    >
                      Send
                    </button>
                  </form>
                </div>
              </div>
            </div>
          ) : (
            <div className="p-8 text-center text-xs text-[#77766F] my-auto">
              Select a submission from the queue to inspect.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
