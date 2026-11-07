// Determine backend API Base URL with smart production fallback
const rawBase = import.meta.env.VITE_API_BASE_URL;

function resolveApiBase() {
  if (rawBase && rawBase.trim()) {
    const formatted = rawBase.startsWith('http://') || rawBase.startsWith('https://')
      ? rawBase
      : `https://${rawBase}`;
    return `${formatted.replace(/\/$/, '')}/api`;
  }

  // If in browser and deployed on Render (or any non-localhost host), point directly to the live backend
  if (typeof window !== 'undefined' && window.location && window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
    return 'https://inkloom-sentinel-api-d40s.onrender.com/api';
  }

  return '/api';
}

const API_BASE = resolveApiBase();

export async function fetchApi(endpoint, options = {}) {
  const currentRole = localStorage.getItem('inkloom_user_role') || 'CREATOR';
  const currentName = currentRole === 'CREATOR' ? 'Krish Arora (Creator)' : 'Sanchita Sharma (Reviewer)';

  const headers = {
    'Content-Type': 'application/json',
    'x-user-role': currentRole,
    'x-user-name': currentName,
    ...(options.headers || {})
  };

  if (options.body instanceof FormData) {
    delete headers['Content-Type'];
  }

  let res;
  try {
    res = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers
    });
  } catch (netErr) {
    throw new Error(
      `Unable to reach the server (${netErr.message}). The backend web service on Render may be waking up from cold start. Please wait 15-20 seconds and try again.`
    );
  }

  const rawText = await res.text();
  let data = null;
  if (rawText && rawText.trim()) {
    try {
      data = JSON.parse(rawText);
    } catch {
      data = null;
    }
  }

  // If the server returned HTML instead of JSON (typical when a static CDN rewrites /api to index.html)
  if (rawText && (rawText.includes('<!doctype html>') || rawText.includes('<html'))) {
    throw new Error(
      `Received HTML instead of API response from ${API_BASE}. Please ensure backend API URL is configured correctly.`
    );
  }

  if (!res.ok) {
    const errorDetail =
      (data && (data.detail || data.message)) ||
      (rawText && rawText.length < 200 ? rawText : `Server returned HTTP ${res.status}: ${res.statusText}`);
    throw new Error(errorDetail);
  }

  if (data === null) {
    if (res.status === 204 || (!rawText && res.ok)) {
      return {};
    }
    throw new Error(`Server returned unexpected format (${res.status}): ${rawText.slice(0, 100)}`);
  }

  return data;
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
