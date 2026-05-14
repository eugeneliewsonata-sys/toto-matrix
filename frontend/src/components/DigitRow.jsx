import React, { useEffect, useState } from 'react';

/**
 * Big digit row display for 4D / 5D / 6D games.
 * - When `spinning`, digits flicker random 0-9.
 * - When `value` is provided (string of digits), shows those digits revealed.
 */
export default function DigitRow({ length = 4, value = null, spinning = false, size = 'lg' }) {
  const [flicker, setFlicker] = useState(Array.from({ length }, () => 0));

  useEffect(() => {
    if (!spinning) return;
    const t = setInterval(() => {
      setFlicker(Array.from({ length }, () => Math.floor(Math.random() * 10)));
    }, 70);
    return () => clearInterval(t);
  }, [spinning, length]);

  const digits = value
    ? value.padStart(length, '0').slice(0, length).split('')
    : (spinning ? flicker.map(String) : Array.from({ length }, () => '–'));

  return (
    <div className={`digit-row ${size}`} data-testid="digit-row">
      {digits.map((d, i) => (
        <div key={i} className={`digit-cell ${spinning && !value ? 'spin' : ''}`} data-testid={`result-digit-${i + 1}`}>
          {d}
        </div>
      ))}
    </div>
  );
}
