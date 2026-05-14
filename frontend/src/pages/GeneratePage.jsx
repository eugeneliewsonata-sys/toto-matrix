import React, { useEffect, useState, useMemo } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { api, ZODIACS } from '../lib/api';
import { useAuth } from '../lib/auth';
import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles, Crown, Wand2, X, RotateCw, ArrowLeft } from 'lucide-react';
import NumberToken from '../components/LottoBall';
import DigitRow from '../components/DigitRow';
import Select from '../components/Select';
import { toast } from 'sonner';

export default function GeneratePage() {
  const { gameId } = useParams();
  const nav = useNavigate();
  const { user, setUser } = useAuth();
  const [games, setGames] = useState([]);
  const [game, setGame] = useState(null);
  const [tab, setTab] = useState('quick');
  const [spinning, setSpinning] = useState(false);
  const [result, setResult] = useState(null);

  const [birthday, setBirthday] = useState('');
  const [zodiac, setZodiac] = useState('');
  const [lucky, setLucky] = useState('');

  useEffect(() => {
    (async () => {
      const r = await api.get('/games');
      setGames(r.data.games);
      const initial = gameId ? r.data.games.find(g => g.id === gameId) : r.data.games[0];
      setGame(initial || r.data.games[0]);
    })();
  }, [gameId]);

  const aiInputsValid = useMemo(() => {
    if (tab !== 'ai') return true;
    const luckyArr = lucky.split(',').map(s => parseInt(s.trim(), 10)).filter(n => !isNaN(n));
    return Boolean(birthday) || Boolean(zodiac) || luckyArr.length > 0;
  }, [tab, birthday, zodiac, lucky]);

  const spin = async () => {
    if (!game) return;
    if (tab === 'ai' && !aiInputsValid) {
      toast.error('Please provide at least one: birthday, zodiac, or your lucky numbers.');
      return;
    }
    setSpinning(true);
    setResult(null);

    try {
      const payload = { game_id: game.id, mode: tab };
      if (tab === 'ai') {
        payload.birthday = birthday || null;
        payload.zodiac = zodiac || null;
        payload.lucky_numbers = lucky.split(',').map(s => parseInt(s.trim(), 10)).filter(n => !isNaN(n)).slice(0, 6);
      }
      const [resp] = await Promise.all([
        api.post('/generate', payload),
        new Promise(res => setTimeout(res, tab === 'ai' ? 1600 : 1200)),
      ]);
      setResult(resp.data.pick);
      setUser(resp.data.user);
      setTimeout(() => setSpinning(false), 400);
    } catch (err) {
      setSpinning(false);
      const code = err.response?.status;
      const msg = err.response?.data?.detail || 'Generation failed';
      if (code === 402) {
        toast.error(msg);
        nav('/vip');
      } else {
        toast.error(msg);
      }
    }
  };

  const closeResult = () => setResult(null);

  if (!game) return null;

  const isDigitGame = game.type === 'digit';

  return (
    <div className="px-5 pt-12 pb-6 relative" data-testid="generate-page">
      <div className="flex items-center justify-between mb-6">
        <button onClick={() => nav('/')} className="text-ink-mute hover:text-ink" aria-label="Back" data-testid="back-button">
          <ArrowLeft size={20} />
        </button>
        <div className="text-center">
          <div className="overline">Number Pick</div>
          <div className="font-semibold text-sm mt-0.5">{game.name}</div>
        </div>
        <div className="w-5" />
      </div>

      {/* Game switcher chips */}
      <div className="flex gap-2 overflow-x-auto pb-2 mb-5 -mx-1 px-1 scroll-smooth" data-testid="game-chips">
        {games.map(g => (
          <button key={g.id}
            onClick={() => setGame(g)}
            data-testid={`game-chip-${g.id}`}
            className={`flex-shrink-0 px-4 py-2 rounded-full text-xs uppercase tracking-widest border transition-colors ${
              game.id === g.id ? 'bg-ink text-white border-ink' : 'border-ink-line text-ink-mute hover:text-ink'
            }`}>
            {g.name}
          </button>
        ))}
      </div>

      {/* Tabs Quick vs AI */}
      <div className="flex bg-[#F4F4F5] rounded-full p-1 mb-6">
        <button onClick={() => setTab('quick')} data-testid="tab-quick-pick"
          className={`flex-1 py-2.5 text-xs uppercase tracking-widest rounded-full flex items-center justify-center gap-1.5 transition-all ${tab==='quick' ? 'bg-white text-ink shadow-sm' : 'text-ink-mute'}`}>
          Quick Pick
        </button>
        <button onClick={() => setTab('ai')} data-testid="tab-ai-premium"
          className={`flex-1 py-2.5 text-xs uppercase tracking-widest rounded-full flex items-center justify-center gap-1.5 transition-all ${tab==='ai' ? 'bg-red text-white' : 'text-red'}`}>
          <Crown size={12} /> AI Lucky
        </button>
      </div>

      {/* Display stage */}
      <div className="card-min p-5 mb-6" data-testid="display-stage">
        <div className="overline mb-3 text-center">
          {isDigitGame ? `Your ${game.digits}-digit number` : `${game.picks} numbers from 1 – ${game.max}`}
        </div>

        {isDigitGame ? (
          <DigitRow
            length={game.digits}
            value={result?.digit_sequence || null}
            spinning={spinning && !result}
            size="lg"
          />
        ) : (
          <div className="flex flex-wrap justify-center gap-2 py-3 min-h-[64px]">
            {(result?.numbers || Array.from({ length: game.picks }, () => null)).map((n, i) =>
              n != null
                ? <NumberToken key={i} n={n} idx={i} />
                : <div key={i} className={`num-token outline ${spinning ? 'animate-pulse' : ''}`} style={{ opacity: 0.5 }}>
                    <span className="text-xs">·</span>
                  </div>
            )}
          </div>
        )}
      </div>

      {/* Inputs / Action */}
      {tab === 'ai' ? (
        <div className="space-y-3 mb-6">
          <div>
            <label className="overline block mb-1.5">Your Birthday</label>
            <input type="date" className="input-min" value={birthday} onChange={e=>setBirthday(e.target.value)} data-testid="input-birthday" />
          </div>
          <div>
            <label className="overline block mb-1.5">Zodiac</label>
            <Select
              value={zodiac}
              onChange={setZodiac}
              placeholder="— pick your sign —"
              options={ZODIACS}
              testid="select-zodiac"
            />
          </div>
          <div>
            <label className="overline block mb-1.5">Your Lucky Numbers</label>
            <input className="input-min" placeholder="e.g. 8, 28, 88" value={lucky} onChange={e=>setLucky(e.target.value)} data-testid="input-lucky-numbers" />
          </div>
          <p className="text-[11px] text-ink-mute leading-relaxed">
            AI picks cost <span className="text-red font-semibold">1 credit</span>. You have <span className="text-red font-semibold">{user?.credits ?? 0}</span>.{user?.is_vip ? ' VIP: unlimited.' : ''}
          </p>
        </div>
      ) : (
        <p className="text-sm text-ink-mute mb-6">
          Quick Pick is unbiased randomness. Free, unlimited, instant.
        </p>
      )}

      <button
        onClick={spin}
        disabled={spinning || (tab === 'ai' && !aiInputsValid)}
        data-testid={tab === 'ai' ? 'predict-ai-button' : 'spin-button'}
        className="btn-red w-full inline-flex items-center justify-center gap-2 sticky bottom-28 shadow-[0_8px_24px_rgba(220,38,38,0.25)]"
        style={{ marginBottom: '24px' }}
      >
        {spinning ? (
          <><RotateCw size={18} className="animate-spin" /> Working…</>
        ) : tab === 'ai' ? (
          <><Wand2 size={18} /> Analyze & Predict</>
        ) : (
          <><Sparkles size={18} /> Generate</>
        )}
      </button>

      {/* Result modal */}
      <AnimatePresence>
        {result && (
          <motion.div
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="fixed inset-0 z-[60] flex items-end sm:items-center justify-center bg-ink/40 backdrop-blur-sm"
            onClick={closeResult}
            data-testid="result-modal"
          >
            <motion.div
              initial={{ y: 80, opacity: 0 }} animate={{ y: 0, opacity: 1 }} exit={{ y: 80, opacity: 0 }}
              transition={{ type: 'spring', stiffness: 200, damping: 24 }}
              className="w-full max-w-md mx-auto bg-white rounded-t-3xl sm:rounded-3xl px-6 pt-6 pb-8 relative"
              onClick={e => e.stopPropagation()}
            >
              <button className="absolute top-4 right-4 text-ink-mute hover:text-ink" onClick={closeResult} data-testid="close-result">
                <X size={20} />
              </button>
              <div className="overline text-center">{game.name} · {result.mode === 'ai' ? 'AI Lucky Pick' : 'Quick Pick'}</div>
              <div className="display text-2xl text-center mt-1 mb-5">Your numbers</div>

              {result.game_type === 'digit' && result.digit_sequence ? (
                <DigitRow length={result.digit_sequence.length} value={result.digit_sequence} size="lg" />
              ) : (
                <div className="flex flex-wrap justify-center gap-2 mb-2">
                  {result.numbers.map((n, idx) => <NumberToken key={idx} n={n} idx={idx} />)}
                </div>
              )}

              {result.mode === 'ai' && result.hot?.length > 0 && (
                <div className="grid grid-cols-2 gap-3 mt-5">
                  <div className="card-min p-3">
                    <div className="overline">Hot</div>
                    <div className="flex flex-wrap gap-1 mt-2">
                      {result.hot.slice(0,6).map(n => <span key={n} className="chip red">{n}</span>)}
                    </div>
                  </div>
                  <div className="card-min p-3">
                    <div className="overline">Cold</div>
                    <div className="flex flex-wrap gap-1 mt-2">
                      {result.cold.slice(0,6).map(n => <span key={n} className="chip">{n}</span>)}
                    </div>
                  </div>
                </div>
              )}

              {result.reasoning && (
                <p className="text-sm text-ink-mute italic text-center mt-5" data-testid="result-reasoning">
                  "{result.reasoning}"
                </p>
              )}

              <div className="grid grid-cols-2 gap-3 mt-6">
                <Link to="/history" className="btn-outline text-center inline-flex items-center justify-center" data-testid="save-pick-button">
                  View History
                </Link>
                <button className="btn-red inline-flex items-center justify-center gap-2" onClick={() => { closeResult(); spin(); }} data-testid="generate-again-button">
                  <RotateCw size={14} /> Again
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
