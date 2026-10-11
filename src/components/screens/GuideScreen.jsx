import React from 'react';

export default function GuideScreen({ service, checklist, onBack, onNext }) {
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

  return (
    <div className="clear-card" role="region" aria-labelledby="guide-heading">
      <div className="clear-card-header">
        <div className="card-title-group">
          <h1 id="guide-heading">
            <span aria-hidden="true">🗺️</span> Step-by-Step Procedure: {service?.title}
          </h1>
          <p>Follow these 5 simple sequential steps from home to receive your digitally signed certificate.</p>
        </div>
        <span className="badge-tag optional" style={{ fontSize: '0.85rem', padding: '0.4rem 0.8rem' }}>
          Step 4 of 5
        </span>
      </div>

      {/* Procedural Timeline */}
      <div className="timeline-list" role="list" aria-label="Step-by-step application timeline">
        {steps.map((st) => (
          <div key={st.step_number} role="listitem" className="timeline-step-card">
            <div className="step-num-badge" aria-hidden="true">
              {st.step_number}
            </div>

            <div className="step-content">
              <div className="step-heading-row">
                <h2 className="step-heading">
                  Step {st.step_number}: {st.title}
                </h2>
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
          <h2 style={{ fontSize: '1.15rem', color: 'var(--color-danger)', fontWeight: 800 }}>
            Common Rejection Traps to Avoid:
          </h2>
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
          <h2 style={{ fontSize: '1.15rem', color: 'var(--color-success)', fontWeight: 800 }}>
            Pro-Tips for Fast Approval:
          </h2>
        </div>
        <ul style={{ paddingLeft: '1.5rem', color: 'var(--color-navy)', fontSize: '0.95rem' }}>
          {tips.map((t, idx) => (
            <li key={idx} style={{ marginBottom: '0.4rem' }}>{t}</li>
          ))}
        </ul>
      </div>

      {/* Navigation Footer */}
      <div className="screen-navigation-bar">
        <button type="button" className="btn btn-secondary btn-lg" onClick={onBack}>
          <span aria-hidden="true">←</span> Back to Document Checklist
        </button>
        <button type="button" className="btn btn-primary btn-lg" onClick={onNext}>
          <span>Proceed to Official Website Links</span> <span aria-hidden="true">→</span>
        </button>
      </div>
    </div>
  );
}
