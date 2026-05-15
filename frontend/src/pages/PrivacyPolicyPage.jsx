import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';

const UPDATED = 'May 15, 2026';
const COMPANY = 'JH Creative Enterprise';
const APP = 'HuatPick';
const CONTACT = 'turyoungpotato@gmail.com';

export default function PrivacyPolicyPage() {
  return (
    <div className="px-5 pt-12 pb-16 text-ink" data-testid="privacy-page">
      <Link to="/" className="inline-flex items-center gap-2 text-ink-mute hover:text-ink mb-6 text-sm" data-testid="privacy-back">
        <ArrowLeft size={16} /> Back
      </Link>

      <div className="overline">Legal · {UPDATED}</div>
      <h1 className="display text-3xl mt-2 mb-1">Privacy <span className="text-red">Policy</span></h1>
      <p className="text-sm text-ink-mute mb-8 leading-relaxed">
        {COMPANY} ("we", "our", "us") operates the <strong>{APP}</strong> mobile and web
        application. This Privacy Policy explains what data we collect, how we use it,
        and the choices you have. By using {APP} you agree to this policy.
      </p>

      <Section title="1. Information we collect">
        <P><strong>Account data</strong> — your email address, a one-way bcrypt hash of your password,
        a display name (if provided), and a unique user ID generated when you sign up.</P>
        <P><strong>Usage data</strong> — every lottery pick you generate (game, numbers, mode, timestamp),
        whether you used Quick Pick or AI mode, and any AI-input you provide (birthday, zodiac, lucky numbers).
        We do not store the raw text of your AI reasoning request beyond what is needed to display your history.</P>
        <P><strong>Payment data</strong> — when you purchase credits or VIP, we record the Stripe session ID,
        amount, currency, and status. <strong>We do not see or store your card details</strong> — Stripe
        handles all card data directly under PCI DSS standards.</P>
        <P><strong>Technical data</strong> — server access logs (IP address, user agent, request path)
        retained up to 30 days for security and debugging.</P>
      </Section>

      <Section title="2. How we use your data">
        <Bullet>To authenticate you and keep your account secure.</Bullet>
        <Bullet>To generate AI-powered lucky-number predictions based on inputs you provide.</Bullet>
        <Bullet>To display your pick history.</Bullet>
        <Bullet>To process subscription and one-time payments via Stripe.</Bullet>
        <Bullet>To detect abuse, fraud, and to improve the service.</Bullet>
        <Bullet>To send service-related notifications (e.g. successful payment receipts).</Bullet>
      </Section>

      <Section title="3. Third-party processors">
        <P>We use the following sub-processors. They each have their own privacy policies.</P>
        <Bullet><strong>Stripe</strong> — payment processing. <a className="text-red underline" href="https://stripe.com/privacy" target="_blank" rel="noreferrer">stripe.com/privacy</a></Bullet>
        <Bullet><strong>Google (Gemini)</strong> — runs the AI lucky-number predictions on the inputs you provide.
          We do not store your raw prompt with Google beyond the API call itself. <a className="text-red underline" href="https://policies.google.com/privacy" target="_blank" rel="noreferrer">policies.google.com/privacy</a></Bullet>
        <Bullet><strong>4dmoon.com / lottolyzer.com / 4d2u.com</strong> — public lottery-result sources we scrape for hot/cold analysis.
          We send no personal data to these sites.</Bullet>
        <Bullet><strong>Emergent Agent (preview infrastructure)</strong> — hosts the application servers.</Bullet>
      </Section>

      <Section title="4. Data retention">
        <P>Account and pick-history data are kept for as long as your account exists.
        Payment records are kept for 7 years to comply with accounting regulations.
        Server logs are rotated every 30 days. You can delete your account at any
        time by emailing us — all personal data is removed within 30 days of the request.</P>
      </Section>

      <Section title="5. Your rights">
        <P>You have the right to:</P>
        <Bullet><strong>Access</strong> the data we hold on you.</Bullet>
        <Bullet><strong>Correct</strong> inaccurate data (email, name).</Bullet>
        <Bullet><strong>Delete</strong> your account and all associated personal data.</Bullet>
        <Bullet><strong>Export</strong> your pick history in JSON.</Bullet>
        <Bullet><strong>Object</strong> to processing or withdraw consent at any time.</Bullet>
        <P>To exercise any of these rights, email <a className="text-red underline" href={`mailto:${CONTACT}`}>{CONTACT}</a>.</P>
      </Section>

      <Section title="6. Cookies & local storage">
        <P>{APP} stores a single JWT authentication token in your browser's localStorage
        to keep you signed in. We do not use third-party advertising cookies.</P>
      </Section>

      <Section title="7. Children's privacy">
        <P>{APP} is intended for users aged <strong>18 and above</strong> only. We do not
        knowingly collect data from children. If we discover an account belongs to a minor,
        we will delete it immediately.</P>
      </Section>

      <Section title="8. Lottery & gambling note">
        <P>{APP} provides <strong>entertainment-only number suggestions</strong>. We do not
        sell lottery tickets, take bets, or guarantee any winnings. AI predictions are
        based on historical patterns and have no statistical advantage in random draws.
        Please play responsibly. If gambling is a problem for you, contact the Malaysian
        Mental Health Association (MMHA) at 03-2780 6803.</P>
      </Section>

      <Section title="9. Security">
        <P>We use industry-standard protections: bcrypt password hashing, HTTPS everywhere,
        JWT auth tokens with expiry, and least-privilege database access. No system is 100%
        secure — if you suspect a breach of your account, email us immediately at <a className="text-red underline" href={`mailto:${CONTACT}`}>{CONTACT}</a>.</P>
      </Section>

      <Section title="10. International transfers">
        <P>Your data may be processed in jurisdictions outside Malaysia (e.g. Stripe in the US,
        Google Cloud servers globally). We use providers who offer Standard Contractual Clauses
        or equivalent safeguards.</P>
      </Section>

      <Section title="11. Changes to this policy">
        <P>We will update this Privacy Policy when the service changes meaningfully. The latest
        version always lives at this URL. Material changes will trigger an in-app notice.</P>
      </Section>

      <Section title="12. Contact">
        <P>{COMPANY}<br />
        Operator of {APP}<br />
        Email: <a className="text-red underline" href={`mailto:${CONTACT}`}>{CONTACT}</a></P>
      </Section>

      <p className="text-[11px] text-ink-mute text-center mt-10">
        Last updated: {UPDATED} · <Link to="/terms" className="text-red underline">Terms of Service</Link>
      </p>
    </div>
  );
}

function Section({ title, children }) {
  return (
    <div className="mb-6">
      <h2 className="font-semibold text-base mb-2">{title}</h2>
      <div className="space-y-3 text-sm text-ink leading-relaxed">{children}</div>
    </div>
  );
}
function P({ children }) { return <p>{children}</p>; }
function Bullet({ children }) {
  return (
    <div className="flex gap-2">
      <span className="text-red flex-shrink-0">·</span>
      <span>{children}</span>
    </div>
  );
}
