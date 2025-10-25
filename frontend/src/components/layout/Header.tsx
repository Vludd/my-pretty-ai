import { ModeToggle } from "@/components/mode-toggle";

export const Header = () => (
  <header className="flex items-center justify-between px-4 py-2 border-b">
    <h1 className="text-lg font-semibold">My Pretty AI</h1>
    <ModeToggle />
  </header>
);