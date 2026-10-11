import React from 'react';

export default function ApplyScreen({ service, checklist, checkedDocs, onBack, onReset }) {
  const documents = checklist?.documents_required || [];
  const total = documents.length;
  const readyCount = documents.filter(d => checkedDocs[d.document_name]).length;
  const pct = total > 0 ? Math.round((readyCount / total) * 100) : 0;

  const steps = checklist?.application_steps || [
    {
      step_number: 1,
      phase: 'Preparation',
      title: 'Self-Attest & Scan Documents',
      description: 'Sign across all photocopies and scan into individual clear PDF files under 1 MB each.',
      estimated_time: '20 mins',
      online_or_offline: 'Offline',
      action_items: [
        'Write "Self Attested" and sign on each copy',
        'Verify applicant name matches Aadhaar exactly',
        'Save scans with clear file names'
      ]
    },
    {
      step_number: 2,
      phase: 'Registration',
      title: 'Portal Signup & Account Verification',
      description: 'Register with mobile OTP on the official state citizen portal (e-District / ServicePlus).',
      estimated_time: '10 mins',
      online_or_offline: 'Online',
      action_items: [
        'Visit state service portal',
        'Complete Aadhaar mobile OTP validation',
        'Set up citizen login credentials'
      ]
    },
    {
      step_number: 3,
      phase: 'Form Filing',
      title: 'Submit Application & Pay Government Fee',
      description: 'Fill in residential details, upload PDF attachments, and pay the statutory fee online.',
      estimated_time: '15 mins',
      online_or_offline: 'Online',
      action_items: [
        'Select certificate service under Revenue',
        'Upload prepared document scans',
        'Pay fee via UPI or Net Banking and download ARN acknowledgement'
      ]
    },
    {
      step_number: 4,
      phase: 'Verification',
      title: 'Revenue Inspector / Patwari Local Inquiry',
      description: 'Field officer reviews documents and conducts locality check.',
      estimated_time: '7-10 Days',
      online_or_offline: 'Hybrid',
      action_items: [
        'Track status using ARN number',
        'Keep original documents ready if called for spot verification'
      ]
    },
    {
      step_number: 5,
      phase: 'Download',
      title: 'Download Digitally Signed Certificate',
      description: 'Download the QR-coded official certificate approved by the Sub-Divisional Magistrate or Tehsildar.',
      estimated_time: '3 Days',
      online_or_offline: 'Online',
      action_items: [
        'Download digitally signed PDF certificate',
        'Store authentic copy in your DigiLocker account'
      ]
    }
  ];

  const commonMistakes = checklist?.common_mistakes || [
    'Submitting un-attested photocopies without signature',
    'Spelling discrepancies between Aadhaar and academic/property records',
    'Applying under wrong Tehsil jurisdiction'
  ];

  const tips = checklist?.helpful_tips || [
    'Save your Application Reference Number (ARN) immediately after payment',
    'Link the issued certificate to DigiLocker for instant legal verification anywhere'
  ];

  const portals = [
    {
      name: 'ServicePlus / ServiceOnline (National Portal)',
      url: service?.official_portal_url || 'https://serviceonline.gov.in',
      desc: 'Primary official portal for online application submission, fee payment, and tracking.',
      badge: 'Official Portal',
      icon: '🏛️'
    },
    {
      name: 'State e-District Citizen Services',
      url: 'https://edistrict.gov.in',
      desc: 'State-specific digital delivery portal for revenue, caste, and income certificates.',
      badge: 'State Govt',
      icon: '💻'
    },
    {
      name: 'DigiLocker (Ministry of Electronics & IT)',
      url: 'https://digilocker.gov.in',
      desc: 'Official cloud repository to retrieve and store digitally signed certificates.',
      badge: 'Digital Locker',
      icon: '🔒'
    },
    {
      name: 'Digital Seva CSC Portal (Assisted Kiosks)',
      url: 'https://digitalseva.csc.gov.in',
      desc: 'Locate nearest Gram Panchayat Common Services Centre for in-person assistance.',
      badge: 'Assisted Mode',
      icon: '🤝'
    }
  ];

  const officialUrl = service?.official_portal_url || 'https://serviceonline.gov.in';

  return (
    <div className="clear-card" role="region" aria-labelledby="apply-heading">
      <div className="clear-card-header">
        <div className="card-title-group">
          <h1 id="apply-heading">
            <span aria-hidden="true">🚀</span> Apply for {service?.title}
          </h1>
          <p>Follow the practical procedural steps below and launch the authorized government portal to file your application.</p>
        </div>
        <span className="badge-tag" style={{ background: 'var(--color-success-bg)', color: 'var(--color-success)', fontSize: '0.85rem', padding: '0.4rem 0.8rem', border: '1px solid var(--color-success-border)' }}>
          Stage 4 of 4: Apply
        </span>
      </div>

      {/* Prominent Call to Action - Launch Government Portal */}
      <div 
        style={{ 
          background: 'linear-gradient(135deg, var(--color-surface), var(--color-primary-light))', 
          border: '3px solid var(--color-primary)', 
          borderRadius: 'var(--radius-lg)', 
          padding: '2rem', 
          marginBottom: '2.5rem',
          boxShadow: 'var(--shadow-md)'
        }}
        role="region"
        aria-label="Official Portal Launch Center"
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1.25rem' }}>
          <div style={{ flex: '1 1 300px' }}>
            <span className="badge-tag mandatory" style={{ background: 'var(--color-primary)', color: '#ffffff', borderColor: 'var(--color-primary)', marginBottom: '0.5rem', display: 'inline-block' }}>
              Final Step: Official Submission
            </span>
            <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--color-navy)', marginBottom: '0.5rem' }}>
              Ready to Submit Your Application
            </h2>
            <p style={{ color: 'var(--color-slate)', fontSize: '1rem', lineHeight: 1.5 }}>
              Your document preparation is <strong>{pct}% complete</strong> ({readyCount} of {total} documents ready). Click below to launch the official authorized portal to upload documents and pay the ₹{service?.fee?.amount} fee.
            </p>
          </div>

          <div style={{ flex: '0 0 auto' }}>
            <a
              href={officialUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="btn btn-primary btn-lg"
              style={{
                fontSize: '1.2rem',
                padding: '1.1rem 2.2rem',
                boxShadow: '0 6px 20px rgba(234, 88, 12, 0.4)',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '0.75rem'
              }}
              aria-label={`Open official government portal for ${service?.title} in a new tab`}
            >
              <span>Open Official Government Portal</span>
              <span aria-hidden="true" style={{ fontSize: '1.4rem' }}>↗</span>
            </a>
          </div>
        </div>

        {/* Quick Details Bar */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1rem', marginTop: '1.5rem', paddingTop: '1.25rem', borderTop: '1px solid var(--color-primary-border)' }}>
          <div>
            <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--color-slate)', textTransform: 'uppercase' }}>Government Fee</span>
            <div style={{ fontSize: '1.15rem', fontWeight: 800, color: 'var(--color-navy)' }}>₹{service?.fee?.amount}</div>
          </div>
          <div>
            <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--color-slate)', textTransform: 'uppercase' }}>Processing SLA</span>
            <div style={{ fontSize: '1.15rem', fontWeight: 800, color: 'var(--color-navy)' }}>{service?.estimated_processing_days} Business Days</div>
          </div>
          <div>
            <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--color-slate)', textTransform: 'uppercase' }}>Issuing Department</span>
            <div style={{ fontSize: '1.05rem', fontWeight: 700, color: 'var(--color-navy)' }}>{service?.department?.split('(')[0].trim()}</div>
          </div>
          <div>
            <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--color-slate)', textTransform: 'uppercase' }}>Certificate Validity</span>
            <div style={{ fontSize: '1.05rem', fontWeight: 700, color: 'var(--color-navy)' }}>{service?.validity_period}</div>
          </div>
        </div>
      </div>

      {/* Practical Steps Roadmap */}
      <h2 style={{ fontSize: '1.35rem', fontWeight: 800, marginBottom: '0.75rem', color: 'var(--color-navy)' }}>
        <span aria-hidden="true">🗺️ </span>Clear Practical Steps (Follow in Order):
      </h2>
      <p style={{ color: 'var(--color-slate)', marginBottom: '1.5rem', fontSize: '1rem' }}>
        Step-by-step roadmap for completing your application on the official portal without mistakes.
      </p>

      <div className="timeline-list" role="list" aria-label="Step-by-step application timeline">
        {steps.map((st) => (
          <div key={st.step_number} role="listitem" className="timeline-step-card">
            <div className="step-num-badge" aria-hidden="true">
              {st.step_number}
            </div>

            <div className="step-content">
              <div className="step-heading-row">
                <h3 className="step-heading" style={{ fontSize: '1.2rem' }}>
                  Step {st.step_number}: {st.title}
                </h3>
                <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap' }}>
                  <span className="step-phase-pill">
                    {st.phase}
                  </span>
                  <span className="step-phase-pill" style={{ color: 'var(--color-primary)' }}>
                    ⏱️ {st.estimated_time}
                  </span>
                  <span className="step-phase-pill" style={{ color: 'var(--color-blue)' }}>
                    🌐 {st.online_or_offline}
                  </span>
                </div>
              </div>

              <p style={{ color: 'var(--color-navy)', fontSize: '0.95rem', lineHeight: 1.5 }}>
                {st.description}
              </p>

              {st.action_items && st.action_items.length > 0 && (
                <ul className="step-action-bullets" aria-label={`Action items for step ${st.step_number}`}>
                  {st.action_items.map((act, i) => (
                    <li key={i}>{act}</li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Traps to Avoid Banner */}
      <div 
        style={{ 
          marginTop: '2.5rem',
          background: 'var(--color-danger-bg)',
          border: '2px solid var(--color-danger-border)',
          borderRadius: 'var(--radius-lg)',
          padding: '1.5rem'
        }}
        role="region"
        aria-label="Common rejection pitfalls to avoid"
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' }}>
          <span style={{ fontSize: '1.4rem' }} aria-hidden="true">⚠️</span>
          <h3 style={{ fontSize: '1.15rem', color: 'var(--color-danger)', fontWeight: 800 }}>
            Common Rejection Traps to Avoid:
          </h3>
        </div>
        <ul style={{ paddingLeft: '1.5rem', color: 'var(--color-navy)', fontSize: '0.95rem' }}>
          {commonMistakes.map((m, idx) => (
            <li key={idx} style={{ marginBottom: '0.4rem' }}>{m}</li>
          ))}
        </ul>
      </div>

      {/* Pro Tips Banner */}
      <div 
        style={{ 
          marginTop: '1.25rem',
          background: 'var(--color-success-bg)',
          border: '2px solid var(--color-success-border)',
          borderRadius: 'var(--radius-lg)',
          padding: '1.5rem'
        }}
        role="region"
        aria-label="Pro tips for faster processing"
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' }}>
          <span style={{ fontSize: '1.4rem' }} aria-hidden="true">💡</span>
          <h3 style={{ fontSize: '1.15rem', color: 'var(--color-success)', fontWeight: 800 }}>
            Pro-Tips for Fast Approval:
          </h3>
        </div>
        <ul style={{ paddingLeft: '1.5rem', color: 'var(--color-navy)', fontSize: '0.95rem' }}>
          {tips.map((t, idx) => (
            <li key={idx} style={{ marginBottom: '0.4rem' }}>{t}</li>
          ))}
        </ul>
      </div>

      {/* Other Government Links */}
      <div style={{ marginTop: '2.5rem' }}>
        <h3 style={{ fontSize: '1.2rem', fontWeight: 800, marginBottom: '0.5rem', color: 'var(--color-navy)' }}>
          🏛️ Alternative Verified Official Portals:
        </h3>
        <p style={{ color: 'var(--color-slate)', fontSize: '0.95rem', marginBottom: '1rem' }}>
          Access DigiLocker or locate offline Common Services Center (CSC) assistance:
        </p>

        <div className="portal-links-grid" role="list">
          {portals.map((p, idx) => (
            <a
              key={idx}
              href={p.url}
              target="_blank"
              rel="noopener noreferrer"
              role="listitem"
              className="portal-link-card"
              aria-label={`Open ${p.name}`}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                <span style={{ fontSize: '1.6rem' }} aria-hidden="true">{p.icon}</span>
                <span className="badge-tag" style={{ background: 'var(--color-surface-muted)', color: 'var(--color-slate)', fontSize: '0.75rem' }}>
                  {p.badge}
                </span>
              </div>
              <strong style={{ fontSize: '1.05rem', color: 'var(--color-navy)', marginBottom: '0.35rem' }}>
                {p.name} ↗
              </strong>
              <p style={{ fontSize: '0.88rem', color: 'var(--color-slate)', lineHeight: 1.4 }}>
                {p.desc}
              </p>
            </a>
          ))}
        </div>
      </div>

      {/* Navigation Footer */}
      <div className="screen-navigation-bar">
        <button type="button" className="btn btn-secondary btn-lg" onClick={onBack}>
          <span aria-hidden="true">←</span> Back to Prepare (Checklist)
        </button>

        <button 
          type="button" 
          className="btn btn-secondary btn-lg" 
          onClick={onReset}
        >
          <span>↺ Choose Another Certificate</span>
        </button>
      </div>
    </div>
  );
}
