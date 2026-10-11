import React from 'react';

export default function ChecklistScreen({ service, checklist, checkedDocs, onToggleDoc, onMarkAllDocs, onResetDocs, onBack, onNext }) {
  const documents = checklist?.documents_required || [
    {
      document_name: 'Proof of Identity',
      category: 'Identity',
      is_mandatory: true,
      description: 'Government photo identification with matching applicant name.',
      accepted_options: ['Aadhaar Card', 'Voter ID (EPIC)', 'Passport', 'Driving License'],
      format_guidelines: 'Self-attested photocopy scanned to PDF under 1 MB.'
    },
    {
      document_name: 'Proof of Address',
      category: 'Address',
      is_mandatory: true,
      description: 'Proof of local residence within the Tehsildar jurisdiction.',
      accepted_options: ['Ration Card', 'Electricity Bill', 'Water Bill', 'Rent Agreement'],
      format_guidelines: 'Readable consumer number and address, scanned to PDF.'
    },
    {
      document_name: 'Self-Declaration Affidavit',
      category: 'Affidavit',
      is_mandatory: true,
      description: 'Sworn undertaking verifying information is accurate.',
      accepted_options: ['State E-District format', 'Notarized Stamp Paper'],
      format_guidelines: 'Signed by applicant or legal guardian.'
    }
  ];

  const total = documents.length;
  const readyCount = documents.filter(d => checkedDocs[d.document_name]).length;
  const pct = total > 0 ? Math.round((readyCount / total) * 100) : 0;

  return (
    <div className="clear-card" role="region" aria-labelledby="checklist-heading">
      <div className="clear-card-header">
        <div className="card-title-group">
          <h1 id="checklist-heading">
            <span aria-hidden="true">📄</span> Document Preparation Checklist: {service?.title}
          </h1>
          <p>Tick off each document as you collect it to ensure zero rejections during verification.</p>
        </div>
        <span className="badge-tag optional" style={{ fontSize: '0.85rem', padding: '0.4rem 0.8rem' }}>
          Step 3 of 5
        </span>
      </div>

      {/* Progress Indicator Card */}
      <div className="progress-card" role="region" aria-label="Document readiness progress">
        <div className="progress-card-header">
          <div className="progress-title">
            <span aria-hidden="true">📊</span>
            <span>Citizen Readiness Progress</span>
          </div>
          <div className="progress-percentage" aria-live="polite">
            {pct}% Complete ({readyCount} of {total} documents ready)
          </div>
        </div>

        <div 
          className="progress-track-bg" 
          role="progressbar" 
          aria-valuenow={pct} 
          aria-valuemin="0" 
          aria-valuemax="100"
          aria-label={`Document preparation: ${pct}% complete`}
        >
          <div className="progress-track-fill" style={{ width: `${pct}%` }}></div>
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '0.75rem', flexWrap: 'wrap', gap: '0.5rem' }}>
          <span style={{ fontSize: '0.85rem', color: 'var(--color-primary)', fontWeight: 600 }}>
            {pct === 100 ? '🎉 All documents ready! You are prepared to apply.' : 'Keep collecting your documents.'}
          </span>
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <button 
              type="button" 
              className="accessibility-btn" 
              onClick={onMarkAllDocs}
              style={{ padding: '0.3rem 0.75rem', fontSize: '0.8rem' }}
            >
              ✓ Mark All Ready
            </button>
            <button 
              type="button" 
              className="accessibility-btn" 
              onClick={onResetDocs}
              style={{ padding: '0.3rem 0.75rem', fontSize: '0.8rem' }}
            >
              ↺ Reset
            </button>
          </div>
        </div>
      </div>

      {/* Checklist Items */}
      <div className="checklist-container" role="list" aria-label="Required documents list">
        {documents.map((doc, idx) => {
          const isChecked = !!checkedDocs[doc.document_name];
          const inputId = `doc-checkbox-${idx}`;

          return (
            <div 
              key={idx} 
              role="listitem"
              className={`checklist-card-item ${isChecked ? 'checked' : ''}`}
            >
              <div className="custom-checkbox-wrapper">
                <input
                  type="checkbox"
                  id={inputId}
                  className="large-checkbox"
                  checked={isChecked}
                  onChange={() => onToggleDoc(doc.document_name)}
                  aria-describedby={`desc-${idx}`}
                />
              </div>

              <div className="doc-info-block">
                <div className="doc-title-row">
                  <label htmlFor={inputId} className="doc-title" style={{ cursor: 'pointer' }}>
                    {doc.document_name}
                  </label>
                  <span className={`badge-tag ${doc.is_mandatory ? 'mandatory' : 'optional'}`}>
                    {doc.is_mandatory ? 'Mandatory' : 'Optional'}
                  </span>
                  <span className="badge-tag optional">
                    {doc.category}
                  </span>
                </div>

                <p id={`desc-${idx}`} style={{ fontSize: '0.95rem', color: 'var(--color-slate)', marginTop: '0.2rem' }}>
                  {doc.description}
                </p>

                {doc.accepted_options && doc.accepted_options.length > 0 && (
                  <div className="doc-accepted-list">
                    <strong>Accepted Options: </strong>
                    <span>{doc.accepted_options.join(', ')}</span>
                  </div>
                )}

                {doc.format_guidelines && (
                  <div className="doc-format-box">
                    <span aria-hidden="true">ℹ️ </span>
                    <span><strong>Formatting Rule: </strong>{doc.format_guidelines}</span>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Navigation Footer */}
      <div className="screen-navigation-bar">
        <button type="button" className="btn btn-secondary btn-lg" onClick={onBack}>
          <span aria-hidden="true">←</span> Back to Eligibility
        </button>
        <button type="button" className="btn btn-primary btn-lg" onClick={onNext}>
          <span>Continue to Application Guide</span> <span aria-hidden="true">→</span>
        </button>
      </div>
    </div>
  );
}
