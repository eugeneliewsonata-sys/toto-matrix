import React from 'react';
import { NavLink } from 'react-router-dom';
import { Home, Sparkles, History, Crown, User } from 'lucide-react';

const items = [
  { to: '/', label: 'Home', icon: Home, testid: 'nav-home' },
  { to: '/generate', label: 'Pick', icon: Sparkles, testid: 'nav-generate' },
  { to: '/history', label: 'History', icon: History, testid: 'nav-history' },
  { to: '/vip', label: 'VIP', icon: Crown, testid: 'nav-vip' },
  { to: '/profile', label: 'Account', icon: User, testid: 'nav-profile' },
];

export default function BottomNav() {
  return (
    <nav
      className="fixed bottom-0 left-1/2 -translate-x-1/2 w-full max-w-md bg-white border-t border-ink-line z-50"
      style={{ paddingBottom: 'env(safe-area-inset-bottom)' }}
      data-testid="bottom-nav"
    >
      <ul className="flex justify-around items-center py-2">
        {items.map(({ to, label, icon: Icon, testid }) => (
          <li key={to}>
            <NavLink
              to={to}
              end={to === '/'}
              data-testid={testid}
              className={({ isActive }) =>
                `flex flex-col items-center gap-1 px-3 py-2 text-[10px] uppercase tracking-widest transition-colors ${
                  isActive ? 'text-red' : 'text-ink-mute hover:text-ink'
                }`
              }
            >
              {({ isActive }) => (
                <>
                  <Icon size={20} strokeWidth={isActive ? 2.4 : 1.8} />
                  <span className="font-medium tracking-wider">{label}</span>
                </>
              )}
            </NavLink>
          </li>
        ))}
      </ul>
    </nav>
  );
}
