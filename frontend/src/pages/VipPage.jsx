import React, { useEffect, useState } from 'react';
import { api } from '../lib/api';
import { useAuth } from '../lib/auth';
import { toast } from 'sonner';
import { Crown, Check, Sparkles, Star, Infinity as InfinityIcon, ArrowRight } from 'lucide-react';

const ICONS = {
  premium_pick: Sparkles,
  credits_10: Star,
  vip_monthly: InfinityIcon,
};

export default function VipPage() {
  const { user } = useAuth();
  const [packages, setPackages] = useState([]);
  const [selected, setSelected] = useState('vip_monthly');
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    (async () => {
      const r = await api.get('/packages');
      setPackages(r.data.packages);
    })();
  }, []);

  const checkout = async () => {
    if (busy) return;
    setBusy(true);
    try {
      const origin_url = window.location.origin;
      const r = await api.post('/payments/checkout', { package_id: selected, origin_url });
      window.location.href = r.data.url;
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Checkout failed');
      setBusy(false);
    }
  };

  const benefits = [
    'Unlimited AI Lucky Picks',
    'Hot & Cold number analysis',
    'Personalized numerology',
    'Priority generation',
    'No ads, ever',
  ];

  return (
    <div className="px-5 pt-12 pb-6" data-testid="vip-page">
      <div className="text-center mb-6">
        <div className="w-14 h-14 rounded-full mx-auto bg-red text-white flex items-center justify-center" data-testid="vip-crown">
          <Crown size={22} strokeWidth={2.2} />
        </div>
        <div className="overline mt-4">Members only</div>
        <h1 className="display text-4xl mt-1">Become <span className="text-red">VIP</span></h1>
        <p className="text-ink-mute text-sm mt-3 max-w-[280px] mx-auto leading-relaxed">
          Unlimited AI-powered picks, hot/cold analysis, and priority access.
        </p>
      </div>

      {/* Benefits */}
      <div className="card-min p-5 mb-6">
        <ul className="space-y-3">
          {benefits.map(b => (
            <li key={b} className="flex items-start gap-3 text-sm">
              <div className="w-5 h-5 rounded-full bg-red text-white flex items-center justify-center flex-shrink-0 mt-0.5">
                <Check size={12} strokeWidth={3} />
              </div>
              <span className="text-ink">{b}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Tiers */}
      <div className="space-y-3 mb-6">
        {packages.map(p => {
          const Icon = ICONS[p.id] || Sparkles;
          const isSelected = selected === p.id;
          const isBest = p.id === 'vip_monthly';
          return (
            <button
              key={p.id}
              onClick={() => setSelected(p.id)}
              data-testid={`vip-tier-${p.id}`}
              className={`w-full text-left rounded-2xl p-4 transition-all relative border ${
                isSelected ? 'border-red bg-red-50' : 'border-ink-line bg-white hover:border-ink-mute'
              }`}
            >
              {isBest && (
                <div className="absolute -top-2 right-4 bg-red text-white text-[10px] uppercase tracking-widest px-2 py-0.5 rounded-full font-semibold">
                  Best Value
                </div>
              )}
              <div className="flex items-center gap-3">
                <div className={`w-10 h-10 rounded-full flex items-center justify-center ${isSelected ? 'bg-red text-white' : 'bg-[#F4F4F5] text-ink'}`}>
                  <Icon size={18} />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="font-semibold text-base">{p.name}</div>
                  <div className="text-[10px] text-ink-mute uppercase tracking-widest mt-0.5">
                    {p.type === 'subscription' ? `${p.days} day membership` : `${p.credits} AI pick${p.credits>1?'s':''}`}
                  </div>
                </div>
                <div className="text-right">
                  <div className="display text-xl">RM {Number(p.amount).toFixed(2)}</div>
                </div>
              </div>
            </button>
          );
        })}
      </div>

      <button onClick={checkout} disabled={busy || !selected} className="btn-red w-full flex items-center justify-center gap-2 sticky bottom-28 shadow-[0_8px_24px_rgba(220,38,38,0.25)]" data-testid="checkout-stripe-button">
        {busy ? 'Loading…' : <>Continue to Checkout <ArrowRight size={16} strokeWidth={2.5} /></>}
      </button>

      <p className="text-[11px] text-ink-mute text-center mt-3">
        Powered by Stripe. {user?.is_vip ? 'Stack additional days onto your VIP membership.' : 'Cancel anytime.'}
      </p>
    </div>
  );
}
