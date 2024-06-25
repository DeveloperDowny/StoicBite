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
    <div className="max-w-[28rem] opacity-0" ref={parentContRef}>
      <QuoteCont />
      <QuoteExplain />
    </div>
  );
};

export default QuotePage;
