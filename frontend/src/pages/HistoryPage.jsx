import React, { useEffect, useState } from 'react';
import { api, formatDate } from '../lib/api';
import NumberToken from '../components/LottoBall';
import DigitRow from '../components/DigitRow';
import { Sparkles } from 'lucide-react';

export default function HistoryPage() {
  const [picks, setPicks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      const r = await api.get('/picks');
      setPicks(r.data.picks);
      setLoading(false);
    })();
  }, []);

  return (
    <div className="px-5 pt-12 pb-6" data-testid="history-page">
      <div className="overline">Your Ledger</div>
      <h2 className="display text-3xl mb-6">History</h2>

      {loading && <div className="text-ink-mute text-sm">Loading…</div>}
      {!loading && picks.length === 0 && (
        <div className="card-min p-8 text-center text-ink-mute text-sm">
          No picks yet. Generate your first lucky number from the Pick tab.
        </div>
      )}

      <div className="space-y-3">
        {picks.map((p, idx) => (
          <div key={p.id} className="card-min p-4" data-testid={`history-list-item-${idx}`}>
            <div className="flex items-center justify-between mb-3">
              <div>
                <div className="font-semibold text-sm">{p.game_name}</div>
                <div className="text-[10px] text-ink-mute uppercase tracking-widest mt-0.5">{formatDate(p.created_at)}</div>
              </div>
              <div className={`chip ${p.mode === 'ai' ? 'red' : ''}`}>
                {p.mode === 'ai' ? <><Sparkles size={10} /> AI</> : 'Quick'}
              </div>
            </div>
            {p.game_type === 'digit' && p.digit_sequence ? (
              <DigitRow length={p.digit_sequence.length} value={p.digit_sequence} size="sm" />
            ) : (
              <div className="flex flex-wrap gap-1.5">
                {p.numbers.map((n, i) => <NumberToken key={i} n={n} idx={i} size="sm" />)}
              </div>
            )}
            {p.mode === 'ai' && p.reasoning && (
              <p className="text-xs text-ink-mute italic mt-3">"{p.reasoning}"</p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
