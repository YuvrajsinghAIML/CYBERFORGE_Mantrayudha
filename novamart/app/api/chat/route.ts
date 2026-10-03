import { streamText } from 'ai';
import { google } from '@ai-sdk/google';

// Allow streaming responses up to 30 seconds
export const maxDuration = 30;

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: google('gemini-3.8-flash'),
    system: "You are a helpful and friendly support bot for NovaMart, an e-commerce store offering fast delivery, easy returns, and 24x7 support. Keep your answers concise, helpful, and polite. If you don't know the answer, say so.",
    messages,
  });

  return result.toUIMessageStreamResponse ? result.toUIMessageStreamResponse() : (result as any).toTextStreamResponse();
}
