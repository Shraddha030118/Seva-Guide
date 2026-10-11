import React, { useState } from 'react';

export default function HomeScreen({ services, selectedService, onSelectService, loading }) {
  const [search, setSearch] = useState('');
  const [activeCategory, setActiveCategory] = useState('All');

  const categories = ['All', 'Revenue & Welfare', 'Social Justice & Empowerment', 'Revenue & General Administration'];

  const filteredServices = services.filter((svc) => {
    const matchesSearch = 
      svc.title.toLowerCase().includes(search.toLowerCase()) ||
      svc.short_description.toLowerCase().includes(search.toLowerCase()) ||
      (svc.tags && svc.tags.some(t => t.toLowerCase().includes(search.toLowerCase())));

    const matchesCategory = 
      activeCategory === 'All' || 
      svc.category.toLowerCase().includes(activeCategory.toLowerCase().split('&')[0].trim());

    return matchesSearch && matchesCategory;
  });

  const getServiceIcon = (slug) => {
    if (slug.includes('income')) return '💰';
    if (slug.includes('caste')) return '📜';
    if (slug.includes('residence') || slug.includes('domicile')) return '🏠';
    return '📋';
  };

  return (
    <div className="clear-card" role="region" aria-labelledby="home-heading">
      <div className="clear-card-header">
        <div className="card-title-group">
          <h1 id="home-heading">
            <span aria-hidden="true">🏛️</span> Select a Government Certificate
          </h1>
          <p>Choose an official service below to check your eligibility, prepare documents, and apply without delays.</p>
        </div>
      </div>

      {/* Accessible Search & Category Filter */}
      <div style={{ marginBottom: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        <div style={{ position: 'relative' }}>
          <label htmlFor="certificate-search" style={{ display: 'block', fontWeight: 700, marginBottom: '0.4rem', fontSize: '0.95rem' }}>
            🔍 Search by Certificate Name or Keyword:
          </label>
          <input
            id="certificate-search"
            type="search"
            className="ai-textarea"
            style={{ margin: 0, padding: '0.85rem 1rem' }}
            placeholder="e.g. Income Certificate, EWS, Caste, Domicile..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            aria-label="Search certificate services"
          />
        </div>

        {/* Category Pills */}
        <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }} role="group" aria-label="Filter certificates by department category">
          {categories.map((cat) => (
            <button
              key={cat}
              className="accessibility-btn"
              style={{
                background: activeCategory === cat ? 'var(--color-primary)' : 'var(--color-surface)',
                color: activeCategory === cat ? '#ffffff' : 'var(--color-navy)',
                borderColor: activeCategory === cat ? 'var(--color-primary)' : 'var(--color-slate-border)',
                fontWeight: 700,
                padding: '0.5rem 1rem'
              }}
              onClick={() => setActiveCategory(cat)}
              aria-pressed={activeCategory === cat}
            >
              {cat === 'All' ? 'All Services' : cat}
            </button>
          ))}
        </div>
      </div>

      {/* Services Grid */}
      {loading ? (
        <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--color-slate)' }}>
          <p style={{ fontSize: '1.2rem', fontWeight: 600 }}>Loading official certificate directory...</p>
        </div>
      ) : filteredServices.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '3rem', background: 'var(--color-surface-muted)', borderRadius: 'var(--radius-md)' }}>
          <p style={{ fontSize: '1.1rem', fontWeight: 600, color: 'var(--color-slate)' }}>No certificates matched "{search}".</p>
          <button 
            className="btn btn-secondary" 
            style={{ marginTop: '1rem' }} 
            onClick={() => { setSearch(''); setActiveCategory('All'); }}
          >
            Reset Filters
          </button>
        </div>
      ) : (
        <div className="services-grid" role="list">
          {filteredServices.map((svc) => {
            const isSelected = selectedService?.slug === svc.slug;
            return (
              <div
                key={svc.slug}
                role="listitem"
                tabIndex={0}
                className={`service-card ${isSelected ? 'selected' : ''}`}
                onClick={() => onSelectService(svc)}
                onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') onSelectService(svc); }}
                aria-label={`Select ${svc.title}. Fee: ₹${svc.fee.amount}. Processing time: ${svc.estimated_processing_days} days.`}
              >
                <div className="service-icon-box" aria-hidden="true">
                  {getServiceIcon(svc.slug)}
                </div>

                <span className="service-badge">{svc.category}</span>
                <h2 className="service-card-title">{svc.title}</h2>
                <p className="service-card-desc">{svc.short_description}</p>

                <div className="service-meta-grid" aria-label="Service details">
                  <div className="meta-col">
                    <span className="meta-label-sm">Statutory Fee</span>
                    <span className="meta-val-lg">₹{svc.fee.amount}</span>
                  </div>
                  <div className="meta-col">
                    <span className="meta-label-sm">Processing Time</span>
                    <span className="meta-val-lg">{svc.estimated_processing_days} Days</span>
                  </div>
                  <div className="meta-col">
                    <span className="meta-label-sm">Validity</span>
                    <span className="meta-val-lg">{svc.validity_period}</span>
                  </div>
                  <div className="meta-col">
                    <span className="meta-label-sm">Department</span>
                    <span className="meta-val-lg">{svc.department.split('(')[0].trim()}</span>
                  </div>
                </div>

                <button 
                  className="btn btn-primary btn-full"
                  onClick={(e) => {
                    e.stopPropagation();
                    onSelectService(svc);
                  }}
                  aria-label={`Proceed to check eligibility for ${svc.title}`}
                >
                  <span>Select & Check Eligibility</span>
                  <span aria-hidden="true">→</span>
                </button>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
