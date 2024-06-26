"use client";

import { useEffect, useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/dist/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

import styles from "./QuoteExplain.module.css";

import React from "react";

const QuoteExplain = () => {
  useEffect(() => {
    for (let i = 0; i < ns.length; i++) {
      gsap.fromTo(
        `.explain_cont .p${i}`,
        {
          opacity: 0,
        },
        {
          opacity: 1,
          y: 0,
          duration: 0.5,
          scrollTrigger: {
            trigger: `.explain_cont .p${i}`,
            start: "top bottom-=50",
            end: "bottom center",
          },
          stagger: 0.2,
        }
      );
    }
    return () => {
      ScrollTrigger.getAll().forEach((trigger) => trigger.kill());
    };
  }, []);

  return (
    <div className={`${styles.explain_cont} explain_cont`}>
      {ns.map((n, i) => {
        return (
          <p key={i} className={`${styles.explain} p${i}`}>
            {n}
          </p>
        );
      })}
    </div>
  );
};
const explaination = `Listen to these words, dear pupil: "And he does live with the gods who constantly shows to them, his own soul is satisfied with that which is assigned to him, and that it does all that the daemon wishes, which Zeus hath given to every man for his guardian and guide, a portion of himself."\nTo live with the gods means to live a life that aligns with divine virtue and wisdom. When a person shows the gods that their soul is content with their lot in life, they demonstrate a profound acceptance and understanding of their role in the universe. This satisfaction is not born of passive resignation but of active embrace of one's destiny and duties.\nEach man, by the will of Zeus, has been blessed with a daemon, a guiding spirit, a portion of the divine that steers him. To live in harmony with this daemon is to heed its counsel, to live virtuously, and to fulfill one's purpose. Thus, true contentment and divine unity are found not in external circumstances but within our inner acceptance and alignment with the higher \n Reflect upon this, and seek the serenity that comes from fulfilling the divine duty assigned to you by fate.`;

const ns = explaination.replace("\n\n", "\n").split("\n");
export default QuoteExplain;
