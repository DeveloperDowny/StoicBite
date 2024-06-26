"use client";

import { useEffect, useRef } from "react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/dist/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

import Image from "next/image";
import styles from "./QuoteCont.module.css";

import React from "react";

const QuoteCont = ({ quote, quote_by }) => {
  const boxRef = useRef(null);
  const quoteByRef = useRef(null);

  useEffect(() => {
    const box = boxRef.current;

    gsap.fromTo(
      box,
      {
        opacity: 0,
        y: 10,
      },
      {
        opacity: 1,
        y: 0,
        duration: 1,
      }
    );

    gsap.fromTo(
      quoteByRef.current,
      {
        opacity: 0,
      },
      {
        opacity: 1,
        delay: 0.5,
        duration: 1,
      }
    );

    return () => {
      ScrollTrigger.getAll().forEach((trigger) => trigger.kill());
    };
  }, [quote]);

  return (
    <div className={styles.parent_cont}>
      <div className={styles.img_cont}>
        <Image
          src="/images/marcus_image.png"
          layout="fill"
          objectFit="cover"
          alt={""}
        />
      </div>
      <div className={styles.black_overlay}>
        <Image
          src="/images/black_gradient.svg"
          layout="fill"
          objectFit="cover"
          alt={""}
        />
      </div>
      {quote && (
        <div className={styles.main_cont}>
          <div className={styles.quote} ref={boxRef}>
            <div className={styles.quote_img_cont}>
              <Image
                src="/images/quote_img.png"
                layout="fill"
                objectFit="cover"
                alt={""}
              />
            </div>
            {quote}
          </div>
          <div className={styles.quote_by} ref={quoteByRef}>
            — {quote_by}
          </div>
        </div>
      )}
    </div>
  );
};

export default QuoteCont;
