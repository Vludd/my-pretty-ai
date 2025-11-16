export function formatTime(iso: string) {
  // "2025-10-23T23:43:09.711555Z" -> "11:43 PM"
  return new Date(iso).toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });
}