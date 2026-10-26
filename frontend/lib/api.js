export async function apiRequest(url, options = {}) {
  const apiBaseUrl =
    typeof window === "undefined"
      ? process.env.BACKEND_API_URL
      : process.env.NEXT_PUBLIC_API_URL;
  const requestUrl = url.startsWith("http") ? url : `${apiBaseUrl ?? ""}${url}`;
  const response = await fetch(requestUrl, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });
  const contentType = response.headers.get("content-type") ?? "";
  const payload = contentType.includes("application/json")
    ? await response.json()
    : null;

  if (!response.ok) {
    throw new Error(payload?.error ?? `Request failed with status ${response.status}`);
  }

  if (payload === null) {
    throw new Error("The server returned an unexpected response.");
  }

  return payload;
}

export function formatPrice(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(value);
}
