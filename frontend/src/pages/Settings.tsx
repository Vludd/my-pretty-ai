import { getUserPrompts } from "@/api/prompts";
import LanguageDropdown from "@/components/LanguageDropdown";
import { Header } from "@/components/layout/Header";
import { ModeSelector } from "@/components/theme/mode-selector";
import PromptManager from "@/components/PromptManager";
import { Card, CardContent, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { SidebarTrigger } from "@/components/ui/sidebar";
import { useUser } from "@/context/useUser";
import type { PromptModel } from "@/types/Prompt";
import { useEffect, useState } from "react";

const languages = [
  "English",
];

export default function Settings() {
  const { userId } = useUser();
  const [prompts, setPrompts] = useState<PromptModel[]>([])
  const [promptsFetching, setPromptsFetching] = useState(true)

  useEffect(() => {
    getUserPrompts(userId)
    .then((res) => {
      setPrompts(res);
    })
    .finally(() => setPromptsFetching(false));
  }, [userId])

  return (
    <div>
      <Header>
        <SidebarTrigger />
      </Header>
      <div className="flex flex-col gap-4 max-w-3xl mx-auto p-4">
        <h1 className="text-2xl font-bold">Settings</h1>
        <Card>
          <CardTitle className="px-4">General</CardTitle>
          <CardContent className="flex flex-col gap-2">
            <div className="flex items-center justify-between">
              <div className="grid gap-2">
                <Label>Language</Label>
                <p className="text-muted-foreground text-sm">
                  Application language
                </p>
              </div>
              <LanguageDropdown languages={languages}/>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardTitle className="px-4">Appearance</CardTitle>
          <CardContent className="flex flex-col gap-4">
            <div className="flex items-center justify-between">
              <div className="grid gap-2">
                <Label>Theme</Label>
                <p className="text-muted-foreground text-sm">
                  Base application theme
                </p>
              </div>
              <ModeSelector />
            </div>
            <div className="flex items-center justify-between">
              <div className="grid gap-2">
                <Label>Color accent (In dev)</Label>
                <p className="text-muted-foreground text-sm">
                  Accent color for buttons and highlights
                </p>
              </div>
              <Label className="text-muted-foreground">Neutral</Label>
            </div>
          </CardContent>
        </Card>
        <PromptManager prompts={prompts} loading={promptsFetching}/>
        <p className="text-muted-foreground text-xs text-center">
          MyPrettyAI v{__APP_VERSION__}
        </p>
      </div>
    </div>
  );
}
