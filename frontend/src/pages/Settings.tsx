import LanguageDropdown from "@/components/LanguageDropdown";
import { Header } from "@/components/layout/Header";
import { ModeSelector } from "@/components/mode-selector";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter, CardTitle } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";
import { SidebarTrigger } from "@/components/ui/sidebar";
import { promptLayers } from "@/data/promptLayers";

const languages = [
  "English",
];

export default function Settings() {
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
        <Card>
          <CardTitle className="px-4">Prompt Manager (In dev)</CardTitle>
          <CardContent className="flex flex-col gap-4">
            <div className="flex flex-col gap-4">
              {promptLayers.map(layer => (
                <div className="flex justify-between items-start" key={layer.id}>
                  <div className="flex items-start gap-3">
                    <Checkbox id={layer.id} defaultChecked={layer.enabled} disabled={!layer.editable} />
                    <div className="grid gap-2">
                      <Label htmlFor={layer.id}>{layer.name}</Label>
                      <p className="text-muted-foreground text-sm">
                        {layer.description}
                      </p>
                    </div>
                  </div>
                  {layer.editable && (
                    <Button 
                      className="mt-2" 
                      size="sm" 
                      variant="outline" 
                    >
                      Edit
                    </Button>
                  )}
                </div>
              ))}
            </div>
          </CardContent>
          <CardFooter className="flex justify-end gap-2">
            <Button variant="ghost">Reset</Button>
            <Button variant="default" disabled>Save</Button>
          </CardFooter>
        </Card>
        <p className="text-muted-foreground text-xs text-center">
          MyPrettyAI v{__APP_VERSION__}
        </p>
      </div>
    </div>
  );
}
