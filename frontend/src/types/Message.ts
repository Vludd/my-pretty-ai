export interface Message {
  public_id: string;
  sender_type: "ai" | "user";
  content: string;
  created_at: string;
  updated_at: string;
}