import { getUserPrompt } from "@/api/prompts";
import { Footer } from "@/components/layout/Footer";
import { Header } from "@/components/layout/Header";
import { Button } from "@/components/ui/button";

import { 
  Card, 
  CardContent, 
  CardFooter
} from "@/components/ui/card";

import { Checkbox } from "@/components/ui/checkbox";

import { 
  Dialog, 
  DialogClose, 
  DialogContent, 
  DialogDescription, 
  DialogFooter,
  DialogHeader, 
  DialogTitle, 
  DialogTrigger 
} from "@/components/ui/dialog";

import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { SidebarTrigger } from "@/components/ui/sidebar";
import { Spinner } from "@/components/ui/spinner";
import { Textarea } from "@/components/ui/textarea";
import { useUser } from "@/context/useUser";

import type { 
  PromptModel,
} from "@/types/Prompt";
import { isDefaultLayer, isSelectableLayer } from "@/utils/typeOfLayer";
import { ChevronLeft } from "lucide-react";

import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

export const PromptEditorPage = () => {
  const { userId } = useUser();
  const { promptId } = useParams();

  const [unsaved, setUnsaved] = useState(false);
  const [fetchingPrompt, setFetchingPrompt] = useState(true);
  const [prompt, setPrompt] = useState<PromptModel>();

  useEffect(() => {
    getUserPrompt(userId, promptId || "")
    .then((res) => {
      setPrompt(res);
    })
    .finally(() => {
      setFetchingPrompt(false);
    })
  }, [userId, promptId])

  const handleEditField = (value: string) => {
    setPrompt(prev => prev ? { ...prev, name: value } : prev);
    setUnsaved(true);
  }

  const handleChangeEnabled = (checked: boolean, layerName: string) => {
    setPrompt(prev => {
      if (!prev) return prev;

      const updatedLayers = prev.layers.map(layer =>
        layer.name === layerName
          ? { ...layer, enabled: checked }
          : layer
      );

      return {
        ...prev,
        layers: updatedLayers,
      };
    });

    setUnsaved(true);
  }

  const handleChangeMultiple = (checked: boolean, layerName: string) => {
    setPrompt(prev => {
      if (!prev) return prev;

      const updatedLayers = prev.layers.map(layer =>
        layer.name === layerName
          ? { ...layer, multiple: checked }
          : layer
      );

      return {
        ...prev,
        layers: updatedLayers,
      };
    });

    setUnsaved(true);
  };

  const handleSave = async () => {
    if (!prompt) return;
    setUnsaved(false);
  }
  
  return (
    <div>
      <Header>
        
      </Header>

      <div className="flex flex-col gap-4 max-w-3xl mx-auto p-4">
        <h1 className="text-2xl font-bold">Prompt Editor</h1>
        {fetchingPrompt ? (
          <div className="flex items-center justify-center">
            <Spinner />
          </div>
        ) : (
          <Card>
            <CardContent className="flex flex-col gap-2">
              <div className="flex flex-col items-left justify-between gap-2">
                <div className="flex flex-col gap-4">
                  <div className="flex flex-col gap-2">
                    <Label htmlFor="prompt_name">Name</Label>
                    <Input 
                      id="prompt_name"
                      value={prompt?.name ?? ""} 
                      onChange={(e) => {handleEditField(e.target.value)}}
                    />
                  </div>
                  <Separator />
                  <div className="flex flex-col gap-4">
                    <Label>Active Layers</Label>
                    <div className="flex flex-col gap-2">
                      {prompt?.layers.map(layer => (
                        <Dialog>
                          <form>
                            <div className="flex justify-between items-center" key={layer.name}>
                              <div className="flex items-start gap-3">
                                <Checkbox 
                                  id={layer.name}
                                  checked={layer.enabled}
                                  onCheckedChange={(checked) => 
                                    handleChangeEnabled(!!checked, layer.name)
                                  }
                                />
                                {isDefaultLayer(layer) ? (
                                  <div>
                                    <Label htmlFor={layer.name}>{layer.name}</Label>
                                  </div>
                                ) : isSelectableLayer(layer) && (
                                  <div>
                                    <div className="grid gap-2">
                                      <Label htmlFor={layer.name}>{layer.name}</Label>
                                      <p className="text-muted-foreground text-sm">
                                        {`Options: ${layer.options.length}`}
                                        {layer.multiple && <span> (Multiple)</span>}
                                      </p>
                                    </div>
                                  </div>
                                )}
                              </div>
                              <DialogTrigger asChild>
                                <Button className="mt-2" size="sm" variant="outline">
                                  Edit
                                </Button>
                              </DialogTrigger>
                              <DialogContent className="sm:max-w-[425px]">
                                <DialogHeader>
                                  <DialogTitle>Edit layer</DialogTitle>
                                  <DialogDescription>
                                    Make changes to your layer here. Click save when you&apos;re
                                    done.
                                  </DialogDescription>
                                </DialogHeader>
                                {isDefaultLayer(layer) ? (
                                  <div className="grid gap-4">
                                    <div className="grid gap-3">
                                      <Label htmlFor="layer-name">Name</Label>
                                      <Input id="layer-name" name="name" value={layer.name ?? ""} />
                                    </div>

                                    <div className="grid gap-3">
                                      <Label htmlFor="layer-prompt">Prompt</Label>
                                      <Textarea id="layer-prompt" name="prompt" value={layer.prompt ?? ""} />
                                      <p className="text-muted-foreground text-sm">
                                        You can use <b>Markdown</b> formatting - the LLM will understand this format. 
                                        But Markdown is not yet supported by the interface
                                      </p>
                                    </div>

                                  </div>
                                ) : isSelectableLayer(layer) && (
                                  <div>
                                    <div className="grid gap-4">
                                      <div className="grid gap-3">
                                        <Label htmlFor="layer-name">Name</Label>
                                        <Input id="layer-name" name="name" value={layer.name ?? ""} />
                                      </div>

                                      <div className="grid gap-3">
                                        <div className="flex items-center justify-between">
                                          <Label htmlFor="layer-options">Options</Label>
                                          <div className="flex items-center gap-2">
                                            <Checkbox 
                                              id="layer-multiple"
                                              checked={layer.multiple}
                                              onCheckedChange={(checked) => handleChangeMultiple(!!checked, layer.name)}
                                            />
                                            <Label htmlFor="layer-multiple">Is multiple</Label>
                                          </div>
                                        </div>
                                        <div className="grid gap-3">
                                          {layer.options.map((option) => (
                                            <div className="flex flex-col gap-2">
                                              <div className="flex flex-row gap-2">
                                                <Checkbox 
                                                  id={`option-${option.name}`}
                                                  checked={option.selected}
                                                />
                                                <Label htmlFor={`option-${option.name}`}>{option.name}</Label>
                                              </div>
                                              <Textarea id={`option-${option.name}`} name="multiple" value={option.prompt} />
                                            </div>
                                          ))}
                                          <p className="text-muted-foreground text-sm">
                                            You can use <b>Markdown</b> formatting - the LLM will understand this format. 
                                            But Markdown is not yet supported by the interface
                                          </p>
                                        </div>
                                      </div>
                                    </div>
                                  </div>
                                )}
                                <DialogFooter>
                                  <DialogClose asChild>
                                    <Button variant="outline">Cancel</Button>
                                  </DialogClose>
                                  <Button type="submit">Save</Button>
                                </DialogFooter>
                              </DialogContent>
                            </div>
                          </form>
                        </Dialog>
                      ))}
                    </div>
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
        )}
      </div>

      <Footer>
      </Footer>
    </div>
  );
};
