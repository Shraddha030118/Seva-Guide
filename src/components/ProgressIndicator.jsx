import React from 'react';

const JOURNEY_STEPS = [
  { id: 1, label: '1. Select', subtitle: 'Choose Certificate', icon: '🏛️' },
  { id: 2, label: '2. Understand', subtitle: 'Eligibility Check', icon: '❓' },
  { id: 3, label: '3. Prepare', subtitle: 'Document Checklist', icon: '📄' },
  { id: 4, label: '4. Apply', subtitle: 'Steps & Official Portal', icon: '🚀' },
];

export default function ProgressIndicator({ currentStep, onStepClick, hasSelectedService }) {
  return (
    <nav className="stepper-container" aria-label="Core User Journey: Select, Understand, Prepare, Apply">
      <div className="stepper-inner">
        <div className="stepper-track" role="list">
          {JOURNEY_STEPS.map((step) => {
            const isActive = currentStep === step.id;
            const isCompleted = currentStep > step.id;
            const canNavigate = step.id === 1 || (hasSelectedService && step.id <= currentStep);

            return (
              <button
                key={step.id}
                role="listitem"
                className={`step-item ${isActive ? 'active' : ''} ${isCompleted ? 'completed' : ''}`}
                onClick={() => canNavigate && onStepClick(step.id)}
                disabled={!canNavigate}
                aria-current={isActive ? 'step' : undefined}
                aria-label={`Stage ${step.id}: ${step.label} - ${step.subtitle}. ${isCompleted ? 'Completed' : (isActive ? 'Current stage' : 'Not started')}`}
              >
                <div className="step-bubble" aria-hidden="true">
                  {isCompleted ? '✓' : step.id}
                </div>
                <div className="step-label">
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                    <span aria-hidden="true">{step.icon}</span>
                    <strong style={{ fontSize: '0.95rem' }}>{step.label}</strong>
                  </div>
                  <div style={{ fontSize: '0.78rem', color: 'var(--color-slate)', fontWeight: 500 }}>
                    {step.subtitle}
                  </div>
                </div>
              </button>
            );
          })}
        </div>
      </div>
    </nav>
  );
}
