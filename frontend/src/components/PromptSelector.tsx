import { useEffect, useState } from "react";
import { ChevronDown } from "lucide-react";

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
import type { PromptModel } from "@/types/Prompt";
// import { useNavigate } from "react-router-dom";

interface PromptSelectorProps {
  prompts: PromptModel[]
  loading?: boolean
  hidden?: boolean
}

export default function PromptSelector({ prompts, hidden }: PromptSelectorProps) {
  // const navigate = useNavigate();
  const [selectedPrompt, setSelectedPrompt] = useState<string>("")

  const handlePromptSelect = (promptName: string) => {
    const foundPrompt = prompts.find((p) => p.name === promptName)
    if (foundPrompt) {
      setSelectedPrompt(foundPrompt.name)
    }
  }

  // const handlePromptEdit = (promptId: string) => {
  //   navigate(`/prompts/edit/${promptId}`)
  // }

  useEffect(() => {
    setSelectedPrompt(prompts.length > 0 ? prompts[0].name : "")
  }, [prompts])

  return (
    <div>
      <DropdownMenu>
        <DropdownMenuTrigger asChild hidden={hidden}>
          <Button variant="ghost" className="flex items-center gap-1 p-0 h-8">
            <p>{selectedPrompt || "No Selected Prompt"}</p>
            <ChevronDown className="ml-auto w-4 h-4" />
          </Button>
        </DropdownMenuTrigger>

        <DropdownMenuContent align="center" className="p-2">
          {prompts.length === 0 ? (
            <div className="p-4 text-sm text-muted-foreground">
              No prompts available
            </div>
          ) : (
            <>
              <DropdownMenuRadioGroup
                value={selectedPrompt}
                onValueChange={handlePromptSelect}
              >
                {prompts.filter(p => p.isDefault).map((prompt) => (
                  <DropdownMenuRadioItem key={prompt.name} value={prompt.name}>
                    {prompt.name}
                  </DropdownMenuRadioItem>
                ))}

                {prompts.length > 1 && (
                  <>
                    <DropdownMenuSeparator />
                    <DropdownMenuLabel>Custom Prompts</DropdownMenuLabel>
                    <div className="flex flex-col gap-2 w-full pb-2">
                      {prompts.filter(p => !p.isDefault).map(prompt => (
                        <div className="flex gap-2">
                          <DropdownMenuRadioItem key={prompt.name} value={prompt.name} className="w-full">
                            <span>{prompt.name}</span>
                          </DropdownMenuRadioItem>
                          {/* <Button
                            size="icon"
                            className="w-8 h-8"
                            variant="secondary"
                            onClick={() => { handlePromptEdit(prompt.id) }}
                          >
                            <Edit className="w-4 h-4" />
                          </Button> */}
                        </div>
                      ))}
                    </div>
                  </>
                )}
              </DropdownMenuRadioGroup>
              
            </>
          )}

          <DropdownMenuSeparator />

          <div className="p-4 flex flex-row justify-center items-center">
            <Button
              variant="outline"
            >
              New prompt
            </Button>
          </div>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
}