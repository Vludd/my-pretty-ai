import { useState } from "react";
import { ChevronDown, Download } from "lucide-react";

import { Button } from "@/components/ui/button";

import { 
  DropdownMenu, 
  DropdownMenuLabel, 
  DropdownMenuSeparator, 
  DropdownMenuContent,
  DropdownMenuTrigger, 
  DropdownMenuRadioItem,
  DropdownMenuRadioGroup
} from "@/components/ui/dropdown-menu";
import type { AIModel } from "@/types/AiModel";

interface ModelSelectorProps {
  models: AIModel[]
  hidden?: boolean
}

export default function ModelSelector({ models, hidden }: ModelSelectorProps) {
  const [selectedModel, setSelectedModel] = useState<string>("")

  const handleModelSelect = (modelTitle: string) => {
    const foundModel = models.find((m) => m.title === modelTitle)
    if (foundModel) {
      setSelectedModel(foundModel.title)
    }
  }

  return (
    <div>
      <DropdownMenu>
        <DropdownMenuTrigger asChild hidden={hidden}>
          <Button variant="ghost" className="flex items-center gap-1 p-0 h-8">
            <p>{selectedModel || "No Model Loaded"}</p>
            <ChevronDown className="ml-auto w-4 h-4" />
          </Button>
        </DropdownMenuTrigger>

        <DropdownMenuContent align="end">
          <DropdownMenuLabel>AI Models</DropdownMenuLabel>

          {models.length === 0 ? (
            <div className="p-4 text-sm text-muted-foreground">
              No models available
            </div>
          ) : (
            <>
              {/* <DropdownMenuLabel>Installed</DropdownMenuLabel> */}
              <DropdownMenuSeparator />
              <DropdownMenuRadioGroup
                value={selectedModel}
                onValueChange={handleModelSelect}
              >
                {models.filter(m => m.downloaded).map(model => (
                  <DropdownMenuRadioItem key={model.title} value={model.title}>
                    {model.title}
                  </DropdownMenuRadioItem>
                ))}
              </DropdownMenuRadioGroup>
              <DropdownMenuSeparator />

              <DropdownMenuLabel>Available for download</DropdownMenuLabel>
              {models.filter(m => !m.downloaded).map((model) => (
                <div key={model.title} className="flex items-center justify-between px-2 py-1.5">
                  <span className="text-muted-foreground">{model.title}</span>
                  <Button
                    size="icon"
                    variant="ghost"
                    onClick={() => { console.log("Downloading:", model.title) }}
                  >
                    <Download className="w-4 h-4" />
                  </Button>
                </div>
              ))}
            </>
          )}
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
}