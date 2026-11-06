import React from 'react';
import { 
  Milestone, 
  Image, 
  BrainCircuit, 
  TrendingUp, 
  ShieldCheck, 
  CheckCircle2,
  Layers,
  SearchCheck,
  Scale
} from 'lucide-react';

export default function Round3Roadmap() {
  const improvements = [
    {
      num: '01',
      title: 'Multimodal Brand Integrity',
      subtitle: 'Visual, Asset & Accessibility Governance',
      icon: Image,
      description: 'Extending Inkloom Sentinel from pure textual analysis to computer vision and graphic layout validation.',
      capabilities: [
        'Automated Logo Verification: Clearance margins, distortion detection, and monochrome vs color asset fidelity.',
        'Brand Color Palette Analysis: Hex/RGB extraction from images with Delta-E perceptual color difference scoring against official #405746 and #F8F7F4 tokens.',
        'WCAG 2.1 Accessibility: Contrast ratio checking for foreground text over brand background surfaces.',
        'Visual Consistency: Typography font-family verification across raster and vector marketing banners.'
      ]
    },
    {
      num: '02',
      title: 'Intelligent Brand Truth Management',
      subtitle: 'Contradiction Detection & Passport Lifecycle',
      icon: BrainCircuit,
      description: 'Next-generation semantic knowledge reasoning to resolve conflicting corporate claims and manage time-decaying evidence.',
      capabilities: [
        'Advanced Contradiction Detection: Multi-hop logical inference to detect subtle incompatibilities across dispersed regulatory filings.',
        'Claim Passport Expiry Lifecycle: Automated notification triggers and review queue deprecation when source SLA/audit evidence expires.',
        'Source Conflict Resolution: Hierarchical precedence rules between corporate board charters, CFO pricing memos, and regional marketing copy.',
        'Blast-Radius Impact Simulation: Simulates the cascading impact across all historical and pending submissions whenever an approved fact (e.g. ₹399 fee) changes.'
      ]
    },
    {
      num: '03',
      title: 'Governance Intelligence & Analytics',
      subtitle: 'Predictive Policy Optimization & Audit Analytics',
      icon: TrendingUp,
      description: 'Enterprise intelligence engine that converts brand review friction into actionable guideline improvements.',
      capabilities: [
        'Recurring Violation Analytics: Cluster detection identifying specific departments, agencies, or AI prompts that repeatedly fail tone rules.',
        'Ambiguous Guideline Identification: Identifies brand rules with high reviewer override rates, signaling that the underlying policy is poorly drafted.',
        'Agency SLA Tracking: Turnaround time analytics between Creator draft submission, Fix Assistant acceptance, and Reviewer cryptographic sign-off.',
        'Automated Executive Compliance Briefings: Exportable board-ready audit summaries with verifiable Ed25519 hash trees.'
      ]
    }
  ];

  return (
    <div className="p-8 max-w-5xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-center space-x-2 text-[11px] font-semibold text-[#405746] uppercase tracking-wider">
          <span>Enterprise Platform Architecture</span>
          <span>•</span>
          <span>Strategic Milestones</span>
        </div>
        <h2 className="text-xl font-semibold text-[#242522] tracking-tight mt-1">
          Product & Architectural Roadmap
        </h2>
        <p className="text-xs text-[#77766F] mt-1 max-w-2xl leading-relaxed">
          Inkloom Sentinel delivers an enterprise brand governance pipeline with verifiable Ed25519 digital signature seals. The following architectural advancements represent scheduled enterprise capabilities.
        </p>
      </div>

      {/* Improvement Cards */}
      <div className="space-y-6">
        {improvements.map((imp) => {
          const Icon = imp.icon;
          return (
            <div
              key={imp.num}
              className="bg-white border border-[#E8E6DF] rounded-md p-6 shadow-2xs space-y-4"
            >
              <div className="flex items-start justify-between">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 rounded bg-[#FAF9F6] border border-[#E8E6DF] flex items-center justify-center text-[#405746]">
                    <Icon className="w-5 h-5" />
                  </div>
                  <div>
                    <span className="text-[10px] font-mono text-[#77766F] uppercase tracking-wider">
                      Capability {imp.num}
                    </span>
                    <h3 className="text-base font-semibold text-[#242522]">
                      {imp.title}
                    </h3>
                    <p className="text-xs text-[#405746] font-medium">
                      {imp.subtitle}
                    </p>
                  </div>
                </div>
                <span className="text-xs font-mono px-2 py-0.5 rounded bg-[#FAF9F6] border border-[#E8E6DF] text-[#77766F]">
                  Scheduled Milestone
                </span>
              </div>

              <p className="text-xs text-[#77766F] leading-relaxed">
                {imp.description}
              </p>

              <div className="pt-3 border-t border-[#E8E6DF] grid grid-cols-1 md:grid-cols-2 gap-3">
                {imp.capabilities.map((cap, cIdx) => (
                  <div key={cIdx} className="flex items-start space-x-2 text-xs text-[#242522]">
                    <CheckCircle2 className="w-4 h-4 text-[#405746] shrink-0 mt-0.5" />
                    <span className="leading-relaxed">{cap}</span>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
