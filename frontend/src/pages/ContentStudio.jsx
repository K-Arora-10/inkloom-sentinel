import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  FileText, 
  Upload, 
  Sparkles, 
  ArrowRight, 
  Check, 
  AlertCircle,
  FileCode,
  FileCheck
} from 'lucide-react';
import { createSubmission, uploadAndExtract } from '../api';

export default function ContentStudio() {
  const navigate = useNavigate();

  const [title, setTitle] = useState('');
  const [contentType, setContentType] = useState('ADVERTISEMENT');
  const [targetAudience, setTargetAudience] = useState('Small and Medium Enterprise Merchants');
  const [objective, setObjective] = useState('Promote merchant checkout onboarding');
  const [campaignName, setCampaignName] = useState('NexaPay Q1 Drive');
  const [rawText, setRawText] = useState('');
  
  // File upload state
  const [fileMode, setFileMode] = useState(false);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [extracting, setExtracting] = useState(false);
  const [extractionSummary, setExtractionSummary] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  const loadScenario = (type) => {
    setError('');
    setFileMode(false);
    setExtractionSummary(null);

    if (type === 'A') {
      setTitle("NexaPay Q1 Merchant Promotional Ad");
      setContentType("ADVERTISEMENT");
      setTargetAudience("Small and Medium Merchants in Tier 1 & 2 cities");
      setObjective("Announce merchant transaction fees and drive onboarding registrations");
      setCampaignName("NexaPay Spring Merchant Drive");
      setRawText("NexaPay is India's safest payment platform for everyday payments. Get started today with our amazing ₹299 transaction fee. Guaranteed secure transactions for everyone!");
    } else if (type === 'B') {
      setTitle("NexaPay Enterprise Product Brochure v2");
      setContentType("PRODUCT_DESCRIPTION");
      setTargetAudience("Enterprise Corporate Accounts");
      setObjective("Comprehensive guide to merchant transaction fee schedule and safety");
      setCampaignName("NexaPay Enterprise Solutions 2026");
      setRawText("NexaPay Enterprise Payment Brochure v2\nHistorical notice: Standard transaction fee was previously INR 499 (superseded).\nUnder our revised pricing schedule, the active transaction fee is INR 399.\nNexaPay is India's safest payment platform for high volume checkout.");
    } else if (type === 'C') {
      setTitle("NexaPay Informal Community Announcement");
      setContentType("SOCIAL_MEDIA");
      setTargetAudience("General Retail Consumers");
      setObjective("Viral social media engagement announcement");
      setCampaignName("Festive Payment Drive");
      setRawText("Hey folks!!! Our deal is absolutely insane. NexaPay is 100% secure and guarantees the best payment experience in India.");
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploadedFile(file);
    setExtracting(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await uploadAndExtract(formData);
      setRawText(res.extracted_text);
      setExtractionSummary(`Extracted ${res.character_count} characters from ${res.filename} (${res.format}).`);
      if (!title) {
        setTitle(file.name.replace(/\.[^/.]+$/, ""));
      }
    } catch (err) {
      setError(`Extraction failed: ${err.message}`);
    } finally {
      setExtracting(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!rawText.trim()) {
      setError("Please provide content to audit.");
      return;
    }

    setSubmitting(true);
    setError('');

    try {
      const res = await createSubmission({
        title: title || "Untitled Submission",
        content_type: contentType,
        target_audience: targetAudience,
        objective: objective,
        campaign_name: campaignName,
        raw_text: rawText
      });

      // Navigate to Review Workspace for this submission
      navigate(`/workspace/${res.id}`);
    } catch (err) {
      setError(err.message);
      setSubmitting(false);
    }
  };

  return (
    <div className="p-8 max-w-4xl mx-auto space-y-6">
      {/* Title */}
      <div>
        <div className="flex items-center space-x-2 text-[11px] font-semibold text-[#405746] uppercase tracking-wider">
          <span>Content Studio</span>
          <span>•</span>
          <span>Pre-Publication Intake</span>
        </div>
        <h2 className="text-xl font-semibold text-[#242522] tracking-tight mt-1">
          Submit Content for Brand Verification
        </h2>
        <p className="text-xs text-[#77766F] mt-1">
          Submit draft copy or upload PDF/DOCX files. Sentinel's multi-stage review engine audits against approved facts, glossary, and policies.
        </p>
      </div>

      {/* Pre-Loaded Compliance Templates Selector */}
      <div className="bg-[#FAF9F6] border border-[#E8E6DF] rounded-md p-4 space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold text-[#242522]">
            Pre-Loaded Compliance Verification Templates:
          </span>
          <span className="text-[10px] text-[#77766F]">
            Select standard enterprise communications to audit compliance
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
          <button
            type="button"
            onClick={() => loadScenario('A')}
            className="p-3 text-left bg-white border border-[#E8E6DF] hover:border-[#405746] rounded transition-all cursor-pointer shadow-2xs"
            title="Audit 1: Promotional Ad"
          >
            <div className="text-[11px] font-semibold text-[#405746]">Template 1: Promotional Ad</div>
            <div className="text-[10px] text-[#77766F] mt-1">
              Checks: Superlative "safest", incorrect ₹299 fee, guarantee.
            </div>
          </button>

          <button
            type="button"
            onClick={() => loadScenario('B')}
            className="p-3 text-left bg-white border border-[#E8E6DF] hover:border-[#405746] rounded transition-all cursor-pointer shadow-2xs"
            title="Audit 2: Brochure"
          >
            <div className="text-[11px] font-semibold text-[#405746]">Template 2: Product Brochure</div>
            <div className="text-[10px] text-[#77766F] mt-1">
              Checks: Outdated ₹499 fee vs ₹399 fee conflict.
            </div>
          </button>

          <button
            type="button"
            onClick={() => loadScenario('C')}
            className="p-3 text-left bg-white border border-[#E8E6DF] hover:border-[#405746] rounded transition-all cursor-pointer shadow-2xs"
            title="Audit 3: Customer Notice"
          >
            <div className="text-[11px] font-semibold text-[#405746]">Template 3: Customer Notice</div>
            <div className="text-[10px] text-[#77766F] mt-1">
              Checks: Tone hyperbole ("insane"), prohibited "100% secure".
            </div>
          </button>
        </div>
      </div>

      {error && (
        <div className="p-3 bg-red-50 border border-red-200 rounded text-xs text-red-700 flex items-center space-x-2">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Submission Form */}
      <form onSubmit={handleSubmit} className="bg-white border border-[#E8E6DF] rounded-md p-6 shadow-2xs space-y-5">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-semibold text-[#242522] mb-1">
              Submission Title *
            </label>
            <input
              type="text"
              required
              placeholder="e.g., NexaPay Q1 Merchant Promotional Ad"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full px-3 py-2 text-xs border border-[#E8E6DF] rounded focus:outline-none focus:border-[#405746]"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-[#242522] mb-1">
              Content Type *
            </label>
            <select
              value={contentType}
              onChange={(e) => setContentType(e.target.value)}
              className="w-full px-3 py-2 text-xs border border-[#E8E6DF] rounded focus:outline-none focus:border-[#405746]"
            >
              <option value="SOCIAL_MEDIA">Social Media Post</option>
              <option value="ADVERTISEMENT">Advertisement / Ad Copy</option>
              <option value="MARKETING_COPY">Marketing Copy</option>
              <option value="EMAIL">Customer Email / Newsletter</option>
              <option value="PRODUCT_DESCRIPTION">Product Description / Brochure</option>
              <option value="PRESS_RELEASE">Press Release</option>
              <option value="GENERAL">General Content</option>
            </select>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div>
            <label className="block text-xs font-semibold text-[#242522] mb-1">
              Target Audience
            </label>
            <input
              type="text"
              placeholder="e.g., SME Retail Merchants"
              value={targetAudience}
              onChange={(e) => setTargetAudience(e.target.value)}
              className="w-full px-3 py-2 text-xs border border-[#E8E6DF] rounded focus:outline-none focus:border-[#405746]"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-[#242522] mb-1">
              Communication Objective
            </label>
            <input
              type="text"
              placeholder="e.g., Merchant acquisition"
              value={objective}
              onChange={(e) => setObjective(e.target.value)}
              className="w-full px-3 py-2 text-xs border border-[#E8E6DF] rounded focus:outline-none focus:border-[#405746]"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-[#242522] mb-1">
              Campaign Name (Optional)
            </label>
            <input
              type="text"
              placeholder="e.g., Spring 2026"
              value={campaignName}
              onChange={(e) => setCampaignName(e.target.value)}
              className="w-full px-3 py-2 text-xs border border-[#E8E6DF] rounded focus:outline-none focus:border-[#405746]"
            />
          </div>
        </div>

        {/* Input Mode Switch (Text vs Upload) */}
        <div className="pt-2 border-t border-[#E8E6DF]">
          <div className="flex items-center justify-between mb-2">
            <label className="text-xs font-semibold text-[#242522]">
              Content Body *
            </label>
            <div className="flex items-center space-x-2 text-xs">
              <button
                type="button"
                onClick={() => setFileMode(false)}
                className={`px-2.5 py-1 rounded cursor-pointer transition-colors ${
                  !fileMode ? 'bg-[#405746] text-white' : 'text-[#77766F] hover:bg-[#F8F7F4]'
                }`}
              >
                Text Editor
              </button>
              <button
                type="button"
                onClick={() => setFileMode(true)}
                className={`px-2.5 py-1 rounded cursor-pointer transition-colors ${
                  fileMode ? 'bg-[#405746] text-white' : 'text-[#77766F] hover:bg-[#F8F7F4]'
                }`}
              >
                Upload File (PDF/DOCX)
              </button>
            </div>
          </div>

          {fileMode ? (
            <div className="space-y-3">
              <div className="border-2 border-dashed border-[#E8E6DF] rounded-md p-6 text-center bg-[#FAF9F6] hover:bg-white transition-colors">
                <Upload className="w-8 h-8 text-[#77766F] mx-auto mb-2" />
                <div className="text-xs font-medium text-[#242522]">
                  Select PDF or DOCX file to extract
                </div>
                <div className="text-[11px] text-[#77766F] mt-1">
                  Server-side PyMuPDF and python-docx text extraction
                </div>
                <input
                  type="file"
                  accept=".pdf,.docx,.txt"
                  onChange={handleFileUpload}
                  className="mt-3 text-xs"
                />
              </div>

              {extracting && (
                <div className="text-xs text-[#77766F] font-mono animate-pulse">
                  Extracting document structure and sentences...
                </div>
              )}

              {extractionSummary && (
                <div className="p-3 bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs rounded flex items-center space-x-2">
                  <FileCheck className="w-4 h-4 shrink-0" />
                  <span>{extractionSummary}</span>
                </div>
              )}

              {rawText && (
                <div>
                  <label className="block text-[11px] font-semibold text-[#77766F] mb-1">
                    Extracted Text Preview:
                  </label>
                  <textarea
                    rows={6}
                    value={rawText}
                    onChange={(e) => setRawText(e.target.value)}
                    className="w-full p-3 text-xs font-mono border border-[#E8E6DF] rounded bg-[#FAF9F6] focus:outline-none focus:border-[#405746]"
                  />
                </div>
              )}
            </div>
          ) : (
            <textarea
              rows={8}
              required
              placeholder="Paste or type copy to be audited against NexaPay brand integrity standards..."
              value={rawText}
              onChange={(e) => setRawText(e.target.value)}
              className="w-full p-3.5 text-xs font-mono border border-[#E8E6DF] rounded leading-relaxed focus:outline-none focus:border-[#405746]"
            />
          )}
        </div>

        {/* Action Button */}
        <div className="pt-3 border-t border-[#E8E6DF] flex items-center justify-between">
          <div className="text-[11px] text-[#77766F]">
            Audits against NexaPay Brand Guidelines v1.0, Facts Register & Claim Passports
          </div>

          <button
            type="submit"
            disabled={submitting}
            className="flex items-center space-x-2 px-5 py-2.5 bg-[#405746] hover:bg-[#344739] text-white text-xs font-semibold rounded shadow-xs transition-colors cursor-pointer"
          >
            <span>{submitting ? 'Running Sentinel Review...' : 'Initiate Sentinel Review'}</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </form>
    </div>
  );
}
