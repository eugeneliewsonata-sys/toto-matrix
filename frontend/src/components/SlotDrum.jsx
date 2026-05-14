import React, { useEffect, useState } from 'react';

/** Slot machine drum that spins random digits then locks to `target` */
export default function SlotDrum({ target, spinning, idx = 0 }) {
  const [display, setDisplay] = useState(0);

  useEffect(() => {
    if (!spinning) { setDisplay(target ?? 0); return; }
    const t = setInterval(() => {
      setDisplay(Math.floor(Math.random() * 59));
    }, 60);
    return () => clearInterval(t);
  }, [spinning, target]);

  return (
    <div className="slot-window" data-testid={`slot-${idx}`}>
      <div className="slot-strip">
        <span>{String(spinning ? display : (target ?? '–')).padStart(2, '0')}</span>
      </div>
    </div>
  );
}
