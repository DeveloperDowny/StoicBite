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

export const kdm = true;
export const fetchQuote = async () => {
  try {
    if (kdm) {
      const quote = `"And he does live with the gods who constantly shows to them, his own soul is satisfied with that which is assigned to him, and that it does all that the daemon wishes, which Zeus hath given to every man for his guardian and guide, a portion of himself." --Marcus Aurelius, Meditations, Book 5`;
      const pay = {
        quote: quote,
      };
      const response = await postRequest("process_quote", pay);
      const data = response.data;
      const ns = data.quote.split("--");
      const quote_by = ns[1].split(",")[0];
      const plain_quote_without_double_quotes = ns[0].replace(/"/g, "");
      const without_right_space = plain_quote_without_double_quotes.trim();
      const delayPromis = (ms) => new Promise((res) => setTimeout(res, ms));
      await delayPromis(2000);
      return {
        quote: without_right_space,
        quote_by: quote_by,
        explanation: data.explanation,
        error: false,
      };
    }
  } catch (error) {
    // Log errors
    console.error(error);
    return {
      quote: "Error fetching quote",
      error: true,
      quote_by: "Please try again later",
    };
  }
};
