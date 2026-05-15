import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';

const UPDATED = 'May 15, 2026';
const COMPANY = 'JH Creative Enterprise';
const APP = 'HuatPick';
const CONTACT = 'turyoungpotato@gmail.com';

export default function TermsPage() {
  return (
    <div className="px-5 pt-12 pb-16 text-ink" data-testid="terms-page">
      <Link to="/" className="inline-flex items-center gap-2 text-ink-mute hover:text-ink mb-6 text-sm" data-testid="terms-back">
        <ArrowLeft size={16} /> Back
      </Link>

      <div className="overline">Legal · {UPDATED}</div>
      <h1 className="display text-3xl mt-2 mb-1">Terms of <span className="text-red">Service</span></h1>
      <p className="text-sm text-ink-mute mb-8 leading-relaxed">
        Welcome to <strong>{APP}</strong> ("the App"), operated by {COMPANY}. By creating an account
        or using the App you agree to be bound by these Terms.
      </p>

      <Section title="1. Eligibility">
        <P>You must be at least <strong>18 years old</strong> to use {APP}. By signing up you confirm
        you meet this age requirement. {APP} is intended for users in Malaysia and other jurisdictions
        where lottery participation is legal.</P>
      </Section>

      <Section title="2. What the service does">
        <P>{APP} is an <strong>entertainment tool</strong> that generates lucky-number suggestions
        for Malaysia lottery games (4D, 5D, 6D and Sports Toto 6/58, 6/55, 6/52, 6/50). Suggestions are
        produced by random sampling ("Quick Pick") or by an AI model that combines numerology inputs
        with historical draw frequencies ("AI Lucky Pick").</P>
        <P><strong>{APP} does not sell lottery tickets, take wagers, or process winnings.</strong>
        You must purchase actual tickets from a licensed Malaysian lottery operator separately.</P>
      </Section>

      <Section title="3. No guarantee of winnings">
        <P>Lottery draws are random events. Past frequencies have <strong>no predictive power</strong>
        over future draws. AI suggestions are entertainment only. {APP}, its operators, employees,
        and agents <strong>make no warranty</strong> that following any suggestion will result in
        winnings. By using the App you accept that any money you spend on actual lottery tickets is
        your sole responsibility and risk.</P>
      </Section>

      <Section title="4. Accounts">
        <P>You are responsible for keeping your password secret and for all activity on your account.
        Notify us at <a className="text-red underline" href={`mailto:${CONTACT}`}>{CONTACT}</a> if you suspect unauthorised access.</P>
        <P>We may suspend or terminate accounts that violate these Terms, attempt to abuse the service,
        or commit fraud.</P>
      </Section>

      <Section title="5. Free vs. paid features">
        <Bullet><strong>Free tier:</strong> 3 AI Lucky Picks on signup, unlimited Quick Picks, full history.</Bullet>
        <Bullet><strong>Premium AI picks:</strong> one-time purchase, adds AI-pick credits to your account.</Bullet>
        <Bullet><strong>VIP subscription:</strong> recurring monthly plan, grants unlimited AI picks and priority generation.</Bullet>
        <P>All prices are shown in MYR including any applicable taxes. Payments are processed by Stripe.</P>
      </Section>

      <Section title="6. Subscriptions, billing & cancellation">
        <P>VIP membership is billed in advance for a fixed period (e.g. 30 days). You can cancel at
        any time by contacting <a className="text-red underline" href={`mailto:${CONTACT}`}>{CONTACT}</a> or by managing
        the subscription in your Stripe customer portal. Cancellation stops future billing — your
        VIP access continues until the end of the paid-up period.</P>
      </Section>

      <Section title="7. Refunds">
        <P>Digital credits and VIP memberships are <strong>generally non-refundable</strong> once
        granted, because they unlock immediate use of AI services we pay per-call to provide.
        We will, however, refund:</P>
        <Bullet>Duplicate or accidental charges within 7 days.</Bullet>
        <Bullet>Charges made on an account that was compromised.</Bullet>
        <Bullet>Service that was unavailable for an extended period.</Bullet>
        <P>Email <a className="text-red underline" href={`mailto:${CONTACT}`}>{CONTACT}</a> with your transaction ID to request a refund review.</P>
      </Section>

      <Section title="8. Acceptable use">
        <P>You agree not to:</P>
        <Bullet>Scrape, reverse-engineer, or attempt to extract the underlying models or data of {APP}.</Bullet>
        <Bullet>Resell or share AI-pick output as a paid service of your own.</Bullet>
        <Bullet>Submit content that is unlawful, hateful, or targeted at harming others.</Bullet>
        <Bullet>Use the App to launder funds, evade taxes, or fund illegal activities.</Bullet>
      </Section>

      <Section title="9. Intellectual property">
        <P>The {APP} name, logo, code, and design are owned by {COMPANY}. You receive a limited,
        revocable, non-exclusive licence to use the App for personal entertainment.</P>
      </Section>

      <Section title="10. Limitation of liability">
        <P>To the maximum extent permitted by Malaysian law, {COMPANY} and its directors are not
        liable for any indirect, incidental, special, or consequential damages arising from your
        use of {APP}, including but not limited to lost winnings, lost profits, lost data, or
        emotional distress. Our total liability in any matter is limited to the amount you paid
        us in the 30 days preceding the claim.</P>
      </Section>

      <Section title="11. Responsible play">
        <P>If you feel gambling is harming you or someone close to you, please seek help:</P>
        <Bullet>Malaysian Mental Health Association (MMHA): <strong>03-2780 6803</strong></Bullet>
        <Bullet>Befrienders KL: <strong>03-7956 8145</strong></Bullet>
        <P>You may also email us at <a className="text-red underline" href={`mailto:${CONTACT}`}>{CONTACT}</a> to permanently close your account.</P>
      </Section>

      <Section title="12. Changes to these Terms">
        <P>We may update these Terms from time to time. The "Last updated" date at the top reflects
        the latest revision. Continued use after a change means you accept the new Terms.</P>
      </Section>

      <Section title="13. Governing law">
        <P>These Terms are governed by the laws of Malaysia. Any dispute will be subject to the
        exclusive jurisdiction of the courts of Malaysia.</P>
      </Section>

      <Section title="14. Contact">
        <P>{COMPANY}<br />
        Operator of {APP}<br />
        Email: <a className="text-red underline" href={`mailto:${CONTACT}`}>{CONTACT}</a></P>
      </Section>

      <p className="text-[11px] text-ink-mute text-center mt-10">
        Last updated: {UPDATED} · <Link to="/privacy" className="text-red underline">Privacy Policy</Link>
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
