"use client";

import { useEffect, useRef, useState } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/dist/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

import styles from "./QuoteExplain.module.css";

import React from "react";

const QuoteExplain = ({ explaination }) => {
  const [ns, setNs] = useState([]);
  useEffect(() => {
    if (!explaination) return;
    const ns = preProcessFunc(explaination);
    setNs(ns);
  }, [explaination]);

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
  }, [ns]);

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

const preProcessFunc = (explaination) =>
  explaination.replace("\n\n", "\n").split("\n");
export default QuoteExplain;
