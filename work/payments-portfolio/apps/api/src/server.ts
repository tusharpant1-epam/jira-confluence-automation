import app from "./app.js";

const port = Number(process.env.API_PORT ?? 3001);

if (!Number.isInteger(port) || port < 1 || port > 65535) {
  throw new Error("API_PORT must be an integer between 1 and 65535");
}

const server = app.listen(port, "127.0.0.1", () => {
  console.info(`API listening at http://127.0.0.1:${port}`);
});

server.on("error", (error: Error) => {
  console.error("API server failed to start", error);
  process.exitCode = 1;
});
