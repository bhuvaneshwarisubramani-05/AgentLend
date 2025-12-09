import axios from "axios";

// IMPORTANT — replace with your laptop IP!!
const BASE_URL = "http://127.0.0.1:8000/chat";

export async function sendMessage(message, memory = {}) {
  try {
    const res = await axios.post(BASE_URL, {
      message,
      memory
    });

    return res.data;
  } catch (err) {
    console.error("API Error:", err);
    return {
      response: { text: "Something went wrong!", type: "error" },
      memory
    };
  }
}
