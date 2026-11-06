import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, useNavigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import Overview from './pages/Overview';
import BrandVault from './pages/BrandVault';
import ContentStudio from './pages/ContentStudio';
import ReviewWorkspace from './pages/ReviewWorkspace';
import ApprovalHub from './pages/ApprovalHub';
import ReleasePublish from './pages/ReleasePublish';
import ReviewHistory from './pages/ReviewHistory';
import Round3Roadmap from './pages/Round3Roadmap';

function AppLayout() {
  const [currentRole, setCurrentRole] = useState(
    localStorage.getItem('inkloom_user_role') || 'CREATOR'
  );
  const navigate = useNavigate();

  const handleRoleChange = (role) => {
    setCurrentRole(role);
  };

  const handleSelectScenario = (scenario) => {
    navigate('/new-review');
    setTimeout(() => {
      const btn = document.querySelector(`button[title*="Scenario ${scenario}"]`);
      if (btn) btn.click();
    }, 100);
  };

  return (
    <div className="flex h-screen bg-[#F8F7F4] text-[#242522] overflow-hidden">
      {/* Sidebar */}
      <Sidebar currentRole={currentRole} onRoleChange={handleRoleChange} />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 overflow-y-auto">
        <Header 
          title="Inkloom Sentinel" 
          subtitle="Enterprise Brand Integrity & Governance Platform"
          onSelectScenario={handleSelectScenario}
        />

        <main className="flex-1 pb-12">
          <Routes>
            <Route path="/" element={<Overview />} />
            <Route path="/brand-vault" element={<BrandVault />} />
            <Route path="/new-review" element={<ContentStudio />} />
            <Route path="/workspace/:id" element={<ReviewWorkspace />} />
            <Route 
              path="/approvals" 
              element={<ApprovalHub currentRole={currentRole} onRoleChange={handleRoleChange} />} 
            />
            <Route path="/release/:id" element={<ReleasePublish />} />
            <Route path="/history" element={<ReviewHistory />} />
            <Route path="/roadmap" element={<Round3Roadmap />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AppLayout />
    </BrowserRouter>
  );
}
