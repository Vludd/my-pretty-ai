import { Card, CardContent, CardFooter, CardTitle } from "@/components/ui/card";
import type { PromptModel } from "@/types/Prompt";
import { Button } from "@/components/ui/button";
import { ChevronRight } from "lucide-react";
import { useNavigate } from "react-router-dom";

interface Props {
  prompts: PromptModel[]
  loading?: boolean
}

export default function PromptManager({prompts, loading}: Props) {
  const navigate = useNavigate();

  const handlePreview = async (promptId: string) => {
    navigate(`/p/${promptId}`);
  }

  const handleEdit = async (promptId: string) => {
    navigate(`/p/edit/${promptId}`);
  };

  const handleNew = async () => {
    navigate(`/p/new`);
  }
  
  return (
    <>
      <Card>
        <CardTitle className="px-4">Prompt Manager</CardTitle>
        <CardContent className="flex flex-col gap-4">
          {prompts.length === 0 ? (
            <>
              <p>No prompts available</p>
            </>
          ) : ( 
            <>
              {prompts.map((prompt) => (
                <Button
                  variant={"secondary"} 
                  className="flex justify-between"
                  onClick={() => {handlePreview(prompt.id)}}
                >
                  <p>{prompt.name}</p>
                  <div className="flex items-center gap-2">
                    {prompt.isDefault && (
                      <span className="">Not editable</span>
                    )}<ChevronRight />
                  </div>
                </Button>
              ))}
            </>
          )}
        </CardContent>
        <CardFooter className="flex justify-end gap-2">
          <Button 
            variant={"default"}
            onClick={handleNew}
          >
            New Prompt
          </Button>
        </CardFooter>
      </Card>
    </>
  )
}