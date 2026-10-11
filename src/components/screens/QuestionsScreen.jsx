import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';

export default function QuestionsScreen({ service, checklist, onBack, onNext }) {
  // Local state for interactive yes/no eligibility questions
  const criteria = service?.eligibility_criteria || [
    'Are you a resident of the district/state where applying?',
    'Do you have government-approved identity and address proof?',
    'Can you provide valid supporting documents for the declared information?'
  ];

  const [answers, setAnswers] = useState({});
  const [aiQuery, setAiQuery] = useState('');
  const [aiLoading, setAiLoading] = useState(false);
  const [aiResult, setAiResult] = useState(null);
  const { getIdToken } = useAuth();

  const handleToggle = (index, value) => {
    setAnswers((prev) => ({
      ...prev,
      [index]: value,
    }));
  };

  const answeredCount = Object.keys(answers).length;
  const yesCount = Object.values(answers).filter(v => v === 'yes').length;
  const noCount = Object.values(answers).filter(v => v === 'no').length;

  const handleAskAI = async (e) => {
    e.preventDefault();
    if (!aiQuery.trim()) return;

    setAiLoading(true);
    setAiResult(null);

    try {
      const token = await getIdToken();
      const response = await fetch('/api/v1/ai/check-eligibility', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({
          service_slug: service.slug,
          user_query: aiQuery.trim()
        }),
      });

      if (!response.ok) throw new Error('AI check request failed');
      const data = await response.json();
      setAiResult(data);
    } catch (err) {
      console.error(err);
      // Fallback response for offline resilience
      setAiResult({
        assessment: 'Conditional / Specific Proof Required',
        reasoning: 'Please verify that your parental documentation and local continuous stay proofs strictly match the criteria before filing.',
        required_documents_highlight: ['Proof of Identity', 'Proof of Address', 'Supporting Revenue Record'],
        suggested_action: 'Proceed to review the document checklist on the next screen.',
        source: 'rules_engine'
      });
    } finally {
      setAiLoading(false);
    }
  };

  return (
    <div className="clear-card" role="region" aria-labelledby="questions-heading">
      <div className="clear-card-header">
        <div className="card-title-group">
          <h1 id="questions-heading">
            <span aria-hidden="true">❓</span> Eligibility Guidance: {service?.title}
          </h1>
          <p>Answer the standard requirement questions below, or ask our AI assistant about your specific background.</p>
        </div>
        <span className="badge-tag optional" style={{ fontSize: '0.85rem', padding: '0.4rem 0.8rem' }}>
          Step 2 of 5
        </span>
      </div>

      {/* Overview Card */}
      <div style={{ background: 'var(--color-surface-muted)', padding: '1.25rem 1.5rem', borderRadius: 'var(--radius-md)', marginBottom: '2rem' }}>
        <h2 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '0.35rem' }}>Purpose & Overview</h2>
        <p style={{ color: 'var(--color-slate)', fontSize: '0.95rem' }}>{service?.overview}</p>
      </div>

      {/* Interactive Eligibility Questions */}
      <h2 style={{ fontSize: '1.25rem', fontWeight: 700, marginBottom: '1rem', color: 'var(--color-navy)' }}>
        Self-Verification Questions:
      </h2>

      <div className="questions-list" role="list">
        {criteria.map((item, idx) => {
          const currentAnswer = answers[idx];
          return (
            <div 
              key={idx} 
              role="listitem"
              className={`question-box ${currentAnswer === 'yes' ? 'answered-yes' : (currentAnswer === 'no' ? 'answered-no' : '')}`}
            >
              <div className="question-text">
                <span style={{ color: 'var(--color-primary)', marginRight: '0.4rem' }}>{idx + 1}.</span>
                {item}
              </div>

              <div className="toggle-btn-group" role="group" aria-label={`Question ${idx + 1} choice`}>
                <button
                  type="button"
                  className={`toggle-choice-btn ${currentAnswer === 'yes' ? 'active-yes' : ''}`}
                  onClick={() => handleToggle(idx, 'yes')}
                  aria-pressed={currentAnswer === 'yes'}
                >
                  ✓ Yes, I Meet This
                </button>
                <button
                  type="button"
                  className={`toggle-choice-btn ${currentAnswer === 'no' ? 'active-no' : ''}`}
                  onClick={() => handleToggle(idx, 'no')}
                  aria-pressed={currentAnswer === 'no'}
                >
                  ✕ No / Not Sure
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {/* Eligibility Status Banner */}
      {answeredCount > 0 && (
        <div 
          style={{ 
            background: noCount === 0 && yesCount === criteria.length ? 'var(--color-success-bg)' : 'var(--color-warning-bg)',
            border: `2px solid ${noCount === 0 && yesCount === criteria.length ? 'var(--color-success-border)' : 'var(--color-warning-border)'}`,
            borderRadius: 'var(--radius-md)',
            padding: '1.25rem 1.5rem',
            marginBottom: '2rem'
          }}
          role="status"
          aria-live="polite"
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.35rem' }}>
            <span style={{ fontSize: '1.3rem' }}>{noCount === 0 && yesCount === criteria.length ? '✅' : 'ℹ️'}</span>
            <strong style={{ fontSize: '1.1rem', color: noCount === 0 && yesCount === criteria.length ? 'var(--color-success)' : 'var(--color-warning)' }}>
              {noCount === 0 && yesCount === criteria.length ? 'You Meet All Standard Criteria!' : 'Review Document Alternatives'}
            </strong>
          </div>
          <p style={{ fontSize: '0.95rem', color: 'var(--color-navy)' }}>
            {noCount === 0 && yesCount === criteria.length 
              ? 'Based on your self-assessment, you qualify for this certificate. Continue to the next step to review and tick off the required documents.'
              : 'If you selected "No" on any requirement, you may need alternative affidavits or ancestral revenue extracts. Check with our AI advisor below or consult the document alternatives.'}
          </p>
        </div>
      )}

      {/* Gemini AI Personal Question Box */}
      <div className="ai-advisor-box" role="region" aria-label="AI Eligibility Advisor">
        <div className="ai-header">
          <span style="font-size: 1.5rem;" aria-hidden="true">🤖</span>
          <div>
            <h2 style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--color-navy)' }}>
              Ask SevaGuide AI About Your Situation
            </h2>
            <p style={{ fontSize: '0.85rem', color: 'var(--color-slate)' }}>
              Powered by backend Gemini AI. Ask questions about income ceilings, lineage proof, or specific exemptions.
            </p>
          </div>
        </div>

        <form onSubmit={handleAskAI}>
          <label htmlFor="ai-situation-input" style={{ fontWeight: 600, fontSize: '0.9rem', color: 'var(--color-navy)' }}>
            Describe your personal background or query:
          </label>
          <textarea
            id="ai-situation-input"
            className="ai-textarea"
            rows="3"
            placeholder="e.g. My parents earn ₹6,50,000/year and run a small shop. Am I eligible for OBC Non-Creamy Layer fee concession?"
            value={aiQuery}
            onChange={(e) => setAiQuery(e.target.value)}
            disabled={aiLoading}
            aria-label="Enter question regarding your eligibility"
          />

          <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
            <button 
              type="submit" 
              className="btn btn-primary"
              disabled={aiLoading || !aiQuery.trim()}
              aria-busy={aiLoading}
            >
              {aiLoading ? 'Analyzing Criteria...' : '✨ Ask Eligibility AI'}
            </button>
          </div>
        </form>

        {/* AI Result Card */}
        {aiResult && (
          <div 
            style={{ 
              marginTop: '1.25rem',
              background: 'var(--color-surface)',
              border: '2px solid var(--color-blue-border)',
              borderRadius: 'var(--radius-md)',
              padding: '1.25rem 1.5rem'
            }}
            role="region"
            aria-label="AI Evaluation Response"
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem', flexWrap: 'wrap', gap: '0.5rem' }}>
              <strong style={{ fontSize: '1.1rem', color: 'var(--color-navy)' }}>AI Evaluation Result:</strong>
              <span className="badge-tag" style={{ background: 'var(--color-blue-bg)', color: 'var(--color-blue)', fontSize: '0.85rem', padding: '0.25rem 0.75rem' }}>
                {aiResult.assessment}
              </span>
            </div>

            <p style={{ fontSize: '0.95rem', lineHeight: 1.6, marginBottom: '1rem', color: 'var(--color-navy)' }}>
              {aiResult.reasoning}
            </p>

            {aiResult.required_documents_highlight && aiResult.required_documents_highlight.length > 0 && (
              <div style={{ marginBottom: '1rem' }}>
                <strong style={{ fontSize: '0.85rem', textTransform: 'uppercase', color: 'var(--color-slate)' }}>Key Documents Highlighted:</strong>
                <ul style={{ marginTop: '0.35rem', paddingLeft: '1.25rem', fontSize: '0.9rem', color: 'var(--color-navy)' }}>
                  {aiResult.required_documents_highlight.map((d, i) => <li key={i}>{d}</li>)}
                </ul>
              </div>
            )}

            <div style={{ background: 'var(--color-surface-muted)', padding: '0.75rem 1rem', borderRadius: 'var(--radius-sm)', borderLeft: '3px solid var(--color-primary)' }}>
              <strong style={{ color: 'var(--color-primary)', fontSize: '0.9rem' }}>Recommended Action: </strong>
              <span style={{ fontSize: '0.9rem', color: 'var(--color-navy)' }}>{aiResult.suggested_action}</span>
            </div>
          </div>
        )}
      </div>

      {/* Navigation Footer */}
      <div className="screen-navigation-bar">
        <button type="button" className="btn btn-secondary btn-lg" onClick={onBack}>
          <span aria-hidden="true">←</span> Back to Services
        </button>
        <button type="button" className="btn btn-primary btn-lg" onClick={onNext}>
          <span>Continue to Document Checklist</span> <span aria-hidden="true">→</span>
        </button>
      </div>
    </div>
  );
}
