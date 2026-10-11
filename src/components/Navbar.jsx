import React from 'react';

export default function Navbar({ currentStep, onReset, theme, onToggleTheme, fontScale, onChangeFontScale }) {
  return (
    <header className="app-header" role="banner">
      <div className="header-inner">
        <button 
          className="brand-wrapper" 
          onClick={onReset}
          aria-label="SevaGuide Home - Citizen Certificate Assistant"
        >
          <div className="brand-badge-icon" aria-hidden="true">🏛️</div>
          <div>
            <div className="brand-title">SevaGuide</div>
            <div className="brand-subtitle">Citizen Public Service Assistant</div>
          </div>
        </button>

        <div className="header-controls" role="toolbar" aria-label="Accessibility and display settings">
          <button 
            className="accessibility-btn"
            onClick={onChangeFontScale}
            aria-label={`Change text size. Current: ${fontScale}`}
            title="Adjust text size for easier reading"
          >
            <span aria-hidden="true">🔤</span> Text: {fontScale === 'normal' ? 'Standard' : (fontScale === 'large' ? 'Large' : 'X-Large')}
          </button>

          <button 
            className="accessibility-btn"
            onClick={onToggleTheme}
            aria-label={`Toggle theme. Current: ${theme}`}
            title="Toggle high contrast dark/light mode"
          >
            <span aria-hidden="true">{theme === 'dark' ? '☀️' : '🌙'}</span> {theme === 'dark' ? 'Light Mode' : 'Dark Mode'}
          </button>
        </div>
      </div>
    </header>
  );
}
