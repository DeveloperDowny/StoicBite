import Image from "next/image";
import styles from "./QuoteCont.module.css";

import React from "react";

const QuoteCont = () => {
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
      <div className={styles.main_cont}>
        <div className={styles.quote}>{quote}</div>
        <div className={styles.quote_by}>— {quote_by}</div>
      </div>
    </div>
  );
};

const quote = `And he does live with the gods who constantly shows to them, his own soul is satisfied with that which is assigned to him, and that it does all that the daemon wishes, which Zeus hath given to every man for his guardian and guide, a portion of himself.`;

const quote_by = `Marcus Aurelius`;

export default QuoteCont;
