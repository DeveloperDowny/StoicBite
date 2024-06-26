"use client";

import QuoteCont from "@/components/QuoteCont/QuoteCont";
import QuoteExplain from "@/components/QuoteExplain/QuoteExplain";
import React, { useEffect, useRef } from "react";

import gsap from "gsap";

const QuotePage = () => {
  const parentContRef = useRef(null);
  // when page loads set window.innerHeight to css variable --full_height
  useEffect(() => {
    document.documentElement.style.setProperty(
      "--full_height",
      `${window.innerHeight}px`
    );
  }, []);

  // take 2 sec to fade in the parent container
  useEffect(() => {
    gsap.to(parentContRef.current, {
      duration: 2,
      opacity: 1,
    });
  }, []);

  return (
    <div className="max-w-[28rem] opacity-0 relative" ref={parentContRef}>
      <QuoteCont quote={quote} quote_by={quote_by} />
      <QuoteExplain explaination={explaination} />
    </div>
  );
};

export default QuotePage;

const explaination = `Listen to these words, dear pupil: "And he does live with the gods who constantly shows to them, his own soul is satisfied with that which is assigned to him, and that it does all that the daemon wishes, which Zeus hath given to every man for his guardian and guide, a portion of himself."\nTo live with the gods means to live a life that aligns with divine virtue and wisdom. When a person shows the gods that their soul is content with their lot in life, they demonstrate a profound acceptance and understanding of their role in the universe. This satisfaction is not born of passive resignation but of active embrace of one's destiny and duties.\nEach man, by the will of Zeus, has been blessed with a daemon, a guiding spirit, a portion of the divine that steers him. To live in harmony with this daemon is to heed its counsel, to live virtuously, and to fulfill one's purpose. Thus, true contentment and divine unity are found not in external circumstances but within our inner acceptance and alignment with the higher \n Reflect upon this, and seek the serenity that comes from fulfilling the divine duty assigned to you by fate.`;

const quote = `And he does live with the gods who constantly shows to them, his own soul is satisfied with that which is assigned to him, and that it does all that the daemon wishes, which Zeus hath given to every man for his guardian and guide, a portion of himself.`;

const quote_by = `Marcus Aurelius`;
