import axios from "axios";

const axiosClient = axios.create();

axiosClient.defaults.baseURL = "http://localhost:5000";

axiosClient.defaults.headers = {
  "Content-Type": "application/json",
  Accept: "application/json",
};

// All requests will wait 10 seconds before timing out
axiosClient.defaults.timeout = 10 * 1000;

axiosClient.defaults.withCredentials = true;

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
      const dummy_data = {
        quote:
          '"And he does live with the gods who constantly shows to them, his own soul is satisfied with that which is assigned to him, and that it does all that the daemon wishes, which Zeus hath given to every man for his guardian and guide, a portion of himself." --Marcus Aurelius, Meditations, Book 5',
      };
      const quote_data = await postRequest("process_quote", dummy_data);
      return quote_data.data;
    }
  } catch (error) {
    // Log errors
    console.error(error);
    return { quote: "Error fetching quote", error: true };
  }
};
