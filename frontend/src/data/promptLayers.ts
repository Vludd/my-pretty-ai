import type { PromptLayer } from "@/types/Prompt";

export const promptLayers: PromptLayer[] = [
  {
    id: "system",
    type: "default",
    name: "System",
    description: "This is the base prompt layer.",
    prompt: "",
    enabled: true,
  },
  {
    id: "about",
    type: "default",
    name: "About",
    description: "Provides context about the user.",
    prompt: "",
    enabled: true,
  },
  {
    id: "rules",
    type: "default",
    name: "Communication Rules",
    description: "Defines the style of communication.",
    prompt: "",
    enabled: true,
  },
  {
    id: "relationship",
    type: "selectable",
    name: "Relationship",
    description: "Defines the relationship with the user.",
    prompt: "",
    options: [
      {
        id: "stranger",
        name: "Stranger",
        description: "You are a stranger to the user.",
        prompt: "",
        selected: true
      },
      {
        id: "friend",
        name: "Friend",
        description: "You are a close friend of the user.",
        prompt: "",
        selected: true
      },
    ],
    enabled: true,
  }
];
