import React, { useEffect, useState } from 'react';
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';

import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';
import RegisterScreen from './components/auth/RegisterScreen';
import LoginScreen from './components/auth/LoginScreen';
import ProgressIndicator from './components/ProgressIndicator';
import HomeScreen from './components/screens/HomeScreen';
import QuestionsScreen from './components/screens/QuestionsScreen';
import ChecklistScreen from './components/screens/ChecklistScreen';
import ApplyScreen from './components/screens/ApplyScreen';
import { AuthProvider, useAuth } from './context/AuthContext';

const DEFAULT_SERVICES = [
  {
    slug: 'income-certificate',
    title: 'Income Certificate (आय प्रमाण पत्र)',
    short_description: 'Official proof of annual household income for scholarship, fee concession, and welfare benefits.',
    overview: 'Certifies total annual income from all sources. Essential for university scholarships, EWS quota, fee waivers, and state subsidies.',
    category: 'Revenue & Welfare',
    department: 'Revenue Department (Tehsildar / Sub-Divisional Magistrate)',
    validity_period: '1 Financial Year (April 1 to March 31)',
    estimated_processing_days: 10,
    fee: { amount: 30.0, currency: 'INR' },
    official_portal_url: 'https://serviceonline.gov.in',
    eligibility_criteria: ['Applicant or family must be resident in the Tehsil jurisdiction.', 'Income from all family members must be declared transparently.', 'Must possess primary proof of identity and local address.'],
    tags: ['income', 'scholarship', 'ews', 'revenue'],
  },
  {
    slug: 'caste-certificate',
    title: 'Caste Certificate (जाति प्रमाण पत्र)',
    short_description: 'Statutory certificate establishing SC, ST, OBC, or SEBC category status for reservation and scheme benefits.',
    overview: 'Definitive proof of belonging to a reserved community under Presidential orders. Required for educational quotas and government recruitment.',
    category: 'Social Justice & Empowerment',
    department: 'District Administration / Revenue Department (SDM / Tehsildar)',
    validity_period: 'Lifetime (SC/ST); Annual / Subject to Creamy Layer (OBC)',
    estimated_processing_days: 15,
    fee: { amount: 30.0, currency: 'INR' },
    official_portal_url: 'https://serviceonline.gov.in',
    eligibility_criteria: ['Applicant must belong to a community notified in the Presidential gazette.', 'Paternal lineage proof (father/grandfather document) is mandatory.', 'For OBC Non-Creamy Layer, annual family income must be under ₹8 Lakh.'],
    tags: ['caste', 'reservation', 'obc', 'sc', 'st'],
  },
  {
    slug: 'residence-certificate',
    title: 'Residence / Domicile Certificate (मूल निवास प्रमाण पत्र)',
    short_description: 'Official proof of permanent residence or domicile within a specific State or Union Territory.',
    overview: 'Establishes continuous long-term residence within the state. Mandatory for state-quota college seats and civil services recruitment.',
    category: 'Revenue & General Administration',
    department: 'Revenue Department (Tehsildar / District Magistrate)',
    validity_period: 'Lifetime (unless domicile is permanently shifted)',
    estimated_processing_days: 14,
    fee: { amount: 35.0, currency: 'INR' },
    official_portal_url: 'https://serviceonline.gov.in',
    eligibility_criteria: ['Continuous residence in the state for minimum period mandated by state law (typically 3 to 15 years).', 'Or proof of owning ancestral land/property in the state.', 'Or born in the state with continuous schooling in the state.'],
    tags: ['domicile', 'residence', 'state-quota', 'admissions'],
  },
];

function CitizenApp() {
  const { user, getIdToken } = useAuth();
  const [currentStep, setCurrentStep] = useState(1);
  const [services, setServices] = useState(DEFAULT_SERVICES);
  const [selectedService, setSelectedService] = useState(null);
  const [checklist, setChecklist] = useState(null);
  const [checkedDocs, setCheckedDocs] = useState({});
  const [loading, setLoading] = useState(false);
  const [theme, setTheme] = useState(() => localStorage.getItem('sevaguide_theme') || 'light');
  const [fontScale, setFontScale] = useState(() => localStorage.getItem('sevaguide_font') || 'normal');

  const apiFetch = async (url, options = {}) => {
    const token = await getIdToken();
    const headers = { ...(options.headers || {}) };
    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }
    if (!(options.body instanceof FormData)) {
      headers['Content-Type'] = headers['Content-Type'] || 'application/json';
    }

    return fetch(url, {
      ...options,
      headers,
    });
  };

  const saveChecklistToBackend = async (nextDocs = checkedDocs) => {
    if (!selectedService || !user || !checklist) {
      return;
    }

    try {
      await apiFetch(`/api/v1/checklists/me/${selectedService.slug}`, {
        method: 'POST',
        body: JSON.stringify({
          service_slug: selectedService.slug,
          service_title: selectedService.title,
          checked_docs: nextDocs,
          documents_required: checklist.documents_required || [],
          updated_at: new Date().toISOString(),
        }),
      });
    } catch (error) {
      console.warn('Could not save checklist to backend:', error);
    }
  };

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('sevaguide_theme', theme);
  }, [theme]);

  useEffect(() => {
    document.body.classList.remove('text-large', 'text-xlarge');
    if (fontScale === 'large') document.body.classList.add('text-large');
    if (fontScale === 'xlarge') document.body.classList.add('text-xlarge');
    localStorage.setItem('sevaguide_font', fontScale);
  }, [fontScale]);

  useEffect(() => {
    if (!user) return;

    async function fetchServices() {
      setLoading(true);
      try {
        const res = await apiFetch('/api/v1/services');
        if (res.ok) {
          const data = await res.json();
          if (Array.isArray(data) && data.length > 0) {
            setServices(data);
          }
        }
      } catch (error) {
        console.warn('Backend offline or proxy unreachable, using initial service dataset:', error);
      } finally {
        setLoading(false);
      }
    }

    fetchServices();
  }, [user]);

  useEffect(() => {
    if (!selectedService || !user) return;

    async function loadSavedChecklist() {
      try {
        const res = await apiFetch(`/api/v1/checklists/me/${selectedService.slug}`);
        if (res.ok) {
          const data = await res.json();
          const saved = data?.checked_docs || {};
          if (saved && Object.keys(saved).length > 0) {
            setCheckedDocs(saved);
          }
        }
      } catch (error) {
        console.warn('No saved checklist found for this user.', error);
      }
    }

    loadSavedChecklist();
  }, [selectedService, user]);

  const handleSelectService = async (service) => {
    setSelectedService(service);
    setCheckedDocs({});

    try {
      const res = await apiFetch(`/api/v1/services/${service.slug}/checklist`);
      if (res.ok) {
        const data = await res.json();
        setChecklist(data);
      }
    } catch (error) {
      console.warn('Could not fetch checklist from backend, using default data:', error);
    }

    setCurrentStep(2);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleStepClick = (stepId) => {
    if (stepId === 1 || selectedService) {
      setCurrentStep(stepId);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const handleToggleDoc = (docName) => {
    setCheckedDocs((prev) => {
      const next = {
        ...prev,
        [docName]: !prev[docName],
      };
      saveChecklistToBackend(next);
      return next;
    });
  };

  const handleMarkAllDocs = () => {
    if (!checklist?.documents_required) return;
    const all = {};
    checklist.documents_required.forEach((document) => {
      all[document.document_name] = true;
    });
    setCheckedDocs(all);
    saveChecklistToBackend(all);
  };

  const handleResetDocs = () => {
    setCheckedDocs({});
    saveChecklistToBackend({});
  };

  const handleResetApp = () => {
    setSelectedService(null);
    setChecklist(null);
    setCheckedDocs({});
    setCurrentStep(1);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const toggleTheme = () => {
    setTheme((prev) => (prev === 'light' ? 'dark' : 'light'));
  };

  const cycleFontScale = () => {
    setFontScale((prev) => {
      if (prev === 'normal') return 'large';
      if (prev === 'large') return 'xlarge';
      return 'normal';
    });
  };

  return (
    <div className="app-layout">
      <Navbar
        currentStep={currentStep}
        onReset={handleResetApp}
        theme={theme}
        onToggleTheme={toggleTheme}
        fontScale={fontScale}
        onChangeFontScale={cycleFontScale}
      />

      <ProgressIndicator
        currentStep={currentStep}
        onStepClick={handleStepClick}
        hasSelectedService={!!selectedService}
      />

      <main className="main-wrapper" id="main-content" tabIndex={-1}>
        {currentStep === 1 && (
          <HomeScreen
            services={services}
            selectedService={selectedService}
            onSelectService={handleSelectService}
            loading={loading}
          />
        )}

        {currentStep === 2 && (
          <QuestionsScreen
            service={selectedService}
            checklist={checklist}
            onBack={() => handleStepClick(1)}
            onNext={() => handleStepClick(3)}
          />
        )}

        {currentStep === 3 && (
          <ChecklistScreen
            service={selectedService}
            checklist={checklist}
            checkedDocs={checkedDocs}
            onToggleDoc={handleToggleDoc}
            onMarkAllDocs={handleMarkAllDocs}
            onResetDocs={handleResetDocs}
            onBack={() => handleStepClick(2)}
            onNext={() => handleStepClick(4)}
          />
        )}

        {currentStep === 4 && (
          <ApplyScreen
            service={selectedService}
            checklist={checklist}
            onBack={() => handleStepClick(3)}
          />
        )}
      </main>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginScreen />} />
          <Route path="/register" element={<RegisterScreen />} />
          <Route
            path="*"
            element={
              <ProtectedRoute>
                <CitizenApp />
              </ProtectedRoute>
            }
          />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
