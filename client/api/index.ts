import axios from "axios";

const axiosClient = axios.create();

axiosClient.defaults.baseURL = "http://localhost:5000";

// axiosClient.defaults.headers = {
//   "Content-Type": "application/json",
//   Accept: "application/json",
// };

// res.headers['X-Content-Type-Options'] = '*' add this too
// axiosClient.defaults.headers["X-Content-Type-Options"] = "*";

// All requests will wait 10 seconds before timing out
axiosClient.defaults.timeout = 10 * 1000;

// axiosClient.defaults.withCredentials = true;

export const getRequest = (URL) =>
  axiosClient.get(`/${URL}`).then((response) => response);

export const postRequest = (URL, payload) =>
  axiosClient.post(`/${URL}`, payload).then((response) => response);

export const patchRequest = (URL, payload) =>
  axiosClient.patch(`/${URL}`, payload).then((response) => response);

export const deleteRequest = (URL) =>
  axiosClient.delete(`/${URL}`).then((response) => response);

export const kdm = false;
export const fetchQuote = async () => {
  try {
    if (kdm) {
      const quote = `"And he does live with the gods who constantly shows to them, his own soul is satisfied with that which is assigned to him, and that it does all that the daemon wishes, which Zeus hath given to every man for his guardian and guide, a portion of himself." --Marcus Aurelius, Meditations, Book 5`;
      const pay = {
        quote: quote,
      };
      const response = await postRequest("process_quote", pay);
      const delayPromis = (ms) => new Promise((res) => setTimeout(res, ms));
      await delayPromis(2000);
      return parseQuoteResponse(response.data);
    } else {
      const response = await getRequest("daily_stoic");
      return parseQuoteResponse(response.data);
    }
  } catch (error) {
    return parseQuoteResponse(fallbackQuote);
    return {
      quote: "Error fetching quote",
      error: true,
      quote_by: "Please try again later",
    };
  }
};
function parseQuoteResponse(data) {
  const ns = data.quote.split("--");
  const quote_by = ns[1].split(",")[0];
  const plain_quote_without_double_quotes = ns[0].replace(/"/g, "");
  const without_right_space = plain_quote_without_double_quotes.trim();

  return {
    quote: without_right_space,
    quote_by: quote_by,
    explanation: data.explanation,
    error: false,
  };
}

const fallbackQuote = {
  quote:
    '"And show him with gentle tact and by general principles that this is so, and that even bees do not do as he does, nor any animals which are formed by nature to be gregarious." --Marcus Aurelius, Meditations, Book 11',
  explanation:
    "My dear pupil, consider the behaviors and inclinations bestowed upon beings by Nature herself. It is a marvel how each creature, within its station, adheres to the order of its kind. Reflect on the bees, those small but diligent architects of harmony within their hives. They work in concert, each knowing its role, striving for the collective good without deviation or dissent.\n\nNow turn your mind to mankind, who is also formed for the purpose of living in fellowship, guided by reason and a sense of duty to one another. When an individual diverges from this natural law, acting selfishly or disruptively, they stray not only from their own nature but from the very principles that sustain communal life.\n\nThus, when you encounter one who is wayward and fails to conform to these principles, approach them with gentle understanding. Illuminate for them, through reason and the broader truths of our existence, their deviation from the path. Remind them that even the simplest creatures adhere to the natural order, working together in a spirit of unity and mutual support.\n\nIt is in this way that, with patience and wisdom, you may guide them back to the fold of collective harmony. Show them that to live for oneself alone is contrary not just to our societal bonds, but to the very essence of our being. For we are all threads in the vast tapestry of life, and our strength and purpose lie in our interconnectedness.",
};
