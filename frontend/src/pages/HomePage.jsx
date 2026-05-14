import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../lib/auth';
import { api, formatDate } from '../lib/api';
import { motion } from 'framer-motion';
import { ArrowRight, ArrowUpRight, Crown, Sparkles } from 'lucide-react';
import NumberToken from '../components/LottoBall';
import DigitRow from '../components/DigitRow';

export default function HomePage() {
  const { user } = useAuth();
  const nav = useNavigate();
  const [games, setGames] = useState([]);
  const [recent, setRecent] = useState([]);

  useEffect(() => {
    (async () => {
      const [g, p] = await Promise.all([api.get('/games'), api.get('/picks')]);
      setGames(g.data.games);
      setRecent(p.data.picks.slice(0, 3));
    })();
  }, []);

  const digitGames = games.filter(g => g.type === 'digit');
  const pickGames = games.filter(g => g.type === 'pick');

  return (
    <div className="px-5 pt-12 pb-6" data-testid="home-page">
      {/* Header */}
      <div className="flex items-start justify-between mb-8">
        <div>
          <div className="overline">{new Date().toLocaleDateString('en-MY', { weekday:'long', day:'numeric', month:'short' })}</div>
          <h2 className="display text-3xl mt-1">
            Hello, <span className="text-red">{user?.name}</span>
          </h2>
        </div>
        <Link to="/vip" data-testid="header-vip-link" className="chip red">
          <Crown size={12} /> {user?.is_vip ? 'VIP' : 'Upgrade'}
        </Link>
      </div>

      {/* Hero CTA */}
      <motion.div
        initial={{ opacity:0, y:10 }} animate={{ opacity:1, y:0 }}
        className="card-red p-6 mb-6 relative overflow-hidden"
        data-testid="home-hero-card"
      >
        <div className="overline text-white/70 mb-2">Today's Pick</div>
        <h3 className="display text-3xl text-white leading-tight">Generate lucky numbers in <span className="underline decoration-2 underline-offset-4">2 seconds</span>.</h3>
        <p className="text-white/85 text-sm mt-3 max-w-[260px]">
          Quick Pick is free. AI Lucky Picks use your numerology — birthday, zodiac, lucky numbers.
        </p>
        <button onClick={() => nav('/generate')} className="mt-5 bg-white text-red px-5 py-3 rounded-full font-semibold inline-flex items-center gap-2 text-sm hover:bg-red-50 transition-colors"
          data-testid="home-generate-cta">
          Start picking <ArrowRight size={16} strokeWidth={2.5} />
        </button>
      </motion.div>

      {/* Stats strip */}
      <div className="grid grid-cols-2 gap-3 mb-8">
        <div className="card-min p-4" data-testid="home-credits-card">
          <div className="overline">AI Picks Left</div>
          <div className="display text-4xl mt-2 text-red">{user?.credits ?? 0}</div>
          <Link to="/vip" className="text-[11px] uppercase tracking-widest text-ink-mute hover:text-ink inline-flex items-center mt-2 gap-1">
            Top up <ArrowUpRight size={11} />
          </Link>
        </div>
        <div className="card-min p-4" data-testid="home-vip-card">
          <div className="overline">Status</div>
          <div className="display text-2xl mt-2">{user?.is_vip ? <span className="text-red">VIP</span> : 'Standard'}</div>
          <Link to="/vip" className="text-[11px] uppercase tracking-widest text-ink-mute hover:text-ink inline-flex items-center mt-2 gap-1">
            {user?.is_vip ? 'Manage' : 'Upgrade'} <ArrowUpRight size={11} />
          </Link>
        </div>
      </div>

      {/* Games — Digit (4D/5D/6D) */}
      {digitGames.length > 0 && (
        <div className="mb-8">
          <div className="flex items-center justify-between mb-3">
            <div className="overline">Digit Games</div>
            <span className="text-[11px] text-ink-mute">4D · 5D · 6D</span>
          </div>
          <div className="space-y-3">
            {digitGames.map((g, i) => (
              <motion.button key={g.id}
                onClick={() => nav(`/generate/${g.id}`)}
                initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.04 * i }}
                className="card-min p-4 w-full text-left hover:border-red transition-colors flex items-center justify-between"
                data-testid={`game-selector-${g.id}`}
              >
                <div>
                  <div className="display text-2xl">{g.name}</div>
                  <div className="text-xs text-ink-mute mt-0.5">{g.label} · {g.digits} digits</div>
                </div>
                <div className="chip red">Pick</div>
              </motion.button>
            ))}
          </div>
        </div>
      )}

      {/* Games — Toto */}
      {pickGames.length > 0 && (
        <div className="mb-8">
          <div className="flex items-center justify-between mb-3">
            <div className="overline">Toto Games</div>
            <span className="text-[11px] text-ink-mute">Pick 6 of N</span>
          </div>
          <div className="grid grid-cols-2 gap-3">
            {pickGames.map((g, i) => (
              <motion.button key={g.id}
                onClick={() => nav(`/generate/${g.id}`)}
                initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.04 * i }}
                className="card-min p-4 text-left hover:border-red transition-colors"
                data-testid={`game-selector-${g.id}`}
              >
                <div className="display text-xl">{g.name.replace('Toto ', '').replace(' Toto', '')}</div>
                <div className="text-xs text-ink-mute mt-1">{g.label}</div>
                <div className="text-[10px] text-ink-mute uppercase tracking-widest mt-2">{g.picks} of {g.max}</div>
              </motion.button>
            ))}
          </div>
        </div>
      )}

      {/* Recent */}
      <div className="flex items-center justify-between mb-3">
        <div className="overline">Recent</div>
        <Link to="/history" className="text-[11px] uppercase tracking-widest text-red font-semibold">View all</Link>
      </div>
      <div className="space-y-3" data-testid="home-recent-picks">
        {recent.length === 0 && (
          <div className="card-min p-6 text-center text-ink-mute text-sm">
            No picks yet — generate your first lucky number.
          </div>
        )}
        {recent.map(p => (
          <div key={p.id} className="card-min p-4">
            <div className="flex items-center justify-between mb-2">
              <div className="text-sm font-semibold">{p.game_name}</div>
              <div className={`chip ${p.mode === 'ai' ? 'red' : ''}`}>
                {p.mode === 'ai' ? <><Sparkles size={10} /> AI</> : 'Quick'}
              </div>
            </div>
            {p.game_type === 'digit' && p.digit_sequence ? (
              <DigitRow length={p.digit_sequence.length} value={p.digit_sequence} size="sm" />
            ) : (
              <div className="flex flex-wrap gap-1.5">
                {p.numbers.map((n, idx) => <NumberToken key={idx} n={n} idx={idx} size="sm" />)}
              </div>
            )}
            <div className="text-[10px] text-ink-mute mt-2.5 uppercase tracking-widest">{formatDate(p.created_at)}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
