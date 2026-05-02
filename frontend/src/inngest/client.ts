// import { Inngest } from "inngest";

// // Create a client to send and receive events
// export const inngest = new Inngest({ id: "music-generator" });

import { Inngest } from "inngest";

export const inngest = new Inngest({ 
  id: "music-generator",
  eventKey: process.env.INNGEST_EVENT_KEY,
  baseUrl: process.env.INNGEST_BASE_URL,
});