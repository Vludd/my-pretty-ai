import { getUserPrompt } from "@/api/prompts";
import { Header } from "@/components/layout/Header";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { SidebarTrigger } from "@/components/ui/sidebar";
import { Spinner } from "@/components/ui/spinner";
import { Textarea } from "@/components/ui/textarea";
import { useUser } from "@/context/useUser";
import type { PromptModel } from "@/types/Prompt";
import { isDefaultLayer, isSelectableLayer } from "@/utils/typeOfLayer";
import { ChevronLeft } from "lucide-react";
import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";

export const PromptPreview = () => {
  const { userId } = useUser();
  const navigate = useNavigate();
  const { promptId } = useParams();
  
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

  const handleEdit = async () => {
    navigate(`/p/edit/${promptId}`);
  };

  return (
    <div>
      <Header className="flex items-center justify-start">
        <SidebarTrigger />
        <Link 
          to="/settings" 
          className="text-sm text-muted-foreground flex items-center whitespace-nowrap"
        >
          <ChevronLeft className="w-5 h-5 shrink-0" strokeWidth={2.5} />
          <span className="">Back to Settings</span>
        </Link>
      </Header>

      <div className="flex flex-col gap-4 max-w-3xl mx-auto p-4">
        <h1 className="text-2xl font-bold">Prompt Info</h1>
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
                      readOnly
                    />
                  </div>
                  <Separator />
                  <div className="flex flex-col gap-4">
                    <div className="flex flex-col gap-2">
                      {prompt?.layers.map((layer, index) => (
                        <div>
                          {isDefaultLayer(layer) ? (
                            <div className="grid gap-2">
                              <Label 
                                htmlFor={`${layer.name}`}
                                className=""
                              >{`Layer: ${layer.name}`}</Label>
                              <Textarea
                                id={layer.name}
                                className="w-full min-h-24"
                                value={layer.prompt}
                              />
                            </div>
                          ) : isSelectableLayer(layer) && (
                            <div>
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
            <CardFooter className="flex items-center justify-between gap-2">
              <Button
                variant={"destructive"}
                disabled={prompt?.isDefault}
              >
                Delete
              </Button>
              <Button variant="default" disabled={prompt?.isDefault} onClick={() => handleEdit}>Edit</Button>
            </CardFooter>
          </Card>
        )}
      </div>
    </div>
  );
};