import { BackButton } from "@/components/layout/BackButton";
import { Footer } from "@/components/layout/Footer";
import { Header } from "@/components/layout/Header";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { SidebarTrigger } from "@/components/ui/sidebar";
import { Textarea } from "@/components/ui/textarea";
import { promptLayers } from "@/data/promptLayers";
// import { useUser } from "@/context/useUser";
import type { DefaultPromptLayer, PromptLayer, PromptModel } from "@/types/Prompt";
import { ChevronLeft } from "lucide-react";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

export const PromptCreator = () => {
  // const { userId } = useUser();

  const [layers, setLayers] = useState<PromptLayer>();

  const [unsaved, setUnsaved] = useState(false);
  const [prompt, setPrompt] = useState<PromptModel>();

  const handleSave = async () => {
    if (!prompt) return;
    setUnsaved(false);
  }

  return (
    <div>
      <Header className="justify-start">
          <SidebarTrigger />
          <BackButton text="Back to Settings" to="/settings" />
      </Header>

      <div className="flex flex-col gap-4 max-w-3xl mx-auto p-4">
        <h1 className="text-2xl font-bold">New Prompt</h1>
        <Card>
          <CardContent className="flex flex-col gap-2">
            <div className="flex flex-col items-left justify-between gap-2">
              <div className="flex flex-col gap-4">
                <div className="flex flex-col gap-2">
                  <Label htmlFor="prompt_name">Name</Label>
                  <Input 
                    id="prompt_name"
                    value={prompt?.name ?? ""}
                  />
                </div>
                <Separator />
                <div className="flex flex-col gap-4">
                  <Card>
                    <CardHeader>
                      <Label>Layer Name</Label>
                      <Input></Input>
                    </CardHeader>
                    <CardContent>
                      <div className="grid gap-2">
                        <Label>Layer Prompt</Label>
                        <Textarea className="min-h-24 max-h-48"></Textarea>
                      </div>
                    </CardContent>
                  </Card>
                  <Button className="mt-2" variant="ghost">Add Layer</Button>
                </div>
              </div>
            </div>
          </CardContent>
          <CardFooter className="flex items-center justify-between gap-2">
            <Button
              variant={"destructive"}
            >
              Delete
            </Button>
            <div className="flex items-center justify-end gap-2">
              <Button variant="secondary">Cancel</Button>
              <Button variant="default" disabled={!unsaved} onClick={handleSave}>Save</Button>
            </div>
          </CardFooter>
        </Card>
      </div>
      <Footer>

      </Footer>
    </div>
  );
};