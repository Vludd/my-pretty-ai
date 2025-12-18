export const API_BASE_URL = "/api/v1";

export async function fetchWithRetry(
  url: string,
  options: RequestInit = {},
  retries = 3,
  delay = 500,
  timeout = 5000
): Promise<Response> {
  for (let attempt = 1; attempt <= retries; attempt++) {
    try {

      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), timeout);

      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
      });

      clearTimeout(timer);

      if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
      }

      return response;
    } catch (error) {
      const isLast = attempt === retries;

      const isAbort = error instanceof DOMException && error.name === "AbortError";

      if (isLast) {
        throw new Error(
          isAbort
            ? `Request timeout after ${retries} attempts`
            : `Request failed after ${retries} attempts: ${String(error)}`
        );
      }

      await new Promise((res) => setTimeout(res, delay));
    }
  }

  throw new Error("Unreachable");
}
