const API_BASE = import.meta.env.VITE_API_BASE_URL 
  ? `${import.meta.env.VITE_API_BASE_URL.replace(/\/$/, '')}/api`
  : '/api';

export async function fetchApi(endpoint, options = {}) {
  const currentRole = localStorage.getItem('inkloom_user_role') || 'CREATOR';
  const currentName = currentRole === 'CREATOR' ? 'Krish Arora (Creator)' : 'Sanchita Sharma (Reviewer)';

  const headers = {
    'Content-Type': 'application/json',
    'x-user-role': currentRole,
    'x-user-name': currentName,
    ...(options.headers || {})
  };

  // If body is FormData, delete Content-Type to allow browser boundary calculation
  if (options.body instanceof FormData) {
    delete headers['Content-Type'];
  }

  const res = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers
  });

  if (!res.ok) {
    let errorDetail = 'API Request Failed';
    try {
      const errJson = await res.json();
      errorDetail = errJson.detail || errJson.message || errorDetail;
    } catch {
      errorDetail = `HTTP ${res.status}: ${res.statusText}`;
    }
    throw new Error(errorDetail);
  }

  return res.json();
}

// Health & Demo
export const getHealth = () => fetchApi('/health');
export const getAnalytics = () => fetchApi('/analytics');
export const switchRole = (role) => fetchApi('/demo/switch-role', {
  method: 'POST',
  body: JSON.stringify({ role })
});

// Brand Vault
export const getDocuments = () => fetchApi('/brand-vault/documents');
export const getDocument = (id) => fetchApi(`/brand-vault/documents/${id}`);
export const uploadDocument = (formData) => fetchApi('/brand-vault/documents/upload', {
  method: 'POST',
  body: formData
});
export const getRules = () => fetchApi('/brand-vault/rules');
export const getGlossary = () => fetchApi('/brand-vault/glossary');
export const getFacts = () => fetchApi('/brand-vault/facts');
export const getClaims = () => fetchApi('/brand-vault/claims');
export const getAssets = () => fetchApi('/brand-vault/assets');

// Submissions
export const getSubmissions = () => fetchApi('/submissions');
export const getSubmission = (id) => fetchApi(`/submissions/${id}`);
export const createSubmission = (data) => fetchApi('/submissions', {
  method: 'POST',
  body: JSON.stringify(data)
});
export const uploadAndExtract = (formData) => fetchApi('/submissions/upload-extract', {
  method: 'POST',
  body: formData
});
export const updateSubmissionText = (id, rawText) => fetchApi(`/submissions/${id}/update-text`, {
  method: 'POST',
  body: JSON.stringify({ raw_text: rawText })
});

// Reviews & Fixes
export const getReview = (id) => fetchApi(`/reviews/${id}`);
export const applyFix = (reviewId, fixId, customSentence = null) => fetchApi(`/reviews/${reviewId}/fixes/${fixId}/apply`, {
  method: 'POST',
  body: JSON.stringify({ fix_id: fixId, custom_sentence: customSentence })
});
export const rejectFix = (reviewId, fixId) => fetchApi(`/reviews/${reviewId}/fixes/${fixId}/reject`, {
  method: 'POST'
});
export const rerunReview = (submissionId) => fetchApi(`/reviews/rerun/${submissionId}`, {
  method: 'POST'
});

// Approvals & Workflow
export const submitForReview = (submissionId) => fetchApi(`/approvals/${submissionId}/submit`, {
  method: 'POST'
});
export const approveSubmission = (submissionId, notes) => fetchApi(`/approvals/${submissionId}/approve`, {
  method: 'POST',
  body: JSON.stringify({ notes })
});
export const requestChanges = (submissionId, notes) => fetchApi(`/approvals/${submissionId}/request-changes`, {
  method: 'POST',
  body: JSON.stringify({ notes })
});
export const addComment = (submissionId, commentText) => fetchApi(`/approvals/${submissionId}/comments`, {
  method: 'POST',
  body: JSON.stringify({ comment_text: commentText })
});

// Releases & Cryptography
export const verifyApprovalSeal = (submissionId) => fetchApi(`/releases/${submissionId}/verify`);
export const publishContent = (submissionId, payload = {}) => fetchApi(`/releases/${submissionId}/publish`, {
  method: 'POST',
  body: JSON.stringify(payload)
});
export const runTamperTest = (submissionId) => fetchApi(`/releases/${submissionId}/tamper-test`, {
  method: 'POST'
});
export const getHistory = () => fetchApi('/history');
