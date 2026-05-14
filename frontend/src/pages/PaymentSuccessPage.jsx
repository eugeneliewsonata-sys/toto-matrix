import React, { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { api } from '../lib/api';
import { useAuth } from '../lib/auth';
import { CheckCircle2, RotateCw, X } from 'lucide-react';

export default function PaymentSuccessPage() {
  const [sp] = useSearchParams();
  const nav = useNavigate();
  const { refresh } = useAuth();
  const sessionId = sp.get('session_id');
  const [status, setStatus] = useState('checking');

  useEffect(() => {
    if (!sessionId) { setStatus('error'); return; }

    let cancelled = false;
    let attempts = 0;
    const MAX = 10;

    const poll = async () => {
      attempts++;
      try {
        const r = await api.get(`/payments/status/${sessionId}`);
        if (cancelled) return;
        if (r.data.payment_status === 'paid') {
          setStatus('paid');
          await refresh();
          return;
        }
        if (r.data.status === 'expired') { setStatus('expired'); return; }
        if (attempts >= MAX) { setStatus('timeout'); return; }
        setTimeout(poll, 2000);
      } catch {
        if (attempts >= MAX) { setStatus('error'); return; }
        setTimeout(poll, 2000);
      }
    };
    poll();
    return () => { cancelled = true; };
  }, [sessionId, refresh]);

  return (
    <div className="px-6 pt-24 pb-10 text-center" data-testid="payment-success-page">
      {status === 'checking' && (
        <>
          <RotateCw className="mx-auto text-red animate-spin" size={36} />
          <h1 className="display text-2xl mt-6">Confirming your payment…</h1>
          <p className="text-ink-mute text-sm mt-2">This usually takes a few seconds.</p>
        </>
      )}
      {status === 'paid' && (
        <>
          <div className="w-16 h-16 rounded-full bg-red text-white inline-flex items-center justify-center mx-auto">
            <CheckCircle2 size={32} strokeWidth={2.2} />
          </div>
          <h1 className="display text-3xl mt-6">You're <span className="text-red">in</span>.</h1>
          <p className="text-ink-mute text-sm mt-3">Your purchase has been credited.</p>
          <button onClick={() => nav('/generate')} className="btn-red mt-8" data-testid="post-pay-generate">Start picking</button>
          <button onClick={() => nav('/profile')} className="block mx-auto mt-4 text-ink-mute underline text-xs" data-testid="post-pay-profile">View Profile</button>
        </>
      )}
      {(status === 'expired' || status === 'error' || status === 'timeout') && (
        <>
          <div className="w-16 h-16 rounded-full bg-[#F4F4F5] text-red inline-flex items-center justify-center mx-auto">
            <X size={32} />
          </div>
          <h1 className="display text-2xl mt-6">Payment {status === 'expired' ? 'expired' : 'unverified'}</h1>
          <p className="text-ink-mute text-sm mt-3">No charge was made. Please try again from the VIP page.</p>
          <button onClick={() => nav('/vip')} className="btn-outline mt-8">Back to VIP</button>
        </>
      )}
    </div>
  );
}
