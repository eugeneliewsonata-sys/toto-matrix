import React from 'react';
import { useAuth } from '../lib/auth';
import { Crown, LogOut, Mail, ArrowRight } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';

export default function ProfilePage() {
  const { user, logout } = useAuth();
  const nav = useNavigate();
  const onLogout = () => { logout(); nav('/auth'); };

  return (
    <div className="px-5 pt-12 pb-6" data-testid="profile-page">
      <div className="overline">My Account</div>
      <h2 className="display text-3xl mb-6">Profile</h2>

      <div className="card-min p-6 mb-5">
        <div className="flex items-center gap-4 mb-5">
          <div className={`w-14 h-14 rounded-full flex items-center justify-center text-2xl font-bold ${user?.is_vip ? 'bg-red text-white' : 'bg-[#F4F4F5] text-red'}`}>
            {user?.name?.[0]?.toUpperCase() || '?'}
          </div>
          <div className="min-w-0">
            <div className="font-semibold text-lg truncate">{user?.name}</div>
            <div className="text-xs text-ink-mute inline-flex items-center gap-1.5 mt-0.5" data-testid="profile-email">
              <Mail size={11} /> {user?.email}
            </div>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div className="rounded-xl bg-[#F8F8F8] p-3">
            <div className="overline">AI Credits</div>
            <div className="display text-3xl mt-1 text-red">{user?.credits ?? 0}</div>
          </div>
          <div className="rounded-xl bg-[#F8F8F8] p-3">
            <div className="overline">VIP</div>
            <div className="font-semibold text-base mt-1" data-testid="vip-status-badge">
              {user?.is_vip ? <span className="text-red inline-flex items-center gap-1"><Crown size={13} /> Active</span> : <span className="text-ink-mute">Inactive</span>}
            </div>
            {user?.vip_until && user?.is_vip && (
              <div className="text-[10px] text-ink-mute mt-0.5">Until {new Date(user.vip_until).toLocaleDateString()}</div>
            )}
          </div>
        </div>
      </div>

      <Link to="/vip" className="card-min p-4 mb-3 flex items-center justify-between hover:border-red transition-colors" data-testid="profile-upgrade-link">
        <div>
          <div className="font-semibold text-sm">{user?.is_vip ? 'Manage VIP membership' : 'Upgrade to VIP'}</div>
          <div className="text-xs text-ink-mute">Unlimited AI lucky picks</div>
        </div>
        <ArrowRight size={16} className="text-ink-mute" />
      </Link>

      <button onClick={onLogout} className="w-full inline-flex items-center justify-center gap-2 text-ink-mute py-4 hover:text-red transition-colors text-sm font-semibold" data-testid="logout-button">
        <LogOut size={15} /> Sign Out
      </button>

      <p className="text-[11px] text-ink-mute text-center mt-8 leading-relaxed">
        HuatPick is an AI entertainment tool. No guarantees of winnings.<br />Play responsibly.
      </p>
    </div>
  );
}
