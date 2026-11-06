import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  ShieldAlert, 
  CheckCircle2, 
  AlertTriangle, 
  Info, 
  Sparkles, 
  Check, 
  X, 
  Edit3, 
  Send, 
  RefreshCw, 
  ArrowRight,
  ExternalLink,
  ChevronDown,
  Hash,
  BookOpen
} from 'lucide-react';
import { 
  getSubmission, 
  applyFix, 
  rejectFix, 
  rerunReview, 
  updateSubmissionText, 
  submitForReview 
} from '../api';

export default function ReviewWorkspace() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [submission, setSubmission] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedFindingId, setSelectedFindingId] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [editedText, setEditedText] = useState('');
  const [processingFixId, setProcessingFixId] = useState(null);
  const [submittingReview, setSubmittingReview] = useState(false);
  const [selectedVersionIndex, setSelectedVersionIndex] = useState(0);

  const loadSubmission = async () => {
    try {
      const data = await getSubmission(id);
      setSubmission(data);
      if (data.versions && data.versions.length > 0) {
        const latestIdx = data.versions.length - 1;
        setSelectedVersionIndex(latestIdx);
        setEditedText(data.versions[latestIdx].raw_text);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSubmission();
  }, [id]);

  if (loading) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[400px]">
        <div className="text-xs text-[#77766F] font-mono">Loading review workspace...</div>
      </div>
    );
  }

  if (!submission || !submission.versions || submission.versions.length === 0) {
    return (
      <div className="p-8 text-center text-xs text-[#77766F]">
        Submission not found.
      </div>
    );
  }

  const currentVersion = submission.versions[selectedVersionIndex] || submission.versions[submission.versions.length - 1];
  const currentReview = currentVersion.reviews?.[0] || null;
  const findings = currentReview?.findings || [];

  const handleApplyFix = async (finding, fix) => {
    setProcessingFixId(fix.id);
    try {
      const updatedSub = await applyFix(currentReview.id, fix.id);
      setSubmission(updatedSub);
      // Select newly created latest version
      const nextIdx = updatedSub.versions.length - 1;
      setSelectedVersionIndex(nextIdx);
      setEditedText(updatedSub.versions[nextIdx].raw_text);
      setSelectedFindingId(null);
    } catch (err) {
      alert(`Failed to apply fix: ${err.message}`);
    } finally {
      setProcessingFixId(null);
    }
  };

  const handleRejectFix = async (finding, fix) => {
    try {
      await rejectFix(currentReview.id, fix.id);
      await loadSubmission();
    } catch (err) {
      alert(`Failed to reject fix: ${err.message}`);
    }
  };

  const handleManualSave = async () => {
    if (!editedText.trim()) return;
    try {
      const updated = await updateSubmissionText(submission.id, editedText);
      setSubmission(updated);
      const nextIdx = updated.versions.length - 1;
      setSelectedVersionIndex(nextIdx);
      setIsEditing(false);
    } catch (err) {
      alert(`Update failed: ${err.message}`);
    }
  };

  const handleRerun = async () => {
    try {
      const updated = await rerunReview(submission.id);
      setSubmission(updated);
    } catch (err) {
      alert(`Rerun failed: ${err.message}`);
    }
  };

  const handleSubmitForApproval = async () => {
    setSubmittingReview(true);
    try {
      await submitForReview(submission.id);
      navigate('/approvals');
    } catch (err) {
      alert(`Submit failed: ${err.message}`);
    } finally {
      setSubmittingReview(false);
    }
  };

  return (
    <div className="h-[calc(100vh-4rem)] flex flex-col bg-[#F8F7F4] overflow-hidden">
      {/* Top Bar */}
      <div className="bg-white border-b border-[#E8E6DF] px-8 py-3.5 flex flex-wrap items-center justify-between gap-4 shrink-0">
        <div>
          <div className="flex items-center space-x-2 text-[10px] font-mono text-[#77766F] uppercase">
            <span>{submission.content_type}</span>
            <span>•</span>
            <span>ID: {submission.id.slice(0, 8)}</span>
          </div>
          <h2 className="text-base font-semibold text-[#242522] tracking-tight">
            {submission.title}
          </h2>
        </div>

        <div className="flex items-center space-x-3">
          {/* Version Switcher */}
          <div className="flex items-center space-x-1.5 text-xs bg-[#FAF9F6] border border-[#E8E6DF] px-2.5 py-1 rounded">
            <span className="text-[#77766F] font-medium">Version:</span>
            <select
              value={selectedVersionIndex}
              onChange={(e) => setSelectedVersionIndex(Number(e.target.value))}
              className="bg-transparent font-semibold text-[#242522] focus:outline-none cursor-pointer"
            >
              {submission.versions.map((ver, idx) => (
                <option key={ver.id} value={idx}>
                  v{ver.version_number} ({new Date(ver.created_at).toLocaleTimeString()})
                </option>
              ))}
            </select>
          </div>

          {/* Finding Counts Pills */}
          <div className="flex items-center space-x-1.5 text-xs">
            <span className="px-2 py-0.5 rounded bg-red-50 text-red-700 border border-red-200 font-semibold text-[11px]">
              {currentReview?.critical_count || 0} Critical
            </span>
            <span className="px-2 py-0.5 rounded bg-amber-50 text-amber-700 border border-amber-200 font-semibold text-[11px]">
              {currentReview?.warning_count || 0} Warnings
            </span>
          </div>

          {/* Status Badge */}
          <span
            className={`text-xs font-semibold px-2.5 py-1 rounded border ${
              submission.current_status === 'APPROVED'
                ? 'bg-emerald-50 text-emerald-800 border-emerald-300'
                : submission.current_status === 'BLOCKED'
                ? 'bg-red-50 text-red-800 border-red-300'
                : submission.current_status === 'CHANGES_REQUESTED'
                ? 'bg-amber-50 text-amber-800 border-amber-300'
                : 'bg-blue-50 text-blue-800 border-blue-300'
            }`}
          >
            {submission.current_status}
          </span>
        </div>
      </div>

      {/* Main Split Body */}
      <div className="flex-1 flex overflow-hidden">
        {/* LEFT PANEL: Submitted Content with Interactive Sentence Highlights */}
        <div className="w-1/2 border-r border-[#E8E6DF] bg-white flex flex-col justify-between overflow-hidden">
          <div className="p-4 border-b border-[#E8E6DF] bg-[#FAF9F6] flex items-center justify-between">
            <div className="text-xs font-semibold text-[#242522] flex items-center space-x-2">
              <span>Submitted Content (v{currentVersion.version_number})</span>
              <span className="text-[10px] text-[#77766F] font-mono">
                SHA-256: {currentVersion.content_hash.slice(0, 12)}...
              </span>
            </div>

            <div className="flex items-center space-x-2">
              {isEditing ? (
                <>
                  <button
                    onClick={() => {
                      setIsEditing(false);
                      setEditedText(currentVersion.raw_text);
                    }}
                    className="text-xs text-[#77766F] px-2 py-1 hover:underline"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={handleManualSave}
                    className="text-xs bg-[#405746] hover:bg-[#344739] text-white px-2.5 py-1 rounded font-medium shadow-xs"
                  >
                    Save & Re-verify
                  </button>
                </>
              ) : (
                <button
                  onClick={() => setIsEditing(true)}
                  className="flex items-center space-x-1 text-xs text-[#405746] hover:underline font-medium"
                >
                  <Edit3 className="w-3.5 h-3.5" />
                  <span>Edit Directly</span>
                </button>
              )}
            </div>
          </div>

          {/* Text Display */}
          <div className="flex-1 p-6 overflow-y-auto">
            {isEditing ? (
              <textarea
                rows={14}
                value={editedText}
                onChange={(e) => setEditedText(e.target.value)}
                className="w-full h-full p-4 text-xs font-mono border border-[#E8E6DF] rounded focus:outline-none focus:border-[#405746] leading-relaxed"
              />
            ) : (
              <div className="text-sm text-[#242522] leading-relaxed whitespace-pre-wrap font-sans">
                {/* Highlight flagged sentences */}
                {findings.length > 0 ? (
                  currentVersion.raw_text.split(/(\n+)/).map((segment, segIdx) => {
                    if (segment.startsWith('\n')) {
                      return <span key={segIdx}>{segment}</span>;
                    }

                    // Check if any finding text exists in this segment
                    const matchingFinding = findings.find(f => segment.includes(f.original_text));
                    if (matchingFinding) {
                      const isSelected = selectedFindingId === matchingFinding.id;
                      const isCrit = matchingFinding.severity === 'CRITICAL';
                      return (
                        <mark
                          key={segIdx}
                          onClick={() => setSelectedFindingId(matchingFinding.id)}
                          className={`cursor-pointer px-1 py-0.5 rounded transition-colors ${
                            isSelected
                              ? 'bg-amber-300 text-black font-medium ring-2 ring-[#405746]'
                              : isCrit
                              ? 'bg-red-100 text-red-900 border-b-2 border-red-500'
                              : 'bg-amber-100 text-amber-900 border-b-2 border-amber-500'
                          }`}
                          title={`Flagged: ${matchingFinding.what_went_wrong}`}
                        >
                          {segment}
                        </mark>
                      );
                    }
                    return <span key={segIdx}>{segment}</span>;
                  })
                ) : (
                  <div>{currentVersion.raw_text}</div>
                )}
              </div>
            )}
          </div>

          {/* Left Footer Action Bar */}
          <div className="p-4 border-t border-[#E8E6DF] bg-[#FAF9F6] flex items-center justify-between text-xs">
            <button
              onClick={handleRerun}
              className="flex items-center space-x-1.5 text-[#77766F] hover:text-[#242522]"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              <span>Re-run Audit Engine</span>
            </button>

            <div className="flex items-center space-x-2">
              {submission.current_status === 'APPROVED' ? (
                <button
                  onClick={() => navigate(`/release/${submission.id}`)}
                  className="flex items-center space-x-1.5 px-4 py-2 bg-[#405746] text-white rounded font-medium shadow-xs"
                >
                  <CheckCircle2 className="w-4 h-4" />
                  <span>View Approval Seal & Publish</span>
                </button>
              ) : (
                <button
                  onClick={handleSubmitForApproval}
                  disabled={submittingReview}
                  className="flex items-center space-x-1.5 px-4 py-2 bg-[#405746] hover:bg-[#344739] text-white rounded font-medium shadow-xs transition-colors cursor-pointer"
                >
                  <Send className="w-3.5 h-3.5" />
                  <span>Submit for Human Approval</span>
                </button>
              )}
            </div>
          </div>
        </div>

        {/* RIGHT PANEL: Findings List & Fix Assistant */}
        <div className="w-1/2 bg-[#F8F7F4] flex flex-col justify-between overflow-hidden">
          <div className="p-4 border-b border-[#E8E6DF] bg-white flex items-center justify-between">
            <div className="text-xs font-semibold text-[#242522]">
              Audit Findings & Recommended Fixes ({findings.length})
            </div>
            <div className="text-[11px] text-[#77766F]">
              Click any finding or highlighted sentence to inspect
            </div>
          </div>

          {/* Findings List */}
          <div className="flex-1 p-6 overflow-y-auto space-y-4">
            {findings.length === 0 ? (
              <div className="p-8 text-center bg-white border border-[#E8E6DF] rounded-md">
                <CheckCircle2 className="w-8 h-8 text-emerald-600 mx-auto mb-2" />
                <h3 className="text-sm font-semibold text-[#242522]">No Brand Violations Detected</h3>
                <p className="text-xs text-[#77766F] mt-1 max-w-sm mx-auto">
                  Content complies with NexaPay brand guidelines, approved pricing, and certified claims. Ready for signoff!
                </p>
              </div>
            ) : (
              findings.map((f) => {
                const isSelected = selectedFindingId === f.id;
                const isCrit = f.severity === 'CRITICAL';
                const fix = f.fixes?.[0];

                return (
                  <div
                    key={f.id}
                    onClick={() => setSelectedFindingId(f.id)}
                    className={`bg-white border rounded-md p-4 transition-all shadow-2xs ${
                      isSelected
                        ? 'border-[#405746] ring-1 ring-[#405746]'
                        : isCrit
                        ? 'border-red-200'
                        : 'border-[#E8E6DF]'
                    }`}
                  >
                    {/* Header */}
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-1.5">
                        <span
                          className={`text-[10px] font-semibold px-2 py-0.5 rounded border ${
                            isCrit
                              ? 'bg-red-50 text-red-700 border-red-200'
                              : 'bg-amber-50 text-amber-700 border-amber-200'
                          }`}
                        >
                          {f.severity}
                        </span>
                        <span className="text-[10px] font-mono text-[#77766F] bg-[#FAF9F6] border border-[#E8E6DF] px-1.5 py-0.5 rounded">
                          {f.classification}
                        </span>
                      </div>
                      <span className="text-[10px] text-[#77766F] font-mono">
                        {f.rule_code || f.category}
                      </span>
                    </div>

                    {/* Problem Statement */}
                    <div className="mt-2 text-xs font-semibold text-[#242522]">
                      {f.what_went_wrong}
                    </div>

                    {/* Flagged Original Text Quote */}
                    <div className="mt-2 text-[11px] font-mono bg-[#FAF9F6] p-2 border-l-2 border-[#77766F] rounded-r text-[#242522]">
                      "{f.original_text}"
                    </div>

                    {/* Why It Matters */}
                    <div className="mt-2 text-xs text-[#77766F] leading-relaxed">
                      <span className="font-medium text-[#242522]">Why it matters:</span> {f.why_it_matters}
                    </div>

                    {/* Evidence Citation */}
                    <div className="mt-2.5 p-2.5 bg-[#FAF9F6] border border-[#E8E6DF] rounded text-[11px] text-[#242522]">
                      <div className="flex items-center space-x-1 font-semibold text-[#405746] mb-1">
                        <BookOpen className="w-3 h-3" />
                        <span>Source: {f.source_document}</span>
                      </div>
                      <div className="text-[#77766F]">{f.supporting_evidence}</div>
                    </div>

                    {/* Fix Assistant Card */}
                    {fix && (
                      <div className="mt-3 p-3 bg-[#F4F6F4] border border-[#DCE4DD] rounded-md">
                        <div className="flex items-center justify-between">
                          <span className="text-[11px] font-semibold text-[#405746] flex items-center space-x-1">
                            <Sparkles className="w-3 h-3" />
                            <span>Fix Assistant (Minimal Correction)</span>
                          </span>
                          <span className="text-[10px] font-mono text-[#77766F]">
                            {fix.status}
                          </span>
                        </div>

                        <div className="mt-1.5 text-xs text-[#242522] font-medium bg-white p-2 rounded border border-[#E8E6DF]">
                          "{fix.suggested_sentence}"
                        </div>

                        {fix.status === 'PENDING' && (
                          <div className="mt-2 flex items-center justify-end space-x-2">
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                handleRejectFix(f, fix);
                              }}
                              className="px-2.5 py-1 text-[11px] text-[#77766F] hover:text-[#242522] border border-[#E8E6DF] rounded bg-white"
                            >
                              Reject
                            </button>
                            <button
                              disabled={processingFixId === fix.id}
                              onClick={(e) => {
                                e.stopPropagation();
                                handleApplyFix(f, fix);
                              }}
                              className="px-3 py-1 text-[11px] font-medium text-white bg-[#405746] hover:bg-[#344739] rounded shadow-2xs flex items-center space-x-1 cursor-pointer"
                            >
                              <Check className="w-3 h-3" />
                              <span>{processingFixId === fix.id ? 'Applying & Re-verifying...' : 'Accept Fix (Bump v' + (currentVersion.version_number + 1) + ')'}</span>
                            </button>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                );
              })
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
