"use client";

import QuoteCont from "@/components/QuoteCont/QuoteCont";
import QuoteExplain from "@/components/QuoteExplain/QuoteExplain";
import React, { useEffect, useRef, useState } from "react";

import gsap from "gsap";
import { fetchQuote } from "@/api";

const QuotePage = () => {
  const [data, setData] = useState({});
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    let isMounted = true;

    const fetchData = async () => {
      setLoading(true);
      try {
        const quoteData = () => {
          return new Promise((resolve) => {
            setTimeout(() => {
              resolve({
                data: {
                  quote: quote,
                  quote_by: quote_by,
                  explanation: explanation,
                },
              });
            }, 2000);
          });
        };
        // const res = await quoteData();
        const res = await fetchQuote();
        if (isMounted) {
          setData(res);
          setLoading(false);
        }
      } catch (err) {
        setLoading(false);
      }
    };
    fetchData();

    return () => {
      isMounted = false;
    };
  }, []);

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
    <div
      className="max-w-[28rem] opacity-0 relative w-full"
      ref={parentContRef}
    >
      <QuoteCont quote={data.quote} quote_by={data.quote_by} />
      <QuoteExplain explanation={data.explanation} />
    </div>
  );
};

export default QuotePage;
