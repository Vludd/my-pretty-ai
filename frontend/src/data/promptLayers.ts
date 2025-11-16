import type { PromptLayer } from "@/types/Prompt";

export const promptLayers: PromptLayer[] = [
  {
    id: "system",
    name: "System",
    description: "This is the base prompt layer.",
    prompt: "",
    editable: false,
    enabled: true,
  },
  {
    id: "about",
    name: "About",
    description: "Provides context about the user.",
    prompt: "",
    editable: true,
    enabled: true,
  },
  {
    id: "rules",
    name: "Communication Rules",
    description: "Defines the style of communication.",
    prompt: "",
    editable: true,
    enabled: true,
  },
  {
    id: "safety",
    name: "Safety",
    description: "Ensures responses are safe and appropriate.",
    prompt: "",
    editable: false,
    enabled: false,
  },
  {
    id: "personality",
    name: "Personality",
    description: "Ensures responses are safe and appropriate.",
    options: [
      {
        id: "friendly",
        name: "Friendly",
        description: "Responds in a friendly manner.",
        prompt: "",
        editable: true,
        selected: true
      },
    ],
    editable: true,
    enabled: true,
  },
  {
    id: "relationship",
    name: "Relationship",
    description: "Defines the relationship with the user.",
    options: [
      {
        id: "stranger",
        name: "Stranger",
        description: "You are a stranger to the user.",
        prompt: "",
        editable: true,
        selected: true
      },
      {
        id: "friend",
        name: "Friend",
        description: "You are a close friend of the user.",
        prompt: "",
        editable: false,
        selected: true
      },
    ],
    editable: true,
    enabled: true,
  },
  {
    id: "context",
    name: "Context",
    description: "Provides additional context for responses.",
    prompt: "",
    editable: true,
    enabled: false,
  },
  {
    id: "interests",
    name: "Interests",
    description: "Incorporates user's interests into responses.",
    accentPrompt: "",
    prompts: [
      {
        name: "Music",
        prompt: "",
      },
      {
        name: "Books",
        prompt: "",
      },
      {
        name: "Movies",
        prompt: "",
      },
      {
        name: "Hobbies",
        prompt: "",
      },
      {
        name: "Games",
        prompt: "",
      }
    ],
    editable: true,
    enabled: false,
  },
  {
    id: "time_context",
    name: "Time Context",
    description: "Keeps responses relevant to current time.",
    prompts: [
      {
        name: "Morning",
        prompt: "Good morning! How can I assist you today?"
      },
      {
        name: "Afternoon",
        prompt: "Good afternoon! What would you like to talk about?"
      },
      {
        name: "Evening",
        prompt: "Good evening! How was your day?"
      },
      {
        name: "Night",
        prompt: "It's late! Need any help before you sleep?"
      },
      {
        name: "Long absence",
        prompt: "Welcome back! I've missed our conversations."
      }
    ],
    editable: true,
    enabled: true,
  },
  {
    id: "erotic",
    name: "Erotic Context",
    description: "Incorporates erotic elements into responses.",
    accentPrompt: "",
    prompt: "",
    editable: false,
    enabled: false,
  }
];