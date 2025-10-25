import { Button } from "@/components/ui/button";
import { Reply, Copy, Volume2 } from "lucide-react";
import { useCallback, useState } from "react";

export const MessageActions = ({ text, isUser }: { text: string, isUser?: boolean }) => {
  const [playing, setPlaying] = useState(false);

  const handleCopy = useCallback(async () => {
    try {
      if (navigator.clipboard?.writeText) {
        await navigator.clipboard.writeText(text);
      } else {
        // fallback
        const ta = document.createElement("textarea");
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand("copy");
        ta.remove();
      }
      // можно тут показывать toast / визуальную индикацию
    } catch (e) {
      console.error("Copy failed", e);
    }
  }, [text]);

  const handleSpeak = useCallback(async () => {
    if (!text) return;
    setPlaying(true);
    try {
      // Подстройте endpoint под ваш бэкенд (например /api/v1/tts)
      const res = await fetch(`/tts/generate?text=${text}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" }
      });

      if (!res.ok) throw new Error("TTS request failed");

      // ожидаем бинарный поток (audio/*)
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const audio = new Audio(url);
      audio.onended = () => {
        URL.revokeObjectURL(url);
        setPlaying(false);
      };
      audio.onerror = () => {
        URL.revokeObjectURL(url);
        setPlaying(false);
      };
      await audio.play();
    } catch (e) {
      console.error("Speak failed", e);
      setPlaying(false);
    }
  }, [text]);
  return (
    <div
      className={`absolute bottom-1 flex gap-1 px-2 opacity-0 group-hover:opacity-100 transition-opacity 
      ${isUser ? "right-0 translate-x-full pr-2" : "left-0 -translate-x-full pl-2"}`}
    >
      <Button size="icon" variant="ghost" className="h-7 w-7">
        <Reply className="h-4 w-4" />
      </Button>
      <Button size="icon" variant="ghost" onClick={handleCopy} className="h-7 w-7">
        <Copy className="h-4 w-4" />
      </Button>
      {!isUser && (
        <Button 
          size="icon" 
          variant="ghost" 
          className="h-7 w-7"
          onClick={handleSpeak}
          aria-label="Speak"
          disabled={playing}
        >
          <Volume2 className="h-4 w-4" />
        </Button>
      )}
    </div>
  );
};