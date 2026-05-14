import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'sonner';
import { AuthProvider, useAuth } from './lib/auth';

import AuthPage from './pages/AuthPage';
import HomePage from './pages/HomePage';
import GeneratePage from './pages/GeneratePage';
import HistoryPage from './pages/HistoryPage';
import VipPage from './pages/VipPage';
import ProfilePage from './pages/ProfilePage';
import PaymentSuccessPage from './pages/PaymentSuccessPage';
import BottomNav from './components/BottomNav';

function Protected({ children }) {
  const { user, loading } = useAuth();
  if (loading) return <Splash />;
  if (!user) return <Navigate to="/auth" replace />;
  return children;
}

function Splash() {
  return (
    <div className="mobile-shell flex items-center justify-center min-h-screen">
      <div className="text-center">
        <div className="w-10 h-10 rounded-full bg-red mx-auto animate-pulse"></div>
        <div className="mt-3 text-ink-mute text-sm">Loading…</div>
      </div>
    </div>
  );
}

function Shell() {
  const { user } = useAuth();
  return (
    <div className={`mobile-shell ${user ? 'safe-bottom' : ''}`}>
      <Routes>
        <Route path="/auth" element={user ? <Navigate to="/" replace /> : <AuthPage />} />
        <Route path="/" element={<Protected><HomePage /></Protected>} />
        <Route path="/generate" element={<Protected><GeneratePage /></Protected>} />
        <Route path="/generate/:gameId" element={<Protected><GeneratePage /></Protected>} />
        <Route path="/history" element={<Protected><HistoryPage /></Protected>} />
        <Route path="/vip" element={<Protected><VipPage /></Protected>} />
        <Route path="/profile" element={<Protected><ProfilePage /></Protected>} />
        <Route path="/payment-success" element={<Protected><PaymentSuccessPage /></Protected>} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
      {user && <BottomNav />}
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Shell />
        <Toaster theme="light" position="top-center" toastOptions={{
          style: { background: '#fff', color: '#0A0A0A', border: '1px solid #E5E5E5' }
        }} />
      </AuthProvider>
    </BrowserRouter>
  );
}
