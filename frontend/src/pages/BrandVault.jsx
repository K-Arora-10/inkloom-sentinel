import React, { useState, useEffect } from 'react';
import { 
  BookOpen, 
  FileText, 
  Search, 
  Upload, 
  CheckCircle, 
  AlertCircle, 
  History, 
  Palette, 
  ShieldCheck, 
  FileCheck2,
  X,
  ExternalLink,
  ChevronRight
} from 'lucide-react';
import { 
  getDocuments, 
  getDocument, 
  getRules, 
  getGlossary, 
  getFacts, 
  getClaims, 
  getAssets,
  uploadDocument 
} from '../api';

export default function BrandVault() {
  const [activeTab, setActiveTab] = useState('documents');
  const [documents, setDocuments] = useState([]);
  const [rules, setRules] = useState([]);
  const [glossary, setGlossary] = useState([]);
  const [facts, setFacts] = useState([]);
  const [claims, setClaims] = useState([]);
  const [assets, setAssets] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedDoc, setSelectedDoc] = useState(null);
  const [loading, setLoading] = useState(true);

  // Upload modal state
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [uploadTitle, setUploadTitle] = useState('');
  const [uploadCategory, setUploadCategory] = useState('BRAND_GOVERNANCE');
  const [uploadFile, setUploadFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  const loadData = async () => {
    setLoading(true);
    try {
      const [docsData, rulesData, glossData, factsData, claimsData, assetsData] = await Promise.all([
        getDocuments(),
        getRules(),
        getGlossary(),
        getFacts(),
        getClaims(),
        getAssets()
      ]);
      setDocuments(docsData);
      setRules(rulesData);
      setGlossary(glossData);
      setFacts(factsData);
      setClaims(claimsData);
      setAssets(assetsData);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleUploadSubmit = async (e) => {
    e.preventDefault();
    if (!uploadFile || !uploadTitle) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('title', uploadTitle);
    formData.append('doc_type', 'GUIDELINE');
    formData.append('category', uploadCategory);
    formData.append('file', uploadFile);

    try {
      await uploadDocument(formData);
      setShowUploadModal(false);
      setUploadTitle('');
      setUploadFile(null);
      await loadData();
    } catch (err) {
      alert(`Upload failed: ${err.message}`);
    } finally {
      setUploading(false);
    }
  };

  const filteredDocs = documents.filter(d => 
    d.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    (d.summary && d.summary.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  const filteredGlossary = glossary.filter(g =>
    g.term.toLowerCase().includes(searchQuery.toLowerCase()) ||
    (g.preferred_alternative && g.preferred_alternative.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  const filteredFacts = facts.filter(f =>
    f.fact_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    f.approved_value.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const filteredClaims = claims.filter(c =>
    c.claim_text.toLowerCase().includes(searchQuery.toLowerCase()) ||
    c.claim_code.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="p-8 max-w-6xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2 text-[11px] font-semibold text-[#405746] uppercase tracking-wider">
            <span>Single Source of Truth</span>
            <span>•</span>
            <span>NexaPay Documentation</span>
          </div>
          <h2 className="text-xl font-semibold text-[#242522] tracking-tight mt-1">
            Brand Vault
          </h2>
          <p className="text-xs text-[#77766F] mt-1">
            Verified repository of corporate brand guidelines, approved numbers, terminology dictionary, and claim passports.
          </p>
        </div>

        <button
          onClick={() => setShowUploadModal(true)}
          className="flex items-center space-x-1.5 px-3 py-2 text-xs font-medium text-white bg-[#405746] hover:bg-[#344739] rounded transition-colors shadow-2xs cursor-pointer"
        >
          <Upload className="w-3.5 h-3.5" />
          <span>Upload Guideline (PDF/DOCX)</span>
        </button>
      </div>

      {/* Tabs & Search Filter */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between border-b border-[#E8E6DF] gap-4 pb-2">
        <div className="flex items-center space-x-1">
          {[
            { id: 'documents', label: 'Guidelines & Policies', count: documents.length },
            { id: 'glossary', label: 'Brand Glossary', count: glossary.length },
            { id: 'facts', label: 'Facts Register', count: facts.length },
            { id: 'claims', label: 'Claim Passports', count: claims.length },
            { id: 'rules', label: 'Active Rules', count: rules.length },
            { id: 'visual', label: 'Visual Identity', count: assets.length }
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-3 py-1.5 text-xs font-medium rounded-t transition-colors cursor-pointer flex items-center space-x-1.5 ${
                activeTab === tab.id
                  ? 'border-b-2 border-[#405746] text-[#405746] font-semibold'
                  : 'text-[#77766F] hover:text-[#242522]'
              }`}
            >
              <span>{tab.label}</span>
              <span className="text-[10px] bg-[#FAF9F6] border border-[#E8E6DF] px-1.5 rounded-full text-[#77766F]">
                {tab.count}
              </span>
            </button>
          ))}
        </div>

        <div className="relative w-full sm:w-64">
          <Search className="w-3.5 h-3.5 absolute left-2.5 top-2.5 text-[#77766F]" />
          <input
            type="text"
            placeholder="Search resources..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-8 pr-3 py-1.5 text-xs bg-white border border-[#E8E6DF] rounded focus:outline-none focus:border-[#405746]"
          />
        </div>
      </div>

      {/* TAB 1: Documents (The 7 NexaPay Guidelines) */}
      {activeTab === 'documents' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {filteredDocs.map((doc) => (
            <div
              key={doc.id}
              onClick={() => setSelectedDoc(doc)}
              className="bg-white border border-[#E8E6DF] rounded-md p-4 hover:border-[#405746] transition-all cursor-pointer shadow-2xs flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-mono font-medium px-2 py-0.5 rounded bg-[#FAF9F6] border border-[#E8E6DF] text-[#405746]">
                    {doc.doc_type} • v{doc.current_version}
                  </span>
                  <span className="text-[10px] text-[#77766F]">
                    {new Date(doc.updated_at).toLocaleDateString()}
                  </span>
                </div>
                <h3 className="text-sm font-semibold text-[#242522] mt-2">
                  {doc.title}
                </h3>
                <p className="text-xs text-[#77766F] mt-1 line-clamp-2">
                  {doc.summary || 'No summary available.'}
                </p>
              </div>

              <div className="mt-4 pt-3 border-t border-[#E8E6DF] flex items-center justify-between text-xs text-[#405746] font-medium">
                <span>Inspect Document Content</span>
                <ChevronRight className="w-3.5 h-3.5" />
              </div>
            </div>
          ))}
        </div>
      )}

      {/* TAB 2: Brand Glossary */}
      {activeTab === 'glossary' && (
        <div className="bg-white border border-[#E8E6DF] rounded-md overflow-hidden shadow-2xs">
          <div className="px-6 py-3 bg-[#FAF9F6] border-b border-[#E8E6DF] text-xs font-semibold text-[#242522]">
            NexaPay Controlled Vocabulary & Terminology
          </div>
          <table className="w-full text-left text-xs">
            <thead className="bg-[#FAF9F6] border-b border-[#E8E6DF] text-[#77766F]">
              <tr>
                <th className="py-2.5 px-6 font-medium">Term / Phrase</th>
                <th className="py-2.5 px-6 font-medium">Status</th>
                <th className="py-2.5 px-6 font-medium">Approved / Preferred Alternative</th>
                <th className="py-2.5 px-6 font-medium">Context & Reason</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#E8E6DF]">
              {filteredGlossary.map((item) => (
                <tr key={item.id} className="hover:bg-[#FAF9F6]">
                  <td className="py-3 px-6 font-semibold text-[#242522]">
                    {item.term}
                  </td>
                  <td className="py-3 px-6">
                    <span
                      className={`text-[10px] font-semibold px-2 py-0.5 rounded border ${
                        item.status === 'PROHIBITED'
                          ? 'bg-red-50 text-red-700 border-red-200'
                          : item.status === 'DISCOURAGED'
                          ? 'bg-amber-50 text-amber-700 border-amber-200'
                          : 'bg-emerald-50 text-emerald-700 border-emerald-200'
                      }`}
                    >
                      {item.status}
                    </span>
                  </td>
                  <td className="py-3 px-6 font-medium text-[#242522]">
                    {item.preferred_alternative || '—'}
                  </td>
                  <td className="py-3 px-6 text-[#77766F] max-w-sm">
                    {item.context_note || '—'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* TAB 3: Facts Register */}
      {activeTab === 'facts' && (
        <div className="bg-white border border-[#E8E6DF] rounded-md overflow-hidden shadow-2xs">
          <div className="px-6 py-3 bg-[#FAF9F6] border-b border-[#E8E6DF] text-xs font-semibold text-[#242522]">
            Certified Facts Single Source of Truth
          </div>
          <table className="w-full text-left text-xs">
            <thead className="bg-[#FAF9F6] border-b border-[#E8E6DF] text-[#77766F]">
              <tr>
                <th className="py-2.5 px-6 font-medium">Fact Code</th>
                <th className="py-2.5 px-6 font-medium">Fact Description</th>
                <th className="py-2.5 px-6 font-medium">Approved Value</th>
                <th className="py-2.5 px-6 font-medium">Status</th>
                <th className="py-2.5 px-6 font-medium">Supporting Source</th>
                <th className="py-2.5 px-6 font-medium">Owner</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#E8E6DF]">
              {filteredFacts.map((fact) => (
                <tr key={fact.id} className={fact.is_historical ? 'bg-amber-50/40' : 'hover:bg-[#FAF9F6]'}>
                  <td className="py-3 px-6 font-mono text-[11px] font-semibold text-[#242522]">
                    {fact.fact_code}
                  </td>
                  <td className="py-3 px-6 font-medium text-[#242522]">
                    {fact.fact_name}
                  </td>
                  <td className="py-3 px-6 font-semibold text-[#405746]">
                    {fact.approved_value}
                  </td>
                  <td className="py-3 px-6">
                    <span
                      className={`text-[10px] font-semibold px-2 py-0.5 rounded border ${
                        fact.is_historical
                          ? 'bg-amber-100 text-amber-800 border-amber-300'
                          : 'bg-emerald-50 text-emerald-700 border-emerald-200'
                      }`}
                    >
                      {fact.is_historical ? 'SUPERSEDED (Historical)' : 'ACTIVE (Approved)'}
                    </span>
                  </td>
                  <td className="py-3 px-6 text-[#77766F] text-[11px]">
                    {fact.supporting_source}
                  </td>
                  <td className="py-3 px-6 text-[#77766F]">
                    {fact.owner}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* TAB 4: Claim Passports */}
      {activeTab === 'claims' && (
        <div className="space-y-4">
          <div className="bg-[#FAF9F6] border border-[#E8E6DF] rounded p-3 text-xs text-[#77766F]">
            Claim Passports track public promotional claims, their audit evidence, and verification status. Unsupported claims lack registered evidence but are not automatically false.
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredClaims.map((claim) => (
              <div
                key={claim.id}
                className="bg-white border border-[#E8E6DF] rounded-md p-4 shadow-2xs flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between">
                    <span className="font-mono text-[11px] font-semibold text-[#242522]">
                      {claim.claim_code}
                    </span>
                    <span
                      className={`text-[10px] font-semibold px-2 py-0.5 rounded border ${
                        claim.approval_status === 'APPROVED'
                          ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                          : 'bg-red-50 text-red-700 border-red-200'
                      }`}
                    >
                      {claim.approval_status}
                    </span>
                  </div>
                  <p className="text-xs font-semibold text-[#242522] mt-2 italic">
                    "{claim.claim_text}"
                  </p>
                  <div className="mt-3 text-[11px] text-[#77766F] space-y-1">
                    <div><span className="font-medium text-[#242522]">Evidence:</span> {claim.evidence}</div>
                    <div><span className="font-medium text-[#242522]">Source:</span> {claim.source_document}</div>
                    <div><span className="font-medium text-[#242522]">Owner:</span> {claim.owner}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB 5: Brand Rules */}
      {activeTab === 'rules' && (
        <div className="bg-white border border-[#E8E6DF] rounded-md overflow-hidden shadow-2xs">
          <div className="px-6 py-3 bg-[#FAF9F6] border-b border-[#E8E6DF] text-xs font-semibold text-[#242522]">
            Deterministic Brand Rule Catalog
          </div>
          <table className="w-full text-left text-xs">
            <thead className="bg-[#FAF9F6] border-b border-[#E8E6DF] text-[#77766F]">
              <tr>
                <th className="py-2.5 px-6 font-medium">Rule Code</th>
                <th className="py-2.5 px-6 font-medium">Category</th>
                <th className="py-2.5 px-6 font-medium">Rule Name</th>
                <th className="py-2.5 px-6 font-medium">Severity</th>
                <th className="py-2.5 px-6 font-medium">Rule Pattern / Description</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#E8E6DF]">
              {rules.map((rule) => (
                <tr key={rule.id} className="hover:bg-[#FAF9F6]">
                  <td className="py-3 px-6 font-mono text-[11px] font-semibold text-[#242522]">
                    {rule.rule_code}
                  </td>
                  <td className="py-3 px-6 font-medium text-[#242522]">
                    {rule.category}
                  </td>
                  <td className="py-3 px-6 font-medium text-[#242522]">
                    {rule.name}
                  </td>
                  <td className="py-3 px-6">
                    <span
                      className={`text-[10px] font-semibold px-2 py-0.5 rounded border ${
                        rule.severity === 'CRITICAL'
                          ? 'bg-red-50 text-red-700 border-red-200'
                          : 'bg-amber-50 text-amber-700 border-amber-200'
                      }`}
                    >
                      {rule.severity}
                    </span>
                  </td>
                  <td className="py-3 px-6 text-[#77766F] max-w-sm">
                    {rule.description}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* TAB 6: Visual Identity Guide */}
      {activeTab === 'visual' && (
        <div className="space-y-6">
          <div className="bg-white border border-[#E8E6DF] rounded-md p-6 shadow-2xs space-y-4">
            <h3 className="text-sm font-semibold text-[#242522]">
              Official NexaPay Visual Brand Assets
            </h3>
            <p className="text-xs text-[#77766F]">
              Official SVG brand mark and color palette specifications.
            </p>

            {assets.map((asset) => (
              <div key={asset.id} className="border border-[#E8E6DF] rounded p-4 bg-[#FAF9F6]">
                <div className="text-xs font-semibold text-[#242522] mb-2">{asset.name}</div>
                <div className="bg-white p-6 border border-[#E8E6DF] rounded flex items-center justify-center">
                  <div dangerouslySetInnerHTML={{ __html: asset.svg_content }} />
                </div>
                <div className="mt-2 text-[11px] text-[#77766F]">
                  <span className="font-medium text-[#242522]">Specifications:</span> {asset.specs}
                </div>
              </div>
            ))}

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-4 border-t border-[#E8E6DF]">
              <div className="p-3 bg-[#405746] text-white rounded text-xs">
                <div className="font-semibold">Forest Green</div>
                <div className="text-[10px] opacity-80">#405746 • Primary Brand</div>
              </div>
              <div className="p-3 bg-[#F8F7F4] border border-[#E8E6DF] text-[#242522] rounded text-xs">
                <div className="font-semibold">Warm Off-White</div>
                <div className="text-[10px] text-[#77766F]">#F8F7F4 • Canvas</div>
              </div>
              <div className="p-3 bg-[#242522] text-white rounded text-xs">
                <div className="font-semibold">Near-Black</div>
                <div className="text-[10px] opacity-80">#242522 • Text</div>
              </div>
              <div className="p-3 bg-white border border-[#E8E6DF] text-[#242522] rounded text-xs">
                <div className="font-semibold">Warm Grey</div>
                <div className="text-[10px] text-[#77766F]">#E8E6DF • Border</div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Inspect Document Modal Drawer */}
      {selectedDoc && (
        <div className="fixed inset-0 bg-black/40 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-md shadow-xl border border-[#E8E6DF] max-w-3xl w-full max-h-[85vh] flex flex-col">
            <div className="px-6 py-4 border-b border-[#E8E6DF] flex items-center justify-between">
              <div>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-[#FAF9F6] border border-[#E8E6DF] text-[#405746]">
                  {selectedDoc.doc_type} • v{selectedDoc.current_version}
                </span>
                <h3 className="text-base font-semibold text-[#242522] mt-1">{selectedDoc.title}</h3>
              </div>
              <button
                onClick={() => setSelectedDoc(null)}
                className="p-1 rounded hover:bg-[#F8F7F4] text-[#77766F] cursor-pointer"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-6 overflow-y-auto space-y-4 text-xs text-[#242522] leading-relaxed font-mono whitespace-pre-wrap bg-[#FAF9F6] border-y border-[#E8E6DF]">
              {selectedDoc.versions?.[0]?.content || 'No content found.'}
            </div>

            <div className="px-6 py-3 bg-white flex justify-end">
              <button
                onClick={() => setSelectedDoc(null)}
                className="px-4 py-1.5 text-xs font-medium bg-[#F8F7F4] hover:bg-[#EAE8E1] border border-[#E8E6DF] rounded text-[#242522]"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Upload Document Modal */}
      {showUploadModal && (
        <div className="fixed inset-0 bg-black/40 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-md shadow-xl border border-[#E8E6DF] max-w-md w-full p-6 space-y-4">
            <div className="flex items-center justify-between border-b border-[#E8E6DF] pb-3">
              <h3 className="text-sm font-semibold text-[#242522]">Upload Brand Guideline Document</h3>
              <button onClick={() => setShowUploadModal(false)} className="text-[#77766F] hover:text-[#242522]">
                <X className="w-4 h-4" />
              </button>
            </div>

            <form onSubmit={handleUploadSubmit} className="space-y-4 text-xs">
              <div>
                <label className="block font-medium text-[#242522] mb-1">Document Title</label>
                <input
                  type="text"
                  required
                  placeholder="e.g., NexaPay Advertising Standards 2026"
                  value={uploadTitle}
                  onChange={(e) => setUploadTitle(e.target.value)}
                  className="w-full px-3 py-2 border border-[#E8E6DF] rounded focus:outline-none focus:border-[#405746]"
                />
              </div>

              <div>
                <label className="block font-medium text-[#242522] mb-1">Category</label>
                <select
                  value={uploadCategory}
                  onChange={(e) => setUploadCategory(e.target.value)}
                  className="w-full px-3 py-2 border border-[#E8E6DF] rounded focus:outline-none focus:border-[#405746]"
                >
                  <option value="BRAND_GOVERNANCE">Brand Governance</option>
                  <option value="COMPLIANCE">Compliance & Legal</option>
                  <option value="TERMINOLOGY">Terminology</option>
                  <option value="FACT_ACCURACY">Fact Accuracy</option>
                </select>
              </div>

              <div>
                <label className="block font-medium text-[#242522] mb-1">File (PDF or DOCX)</label>
                <input
                  type="file"
                  required
                  accept=".pdf,.docx,.txt,.md"
                  onChange={(e) => setUploadFile(e.target.files[0])}
                  className="w-full px-2 py-1.5 border border-[#E8E6DF] rounded text-[11px]"
                />
              </div>

              <div className="flex items-center justify-end space-x-2 pt-2 border-t border-[#E8E6DF]">
                <button
                  type="button"
                  onClick={() => setShowUploadModal(false)}
                  className="px-3 py-1.5 border border-[#E8E6DF] rounded text-[#77766F] hover:bg-[#F8F7F4]"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={uploading}
                  className="px-4 py-1.5 bg-[#405746] hover:bg-[#344739] text-white font-medium rounded shadow-xs"
                >
                  {uploading ? 'Processing File...' : 'Upload & Ingest'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
