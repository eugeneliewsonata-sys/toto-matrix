import React, { useEffect, useState } from 'react';
import { api } from '../lib/api';
import { useAuth } from '../lib/auth';
import { Navigate, useNavigate } from 'react-router-dom';
import { toast } from 'sonner';
import { ArrowLeft, Database, Download, FlaskConical, Loader2, Plus } from 'lucide-react';

export default function AdminPage() {
  const { user } = useAuth();
  const nav = useNavigate();
  const [stats, setStats] = useState(null);
  const [draws, setDraws] = useState(null);
  const [rawText, setRawText] = useState('');
  const [label, setLabel] = useState('manual paste');
  const [busy, setBusy] = useState('');

  const load = async () => {
    const [s, d] = await Promise.all([api.get('/admin/stats'), api.get('/admin/draws')]);
    setStats(s.data);
    setDraws(d.data);
  };

  useEffect(() => {
    if (user && user.is_admin) load();
  }, [user]);

  if (user && !user.is_admin) return <Navigate to="/" replace />;

  const addDraws = async () => {
    if (!rawText.trim()) { toast.error('Paste some 4-digit numbers first'); return; }
    setBusy('add');
    try {
      const r = await api.post('/admin/draws', { raw_text: rawText, label });
      toast.success(`Injected ${r.data.added} numbers`);
      setRawText('');
      await load();
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed');
    } finally { setBusy(''); }
  };

  const scrape = async () => {
    setBusy('scrape');
    try {
      const r = await api.post('/admin/scrape', {});
      toast.success(`Fetched ${r.data.fetched} numbers from 4dmoon.com`);
      await load();
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Scrape failed');
    } finally { setBusy(''); }
  };

  return (
    <div className="px-5 pt-12 pb-6" data-testid="admin-page">
      <div className="flex items-center gap-3 mb-6">
        <button onClick={() => nav('/profile')} className="text-ink-mute" data-testid="admin-back"><ArrowLeft size={20} /></button>
        <div>
          <div className="overline">System</div>
          <h2 className="display text-3xl">Admin <span className="text-red">Console</span></h2>
        </div>
      </div>

      {/* Stats */}
      {stats && (
        <div className="grid grid-cols-2 gap-3 mb-6">
          <Stat label="Users" value={stats.users} />
          <Stat label="Total Picks" value={stats.picks} />
          <Stat label="Transactions" value={`${stats.paid_txns}/${stats.txns}`} hint="paid / total" />
          <Stat label="Pool Size" value={`${stats.extra_pool_size.toLocaleString()}c`} hint="extras + scrape chars" />
        </div>
      )}

      {/* Draws library */}
      <div className="card-min p-5 mb-5">
        <div className="flex items-center gap-2 mb-2">
          <Database size={16} className="text-red" />
          <div className="font-semibold">Data Library</div>
        </div>
        {draws && (
          <div className="grid grid-cols-3 gap-3 mt-3">
            <Mini label="Bundled" value={draws.bundled_draws} sub={`${draws.bundled_count} nums`} />
            <Mini label="Manual" value={draws.manual_draws} sub="batches" />
            <Mini label="Live cache" value={draws.live_cache_count || 0} sub="4D scraped" />
          </div>
        )}
        {draws?.live_cache_fetched_at && (
          <p className="text-[10px] text-ink-mute mt-3">Live last fetched: {new Date(draws.live_cache_fetched_at).toLocaleString()}</p>
        )}
      </div>

      {/* Live scrape */}
      <div className="card-min p-5 mb-5">
        <div className="flex items-center gap-2 mb-2">
          <Download size={16} className="text-red" />
          <div className="font-semibold">Scrape 4dmoon.com</div>
        </div>
        <p className="text-xs text-ink-mute mb-4">Pulls the latest 4D draw numbers from 4dmoon.com and adds them to the data pool. Runs automatically on app startup, but you can refresh on demand.</p>
        <button onClick={scrape} disabled={busy === 'scrape'} className="btn-outline w-full inline-flex items-center justify-center gap-2" data-testid="admin-scrape-btn">
          {busy === 'scrape' ? <><Loader2 size={14} className="animate-spin" /> Scraping…</> : <>Run live scrape</>}
        </button>
      </div>

      {/* Manual injection */}
      <div className="card-min p-5 mb-5">
        <div className="flex items-center gap-2 mb-2">
          <Plus size={16} className="text-red" />
          <div className="font-semibold">Inject Draw Data</div>
        </div>
        <p className="text-xs text-ink-mute mb-3">Paste raw text. Every 4-digit run will be extracted and saved.</p>
        <input className="input-min mb-2" placeholder="Label (e.g. '14 May draw')" value={label} onChange={e => setLabel(e.target.value)} data-testid="admin-label-input" />
        <textarea
          className="input-min font-mono text-sm"
          rows={6}
          placeholder="e.g. 4827 1234 9999 0001 ..."
          value={rawText}
          onChange={e => setRawText(e.target.value)}
          data-testid="admin-raw-input"
        />
        <button onClick={addDraws} disabled={busy === 'add'} className="btn-red w-full mt-3 inline-flex items-center justify-center gap-2" data-testid="admin-add-btn">
          {busy === 'add' ? <><Loader2 size={14} className="animate-spin" /> Injecting…</> : <>Inject into Pool</>}
        </button>
      </div>

      {/* Hot/Cold preview */}
      {stats && (
        <div className="card-min p-5 mb-5">
          <div className="flex items-center gap-2 mb-3">
            <FlaskConical size={16} className="text-red" />
            <div className="font-semibold">Hot / Cold Preview</div>
          </div>
          <div className="space-y-3">
            <HotCold label="4D / 5D / 6D digits" hot={stats.digit_hot_cold.hot} cold={stats.digit_hot_cold.cold} />
            <HotCold label="Toto 6/58 numbers" hot={stats.toto_6_58_hot_cold.hot} cold={stats.toto_6_58_hot_cold.cold} />
          </div>
        </div>
      )}

      {/* Recent manual draws */}
      {draws?.draws && draws.draws.length > 0 && (
        <div className="mb-6">
          <div className="overline mb-2">Recent manual batches</div>
          <div className="space-y-2">
            {draws.draws.slice(0, 5).map(d => (
              <div key={d.id} className="card-min p-3 text-xs">
                <div className="flex justify-between"><strong>{d.label}</strong><span className="text-ink-mute">{d.count} nums</span></div>
                <div className="text-ink-mute mt-1">{new Date(d.created_at).toLocaleString()} · {d.created_by}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function Stat({ label, value, hint }) {
  return (
    <div className="card-min p-4">
      <div className="overline">{label}</div>
      <div className="display text-2xl mt-1 text-red">{value}</div>
      {hint && <div className="text-[10px] text-ink-mute mt-0.5">{hint}</div>}
    </div>
  );
}

function Mini({ label, value, sub }) {
  return (
    <div className="text-center">
      <div className="overline">{label}</div>
      <div className="display text-xl mt-1">{value}</div>
      <div className="text-[10px] text-ink-mute">{sub}</div>
    </div>
  );
}

function HotCold({ label, hot, cold }) {
  return (
    <div>
      <div className="text-xs font-semibold mb-1.5">{label}</div>
      <div className="flex flex-wrap gap-1 mb-1">
        <span className="text-[10px] uppercase tracking-widest text-red w-10">Hot</span>
        {hot.map(n => <span key={`h-${n}`} className="chip red">{n}</span>)}
      </div>
      <div className="flex flex-wrap gap-1">
        <span className="text-[10px] uppercase tracking-widest text-ink-mute w-10">Cold</span>
        {cold.map(n => <span key={`c-${n}`} className="chip">{n}</span>)}
      </div>
    </div>
  );
}
