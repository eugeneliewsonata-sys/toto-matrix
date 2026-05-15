import React, { useState } from 'react';
import { useAuth } from '../lib/auth';
import { toast } from 'sonner';
import { motion } from 'framer-motion';
import { ArrowRight } from 'lucide-react';

export default function AuthPage() {
  const { login, register } = useAuth();
  const [mode, setMode] = useState('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [busy, setBusy] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    if (busy) return;
    setBusy(true);
    try {
      if (mode === 'login') {
        await login(email.trim(), password);
        toast.success('Welcome back.');
      } else {
        await register(email.trim(), password, name.trim() || null);
        toast.success('Account created. You have 3 free AI picks.');
      }
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Something went wrong');
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="min-h-screen px-6 pt-20 pb-10 flex flex-col" data-testid="auth-page">
      {/* Brand mark */}
      <motion.div initial={{ opacity:0, y:8 }} animate={{ opacity:1, y:0 }} transition={{ duration:0.4 }}>
        <div className="flex items-center gap-2.5">
          <div className="w-9 h-9 rounded-full bg-red"></div>
          <h1 className="display text-4xl">HuatPick</h1>
        </div>
        <div className="overline mt-3">Malaysia Lottery · AI</div>
      </motion.div>

      <motion.p initial={{ opacity:0, y:8 }} animate={{ opacity:1, y:0 }} transition={{ duration:0.5, delay:0.08 }}
        className="text-ink mt-8 text-2xl leading-snug max-w-[300px]">
        Pick your lucky numbers with <span className="text-red">a little math</span> and a lot of intuition.
      </motion.p>

      <motion.form
        onSubmit={submit}
        initial={{ opacity:0, y:12 }} animate={{ opacity:1, y:0 }} transition={{ duration:0.5, delay:0.16 }}
        className="mt-12 space-y-4"
      >
        {/* Segmented control */}
        <div className="flex bg-[#F4F4F5] rounded-full p-1 mb-6">
          <button type="button" onClick={() => setMode('login')}
            data-testid="tab-login"
            className={`flex-1 py-2.5 text-xs uppercase tracking-widest rounded-full transition-all ${mode==='login' ? 'bg-white text-ink shadow-sm' : 'text-ink-mute'}`}>
            Sign In
          </button>
          <button type="button" onClick={() => setMode('register')}
            data-testid="tab-register"
            className={`flex-1 py-2.5 text-xs uppercase tracking-widest rounded-full transition-all ${mode==='register' ? 'bg-white text-ink shadow-sm' : 'text-ink-mute'}`}>
            Register
          </button>
        </div>

        {mode === 'register' && (
          <div>
            <label className="overline block mb-1.5">Name</label>
            <input className="input-min" placeholder="Your name"
              value={name} onChange={e=>setName(e.target.value)} data-testid="register-name-input" />
          </div>
        )}

        <div>
          <label className="overline block mb-1.5">Email</label>
          <input className="input-min" type="email" required placeholder="you@email.com"
            value={email} onChange={e=>setEmail(e.target.value)} data-testid="login-email-input" autoComplete="email" />
        </div>

        <div>
          <label className="overline block mb-1.5">Password</label>
          <input className="input-min" type="password" required minLength={6} placeholder="At least 6 characters"
            value={password} onChange={e=>setPassword(e.target.value)} data-testid="login-password-input" autoComplete={mode==='login'?'current-password':'new-password'} />
        </div>

        <button type="submit" disabled={busy} className="btn-red w-full flex items-center justify-center gap-2 mt-2"
          data-testid="login-submit-button">
          {busy ? 'Please wait…' : (mode === 'login' ? 'Sign In' : 'Create Account')}
          {!busy && <ArrowRight size={16} strokeWidth={2.5} />}
        </button>

        <p className="text-center text-[11px] text-ink-mute pt-2">
          For entertainment only. Play responsibly.<br />
          By continuing you agree to our{' '}
          <a href="/terms" className="text-red underline" data-testid="auth-terms-link">Terms</a>
          {' & '}
          <a href="/privacy" className="text-red underline" data-testid="auth-privacy-link">Privacy Policy</a>.
        </p>
      </motion.form>
    </div>
  );
}
