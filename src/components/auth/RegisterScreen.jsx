import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

export default function RegisterScreen() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { signup } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    setLoading(true);

    try {
      await signup(email, password);
      navigate('/');
    } catch (err) {
      setError(err.message || 'Failed to create account');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 420, margin: '4rem auto', padding: '2rem', background: '#fff', borderRadius: 12 }}>
      <h2 style={{ marginBottom: '1rem' }}>Create your account</h2>
      <p style={{ color: '#475569', marginBottom: '1.5rem' }}>Register to save your certificates and checklist progress.</p>

      <form onSubmit={handleSubmit}>
        {error && <p style={{ color: '#b91c1c', marginBottom: '1rem' }}>{error}</p>}

        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="register-email" style={{ display: 'block', marginBottom: '0.4rem' }}>Email</label>
          <input
            id="register-email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            style={{ width: '100%', padding: '0.75rem', borderRadius: 8, border: '1px solid #cbd5e1' }}
          />
        </div>

        <div style={{ marginBottom: '1rem' }}>
          <label htmlFor="register-password" style={{ display: 'block', marginBottom: '0.4rem' }}>Password</label>
          <input
            id="register-password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={6}
            style={{ width: '100%', padding: '0.75rem', borderRadius: 8, border: '1px solid #cbd5e1' }}
          />
        </div>

        <button type="submit" disabled={loading} style={{ width: '100%', padding: '0.8rem', borderRadius: 8, background: '#2563eb', color: '#fff', border: 'none' }}>
          {loading ? 'Creating account...' : 'Sign Up'}
        </button>
      </form>

      <p style={{ marginTop: '1rem', textAlign: 'center' }}>
        Already have an account? <Link to="/login">Log in</Link>
      </p>
    </div>
  );
}
