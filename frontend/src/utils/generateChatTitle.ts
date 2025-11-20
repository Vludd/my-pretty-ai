export function generateChatTitle(message: string, maxLength = 50): string {
  const clean = message
    .trim()
    .replace(/\s+/g, " ");

  return clean.length > maxLength
    ? clean.slice(0, maxLength).trim() + "..."
    : clean;
}
