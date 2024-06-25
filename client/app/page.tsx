"use client";

import QuoteCont from "@/components/QuoteCont/QuoteCont";
import QuoteExplain from "@/components/QuoteExplain/QuoteExplain";
import React from "react";

const QuotePage = () => {
  // when page loads set window.innerHeight to css variable --full_height
  React.useEffect(() => {
    document.documentElement.style.setProperty(
      "--full_height",
      `${window.innerHeight}px`
    );
  }, []);
  
  return (
    <div className="max-w-[28rem]">
      <QuoteCont />
      <QuoteExplain />
    </div>
  );
};

export default QuotePage;
