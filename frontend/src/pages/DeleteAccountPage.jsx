import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ArrowLeft, AlertTriangle, Trash2, Mail, CheckCircle2 } from 'lucide-react';
import { toast } from 'sonner';
import { api } from '../lib/api';
import { useAuth } from '../lib/auth';

const COMPANY = 'JH Creative Enterprise';
const APP = 'HuatPick';
const CONTACT = 'turyoungpotato@gmail.com';

export default function DeleteAccountPage() {
  const { user, logout } = useAuth();
  const nav = useNavigate();

  // Logged-in deletion state
  const [confirmText, setConfirmText] = useState('');
  const [deleting, setDeleting] = useState(false);

  // Public request state
  const [email, setEmail] = useState('');
  const [reason, setReason] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const handleDeleteNow = async () => {
    if (confirmText.trim().toUpperCase() !== 'DELETE') {
      toast.error('Type DELETE to confirm');
      return;
    }
    setDeleting(true);
    try {
      await api.delete('/auth/account');
      toast.success('Your account has been deleted');
      logout();
      setTimeout(() => nav('/auth', { replace: true }), 600);
    } catch (e) {
      toast.error(e?.response?.data?.detail || 'Could not delete account. Please try again.');
    } finally {
      setDeleting(false);
    }
  };

  const handleRequestDeletion = async (e) => {
    e.preventDefault();
    if (!email) {
      toast.error('Enter your account email');
      return;
    }
    setSubmitting(true);
    try {
      await api.post('/auth/account/request-deletion', { email, reason });
      setSubmitted(true);
      toast.success('Deletion request received');
    } catch (err) {
      toast.error(err?.response?.data?.detail || 'Could not submit request. Please email us.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="px-5 pt-12 pb-16 text-ink" data-testid="delete-account-page">
      <Link to={user ? '/profile' : '/auth'} className="inline-flex items-center gap-2 text-ink-mute hover:text-ink mb-6 text-sm" data-testid="delete-account-back">
        <ArrowLeft size={16} /> Back
      </Link>

      <div className="overline">Account · Data Removal</div>
      <h1 className="display text-3xl mt-2 mb-2">Delete <span className="text-red">Account</span></h1>
      <p className="text-sm text-ink-mute mb-6 leading-relaxed">
        Permanently delete your <strong>{APP}</strong> account and all associated personal data.
        This action is <strong>irreversible</strong>.
      </p>

      {/* What gets deleted */}
      <div className="card-min p-5 mb-6">
        <h2 className="font-semibold text-sm mb-3 inline-flex items-center gap-2">
          <Trash2 size={15} className="text-red" /> What gets deleted
        </h2>
        <ul className="space-y-2 text-sm text-ink leading-relaxed">
          <li className="flex gap-2"><span className="text-red flex-shrink-0">·</span><span>Your account: email, name, password hash, user ID</span></li>
          <li className="flex gap-2"><span className="text-red flex-shrink-0">·</span><span>Your full pick history (all generated lottery numbers)</span></li>
          <li className="flex gap-2"><span className="text-red flex-shrink-0">·</span><span>Your VIP/credits balance &amp; any active subscription link</span></li>
          <li className="flex gap-2"><span className="text-red flex-shrink-0">·</span><span>Any AI inputs you provided (birthday, zodiac, lucky numbers)</span></li>
        </ul>
        <h2 className="font-semibold text-sm mt-5 mb-2">What is retained</h2>
        <p className="text-sm text-ink-mute leading-relaxed">
          Payment records (amount, date, Stripe session ID) are kept <strong>anonymised</strong> (without
          your email or user ID) for <strong>7 years</strong> to comply with Malaysian accounting law,
          as disclosed in our <Link to="/privacy" className="text-red underline">Privacy Policy</Link>.
        </p>
      </div>

      {/* Logged-in: immediate deletion */}
      {user ? (
        <div className="card-min p-5 mb-6 border-red/30" data-testid="logged-in-delete-block">
          <div className="flex items-start gap-2 mb-3">
            <AlertTriangle size={18} className="text-red flex-shrink-0 mt-0.5" />
            <div>
              <h2 className="font-semibold text-sm">You are signed in as <span className="text-red">{user.email}</span></h2>
              <p className="text-xs text-ink-mute mt-1 leading-relaxed">
                Clicking the button below will delete your account immediately. You will be signed out
                and unable to recover any data. To confirm, type <strong>DELETE</strong> below.
              </p>
            </div>
          </div>
          <input
            type="text"
            value={confirmText}
            onChange={(e) => setConfirmText(e.target.value)}
            placeholder="Type DELETE to confirm"
            className="w-full px-3 py-2.5 rounded-lg border border-[#E5E5E5] focus:border-red focus:outline-none text-sm mb-3"
            data-testid="delete-confirm-input"
          />
          <button
            onClick={handleDeleteNow}
            disabled={deleting || confirmText.trim().toUpperCase() !== 'DELETE'}
            className="w-full bg-red text-white font-semibold py-3 rounded-lg disabled:opacity-40 disabled:cursor-not-allowed hover:bg-red/90 transition-colors inline-flex items-center justify-center gap-2"
            data-testid="delete-account-now-btn"
          >
            <Trash2 size={15} /> {deleting ? 'Deleting…' : 'Delete my account now'}
          </button>
        </div>
      ) : (
        // Public: request via email
        <div className="card-min p-5 mb-6" data-testid="public-delete-block">
          <h2 className="font-semibold text-sm mb-1 inline-flex items-center gap-2">
            <Mail size={15} className="text-red" /> Request deletion by email
          </h2>
          <p className="text-xs text-ink-mute mb-4 leading-relaxed">
            Don't have access to your account? Submit the email you registered with and we'll permanently
            remove all data within <strong>30 days</strong>. If you can log in,{' '}
            <Link to="/auth" className="text-red underline">sign in</Link> for instant deletion.
          </p>

          {submitted ? (
            <div className="bg-[#F8F8F8] rounded-lg p-4 text-center" data-testid="deletion-submitted">
              <CheckCircle2 size={28} className="text-red mx-auto mb-2" />
              <div className="font-semibold text-sm mb-1">Request received</div>
              <p className="text-xs text-ink-mute leading-relaxed">
                We will permanently remove all data associated with <strong>{email}</strong> within 30 days
                and email confirmation to that address.
              </p>
            </div>
          ) : (
            <form onSubmit={handleRequestDeletion} className="space-y-3">
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="your@email.com"
                required
                className="w-full px-3 py-2.5 rounded-lg border border-[#E5E5E5] focus:border-red focus:outline-none text-sm"
                data-testid="deletion-email-input"
              />
              <textarea
                value={reason}
                onChange={(e) => setReason(e.target.value)}
                placeholder="Reason (optional)"
                rows={3}
                maxLength={500}
                className="w-full px-3 py-2.5 rounded-lg border border-[#E5E5E5] focus:border-red focus:outline-none text-sm resize-none"
                data-testid="deletion-reason-input"
              />
              <button
                type="submit"
                disabled={submitting}
                className="w-full bg-red text-white font-semibold py-3 rounded-lg disabled:opacity-40 hover:bg-red/90 transition-colors"
                data-testid="deletion-submit-btn"
              >
                {submitting ? 'Submitting…' : 'Submit deletion request'}
              </button>
            </form>
          )}
        </div>
      )}

      <p className="text-[11px] text-ink-mute text-center leading-relaxed">
        Operated by {COMPANY}. Questions? Email{' '}
        <a className="text-red underline" href={`mailto:${CONTACT}`}>{CONTACT}</a>.<br />
        See our <Link to="/privacy" className="text-red underline">Privacy Policy</Link> for full details
        on data handling.
      </p>
    </div>
  );
}
