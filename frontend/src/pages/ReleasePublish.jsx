import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  ShieldCheck, 
  ShieldAlert, 
  CheckCircle2, 
  AlertCircle, 
  Lock, 
  Send, 
  Key, 
  FileText, 
  ArrowLeft,
  RefreshCw,
  ExternalLink
} from 'lucide-react';
import { 
  getSubmission, 
  verifyApprovalSeal, 
  publishContent, 
  runTamperTest 
} from '../api';

export default function ReleasePublish() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [submission, setSubmission] = useState(null);
  const [sealData, setSealData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [publishResult, setPublishResult] = useState(null);
  const [tamperResult, setTamperResult] = useState(null);
  const [publishing, setPublishing] = useState(false);
  const [tampering, setTampering] = useState(false);

  const loadData = async () => {
    setLoading(true);
    try {
      const [subData, verifyData] = await Promise.all([
        getSubmission(id),
        verifyApprovalSeal(id)
      ]);
      setSubmission(subData);
      setSealData(verifyData);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [id]);

  const handlePublish = async () => {
    setPublishing(true);
    setPublishResult(null);
    try {
      const res = await publishContent(id, { tamper_with_char: false });
      setPublishResult(res);
      await loadData();
    } catch (err) {
      setPublishResult({
        status: 'BLOCKED',
        message: err.message
      });
    } finally {
      setPublishing(false);
    }
  };

  const handleTamperDemonstration = async () => {
    setTampering(true);
    setTamperResult(null);
    try {
      const res = await runTamperTest(id);
      setTamperResult(res);
      await loadData();
    } catch (err) {
      setTamperResult({
        status: 'ERROR',
        message: err.message
      });
    } finally {
      setTampering(false);
    }
  };

  if (loading) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[400px]">
        <div className="text-xs text-[#77766F] font-mono">Verifying cryptographic seal...</div>
      </div>
    );
  }

  const latestVersion = submission?.versions?.[submission.versions.length - 1];

  return (
    <div className="p-8 max-w-5xl mx-auto space-y-6">
      {/* Navigation & Header */}
      <div className="flex items-center space-x-3 text-xs">
        <button
          onClick={() => navigate(`/workspace/${id}`)}
          className="flex items-center space-x-1 text-[#405746] hover:underline"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back to Workspace</span>
        </button>
        <span className="text-[#E8E6DF]">/</span>
        <span className="text-[#77766F]">Cryptographic Release Gateway</span>
      </div>

      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-[11px] font-semibold text-[#405746] uppercase tracking-wider">
            <span>Cryptographic Trust</span>
            <span>•</span>
            <span>Ed25519 & SHA-256 Publishing Seal</span>
          </div>
          <h2 className="text-xl font-semibold text-[#242522] tracking-tight mt-1">
            Publish Verification & Tamper Protection
          </h2>
          <p className="text-xs text-[#77766F] mt-1">
            NexaPay Distribution & Release Gateway verifying cryptographic digital signatures prior to public release.
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <span
            className={`text-xs font-semibold px-3 py-1 rounded border ${
              submission.current_status === 'PUBLISHED'
                ? 'bg-emerald-50 text-emerald-800 border-emerald-300'
                : submission.current_status === 'APPROVED'
                ? 'bg-blue-50 text-blue-800 border-blue-300'
                : 'bg-red-50 text-red-800 border-red-300'
            }`}
          >
            Status: {submission.current_status}
          </span>
        </div>
      </div>

      {/* Cryptographic Certificate Card */}
      <div className="bg-white border border-[#E8E6DF] rounded-md overflow-hidden shadow-2xs">
        <div className="p-4 bg-[#FAF9F6] border-b border-[#E8E6DF] flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Lock className="w-4 h-4 text-[#405746]" />
            <span className="text-xs font-semibold text-[#242522]">
              Digital Signature Certificate
            </span>
          </div>
          <span className="text-[10px] font-mono text-[#77766F]">
            Issuer: Inkloom Sentinel • NexaPay Authority
          </span>
        </div>

        <div className="p-6 space-y-4 text-xs">
          {sealData?.has_approval_seal ? (
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-3 bg-[#FAF9F6] border border-[#E8E6DF] rounded">
                  <div className="text-[11px] font-semibold text-[#77766F] uppercase">
                    Canonical SHA-256 Content Digest
                  </div>
                  <div className="font-mono text-[11px] text-[#242522] mt-1 break-all bg-white p-2 border border-[#E8E6DF] rounded">
                    {sealData.content_sha256}
                  </div>
                  <div className="text-[10px] text-emerald-700 mt-1 flex items-center space-x-1">
                    <CheckCircle2 className="w-3 h-3" />
                    <span>Canonical hash matches current text version</span>
                  </div>
                </div>

                <div className="p-3 bg-[#FAF9F6] border border-[#E8E6DF] rounded">
                  <div className="text-[11px] font-semibold text-[#77766F] uppercase">
                    Ed25519 Public Key Reference
                  </div>
                  <div className="font-mono text-[11px] text-[#242522] mt-1 break-all bg-white p-2 border border-[#E8E6DF] rounded">
                    {sealData.public_key_b64}
                  </div>
                  <div className="text-[10px] text-[#77766F] mt-1">
                    Persistent server-side keypair
                  </div>
                </div>
              </div>

              <div className="p-3 bg-[#FAF9F6] border border-[#E8E6DF] rounded">
                <div className="text-[11px] font-semibold text-[#77766F] uppercase">
                  Ed25519 Digital Signature (Base64)
                </div>
                <div className="font-mono text-[11px] text-[#242522] mt-1 break-all bg-white p-2 border border-[#E8E6DF] rounded">
                  {sealData.signature_b64}
                </div>
                <div className="text-[10px] text-[#77766F] mt-1">
                  Signed by: {sealData.reviewer_name} at {new Date(sealData.approved_at).toLocaleString()}
                </div>
              </div>

              {/* Action Buttons: Standard Publish vs Tamper Demo */}
              <div className="pt-4 border-t border-[#E8E6DF] flex flex-wrap items-center justify-between gap-3">
                <button
                  onClick={handlePublish}
                  disabled={publishing}
                  className="px-5 py-2.5 bg-[#405746] hover:bg-[#344739] text-white font-semibold text-xs rounded shadow-xs flex items-center space-x-2 transition-colors cursor-pointer"
                >
                  <Send className="w-4 h-4" />
                  <span>{publishing ? 'Verifying & Publishing...' : 'Verify & Publish to Distribution'}</span>
                </button>

                <button
                  onClick={handleTamperDemonstration}
                  disabled={tampering}
                  className="px-4 py-2.5 bg-red-50 hover:bg-red-100 text-red-800 border border-red-300 font-semibold text-xs rounded transition-colors flex items-center space-x-2 cursor-pointer"
                >
                  <ShieldAlert className="w-4 h-4 text-red-600" />
                  <span>Execute Tamper-Resistance Verification</span>
                </button>
              </div>
            </div>
          ) : (
            <div className="p-6 text-center text-[#77766F] space-y-2">
              <AlertCircle className="w-8 h-8 text-amber-600 mx-auto" />
              <div className="font-semibold text-sm text-[#242522]">
                Content is not yet approved
              </div>
              <p className="text-xs max-w-md mx-auto">
                Only approved submissions receive an Ed25519 digital signature seal. Switch to the Reviewer profile in the Approval Hub to sign off.
              </p>
              <button
                onClick={() => navigate('/approvals')}
                className="mt-2 px-3 py-1.5 bg-[#405746] text-white rounded text-xs"
              >
                Go to Approval Hub
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Publishing Result Box */}
      {publishResult && (
        <div className={`p-5 rounded-md border text-xs space-y-2 ${
          publishResult.status === 'APPROVED'
            ? 'bg-emerald-50 border-emerald-200 text-emerald-900'
            : 'bg-red-50 border-red-200 text-red-900'
        }`}>
          <div className="flex items-center space-x-2 font-bold text-sm">
            {publishResult.status === 'APPROVED' ? (
              <>
                <CheckCircle2 className="w-5 h-5 text-emerald-600" />
                <span>Publication Successful — Verified Authentic</span>
              </>
            ) : (
              <>
                <ShieldAlert className="w-5 h-5 text-red-600" />
                <span>Publication Blocked — Verification Failed</span>
              </>
            )}
          </div>
          <p>{publishResult.message}</p>
          <div className="text-[11px] font-mono opacity-80">
            Hash matches: {publishResult.hash_matches ? 'YES' : 'NO'} • Signature valid: {publishResult.signature_valid ? 'YES' : 'NO'}
          </div>
        </div>
      )}

      {/* TAMPER VERIFICATION AUDIT BOX */}
      {tamperResult && (
        <div className="bg-white border-2 border-red-300 rounded-md p-6 shadow-md space-y-4">
          <div className="flex items-center justify-between border-b border-red-200 pb-3">
            <div className="flex items-center space-x-2 text-red-700 font-bold text-sm">
              <ShieldAlert className="w-5 h-5" />
              <span>Tamper-Resistance Audit Results (Cryptographic Rejection)</span>
            </div>
            <span className="text-xs bg-red-100 text-red-800 font-bold px-2 py-0.5 rounded border border-red-300">
              STATUS: BLOCKED
            </span>
          </div>

          <div className="text-xs text-[#242522] leading-relaxed">
            {tamperResult.explanation}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono">
            <div className="p-3 bg-emerald-50 border border-emerald-200 rounded">
              <div className="text-[10px] font-bold text-emerald-800 uppercase">
                Expected Approved SHA-256 Digest
              </div>
              <div className="mt-1 text-[11px] text-emerald-900 break-all">
                {tamperResult.original_sha256}
              </div>
            </div>

            <div className="p-3 bg-red-50 border border-red-200 rounded">
              <div className="text-[10px] font-bold text-red-800 uppercase">
                Tampered Payload SHA-256 Digest
              </div>
              <div className="mt-1 text-[11px] text-red-900 break-all">
                {tamperResult.tampered_sha256}
              </div>
            </div>
          </div>

          <div className="p-3 bg-[#FAF9F6] border border-[#E8E6DF] rounded text-xs text-[#77766F]">
            <span className="font-semibold text-[#242522]">Tamper Modification: </span>
            A single character was appended/modified after Ed25519 signing. The NexaPay distribution gateway detected the hash divergence and rejected release automatically.
          </div>
        </div>
      )}
    </div>
  );
}
