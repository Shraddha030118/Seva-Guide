import React from 'react';

export default function PortalScreen({ service, checklist, checkedDocs, onBack, onReset }) {
  const documents = checklist?.documents_required || [];
  const total = documents.length;
  const readyCount = documents.filter(d => checkedDocs[d.document_name]).length;
  const pct = total > 0 ? Math.round((readyCount / total) * 100) : 0;

  const portals = [
    {
      name: 'ServicePlus / ServiceOnline (National Portal)',
      url: service?.official_portal_url || 'https://serviceonline.gov.in',
      desc: 'Unified central portal used by 25+ States for Revenue and Civil certificate issuance.',
      badge: 'Official Central Portal',
      icon: '🏛️'
    },
    {
      name: 'State e-District Citizen Services',
      url: 'https://edistrict.gov.in',
      desc: 'State-specific digital delivery portal for revenue, caste, income, and local certificates.',
      badge: 'State Govt Portal',
      icon: '💻'
    },
    {
      name: 'DigiLocker (Ministry of Electronics & IT)',
      url: 'https://digilocker.gov.in',
      desc: 'Store, verify, and share your legally binding digitally signed certificate.',
      badge: 'Legal Digital Repository',
      icon: '🔒'
    },
    {
      name: 'Digital Seva CSC Portal (Assisted Mode)',
      url: 'https://digitalseva.csc.gov.in',
      desc: 'Find your nearest Common Services Centre (CSC) village kiosk for assisted application filing.',
      badge: 'Offline Assistance',
      icon: '🤝'
    }
  ];

  return (
    <div className="clear-card" role="region" aria-labelledby="portal-heading">
      <div className="clear-card-header">
        <div className="card-title-group">
          <h1 id="portal-heading">
            <span aria-hidden="true">🌐</span> Official Portals & Application Launchpad
          </h1>
          <p>Your preparation is ready. Proceed to the official verified government portals to submit your application.</p>
        </div>
        <span className="badge-tag" style={{ background: 'var(--color-success-bg)', color: 'var(--color-success)', fontSize: '0.85rem', padding: '0.4rem 0.8rem', border: '1px solid var(--color-success-border)' }}>
          Ready to Apply
        </span>
      </div>

      {/* Citizen Readiness Recap Card */}
      <div 
        style={{ 
          background: 'var(--color-primary-light)', 
          border: '2px solid var(--color-primary-border)', 
          borderRadius: 'var(--radius-lg)', 
          padding: '1.75rem', 
          marginBottom: '2rem' 
        }}
        role="region"
        aria-label="Citizen readiness summary"
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem', marginBottom: '1rem' }}>
          <div>
            <span style={{ fontSize: '0.85rem', fontWeight: 700, textTransform: 'uppercase', color: 'var(--color-primary)' }}>
              Selected Certificate
            </span>
            <h2 style={{ fontSize: '1.4rem', fontWeight: 800, color: 'var(--color-navy)', marginTop: '0.2rem' }}>
              {service?.title}
            </h2>
          </div>

          <div style={{ textAlign: 'right' }}>
            <span style={{ fontSize: '0.85rem', fontWeight: 700, textTransform: 'uppercase', color: 'var(--color-slate)' }}>
              Document Preparation
            </span>
            <div style={{ fontSize: '1.3rem', fontWeight: 800, color: pct === 100 ? 'var(--color-success)' : 'var(--color-primary)' }}>
              {readyCount} of {total} Prepared ({pct}%)
            </div>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', background: 'var(--color-surface)', padding: '1rem', borderRadius: 'var(--radius-md)' }}>
          <div>
            <span style={{ fontSize: '0.8rem', color: 'var(--color-slate)', fontWeight: 600 }}>GOVT FEE</span>
            <div style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--color-navy)' }}>₹{service?.fee?.amount}</div>
          </div>
          <div>
            <span style={{ fontSize: '0.8rem', color: 'var(--color-slate)', fontWeight: 600 }}>EXPECTED PROCESSING</span>
            <div style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--color-navy)' }}>{service?.estimated_processing_days} Business Days</div>
          </div>
          <div>
            <span style={{ fontSize: '0.8rem', color: 'var(--color-slate)', fontWeight: 600 }}>ISSUING AUTHORITY</span>
            <div style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--color-navy)' }}>{service?.department?.split('(')[0].trim()}</div>
          </div>
        </div>
      </div>

      {/* Official Government Portals Grid */}
      <h2 style={{ fontSize: '1.3rem', fontWeight: 700, marginBottom: '0.75rem', color: 'var(--color-navy)' }}>
        Authorized Government Links:
      </h2>
      <p style={{ color: 'var(--color-slate)', marginBottom: '1.25rem', fontSize: '0.95rem' }}>
        These are verified official government web portals. Avoid third-party commercial portals charging inflated brokerage fees.
      </p>

      <div className="portal-links-grid" role="list" aria-label="Official portal links">
        {portals.map((p, idx) => (
          <a
            key={idx}
            href={p.url}
            target="_blank"
            rel="noopener noreferrer"
            role="listitem"
            className="portal-link-card"
            aria-label={`Open ${p.name} in a new tab`}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
              <span style={{ fontSize: '1.8rem' }} aria-hidden="true">{p.icon}</span>
              <span className="badge-tag" style={{ background: 'var(--color-surface-muted)', color: 'var(--color-slate)', fontSize: '0.75rem' }}>
                {p.badge}
              </span>
            </div>

            <h3 className="portal-name">
              <span>{p.name}</span>
              <span aria-hidden="true">↗</span>
            </h3>

            <p style={{ fontSize: '0.9rem', color: 'var(--color-slate)', lineHeight: 1.5, flex: 1 }}>
              {p.desc}
            </p>

            <div style={{ marginTop: '1rem', paddingTop: '0.75rem', borderTop: '1px solid var(--color-slate-border)', color: 'var(--color-primary)', fontWeight: 700, fontSize: '0.9rem' }}>
              Open Official Website ↗
            </div>
          </a>
        ))}
      </div>

      {/* Final Guidance Card */}
      <div style={{ marginTop: '2rem', background: 'var(--color-surface-muted)', padding: '1.25rem 1.5rem', borderRadius: 'var(--radius-md)' }}>
        <h3 style={{ fontSize: '1.05rem', fontWeight: 700, marginBottom: '0.5rem', color: 'var(--color-navy)' }}>
          📋 What to do after submitting on the portal:
        </h3>
        <ol style={{ paddingLeft: '1.5rem', fontSize: '0.95rem', color: 'var(--color-slate)', lineHeight: 1.6 }}>
          <li>Download the Application Receipt with your unique Application Reference Number (ARN).</li>
          <li>Note down the tracking SMS received on your registered mobile number.</li>
          <li>Once approved, download the certificate PDF with the embedded digital signature stamp and QR verification code.</li>
        </ol>
      </div>

      {/* Navigation Footer */}
      <div className="screen-navigation-bar">
        <button type="button" className="btn btn-secondary btn-lg" onClick={onBack}>
          <span aria-hidden="true">←</span> Back to Next Steps Guide
        </button>

        <button 
          type="button" 
          className="btn btn-primary btn-lg" 
          onClick={onReset}
        >
          <span>Check Another Certificate</span> <span aria-hidden="true">↺</span>
        </button>
      </div>
    </div>
  );
}
