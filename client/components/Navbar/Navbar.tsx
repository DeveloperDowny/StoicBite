"use client";

import Image from "next/image";
import styles from "./Navbar.module.css";

import React, { useEffect, useRef } from "react";

import gsap from "gsap";

const Navbar = () => {
  const parentContRef = useRef(null);

  useEffect(() => {
    gsap.to(parentContRef.current, {
      duration: 0.5,
      opacity: 1,
    });
  }, []);
  return (
    <div className={styles.cont} ref={parentContRef}>
      <Image
        src="/images/logo.svg"
        alt="logo"
        width={110}
        height={100}
        className="mt-[-2rem]"
      />
    </div>
  );
};

export default Navbar;
