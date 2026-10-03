import { createGoogleGenerativeAI } from '@ai-sdk/google'
import { streamText, generateText } from 'ai'
import { NextResponse } from 'next/server'

export const maxDuration = 30

const google = createGoogleGenerativeAI({
  apiKey: process.env.GOOGLE_GENERATIVE_AI_API_KEY,
})

const PRODUCT_CATALOG = `
- Lenovo IdeaPad Slim 5 (Electronics): ₹58,990
- boAt Airdopes 141 (Electronics): ₹1,299
- Noise ColorFit Pro 5 (Electronics): ₹2,999
- Nike Air Force 1 (Fashion): ₹7,999
- Skybags Crew Backpack (Fashion): ₹1,899
- Apple iPhone 15 (Electronics): ₹69,900
- Sony WH-1000XM5 (Electronics): ₹29,990
- Samsung Galaxy S24 (Electronics): ₹74,999
- Levi's Denim Jacket (Fashion): ₹3,499
- Casio Vintage Watch (Fashion): ₹1,695
- Nintendo Switch OLED (Toys & Games): ₹34,990
- Adidas Ultraboost (Sports & Fitness): ₹11,999
`

const SYSTEM_PROMPT = `You are a helpful NovaMart AI Support Agent. You assist with order tracking, returns, and products.
Here is the available product catalog and prices:
${PRODUCT_CATALOG}

Keep your answers concise, accurate, and polite. Only recommend products from the catalog above.`

export async function POST(req: Request) {
  try {
    const body = await req.json()
    
    // Check if request is from SupportWidget (expects JSON response)
    if (body.message && body.customer_id) {
      const { text } = await generateText({
        model: google('gemini-3.8-flash'),
        system: SYSTEM_PROMPT,
        prompt: body.message,
      })
      
      return NextResponse.json({
        reply: text,
        decisions: [{ intent: 'ai_support', move: 'ANSWER', reason_code: 'ai_generated', policy_ref: 'AI Knowledge' }],
        trace: {
          understanding: { intents: ['ai_support'], raw_message: body.message },
          verification: { customer_status: 'active' }
        },
        metrics: { llm_calls: 1, total_latency_ms: 1500 }
      })
    }

    // Otherwise, assume it's from useChat (expects Streaming response)
    if (body.messages) {
      const result = await streamText({
        model: google('gemini-3.8-flash'),
        system: SYSTEM_PROMPT,
        messages: body.messages,
      })
      return result.toDataStreamResponse()
    }

    return NextResponse.json({ error: "Invalid request format" }, { status: 400 })

  } catch (error: unknown) {
    const msg = error instanceof Error ? error.message : 'Internal Server Error'
    return NextResponse.json({ error: msg }, { status: 500 })
  }
}
