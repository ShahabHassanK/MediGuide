import { useState, useRef, useCallback } from 'react'
import { sendChat } from '../lib/api'

export type MessageRole = 'user' | 'assistant' | 'system'

export interface Message {
  id: string
  role: MessageRole
  content: string
  timestamp: Date
}

function makeId() {
  return `msg_${Date.now()}_${Math.random().toString(36).slice(2, 7)}`
}

export function useChat(sessionId: string) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: makeId(),
      role: 'assistant',
      content:
        "Hello! I'm **MediGuide**, your AI medical information assistant. I can help you understand symptoms, conditions, medications, and treatments based on trusted medical sources.\n\n> **Disclaimer:** I provide general health information only — always consult a qualified healthcare professional for medical advice, diagnosis, or treatment.",
      timestamp: new Date(),
    },
  ])
  const [isLoading, setIsLoading] = useState(false)
  const abortRef = useRef<AbortController | null>(null)

  const addMessage = useCallback((role: MessageRole, content: string) => {
    const msg: Message = { id: makeId(), role, content, timestamp: new Date() }
    setMessages((prev) => [...prev, msg])
    return msg
  }, [])

  const send = useCallback(
    async (text: string) => {
      if (!text.trim() || isLoading) return
      addMessage('user', text)
      setIsLoading(true)
      abortRef.current = new AbortController()
      try {
        const data = await sendChat(sessionId, text)
        addMessage('assistant', data.response)
      } catch (err: unknown) {
        const msg = err instanceof Error ? err.message : 'Unknown error'
        addMessage('system', `Error: ${msg}`)
      } finally {
        setIsLoading(false)
      }
    },
    [sessionId, isLoading, addMessage],
  )

  const injectUserMessage = useCallback(
    (content: string) => addMessage('user', content),
    [addMessage],
  )

  const injectAssistantMessage = useCallback(
    (content: string) => addMessage('assistant', content),
    [addMessage],
  )

  const clearMessages = useCallback(() => {
    setMessages([
      {
        id: makeId(),
        role: 'assistant',
        content:
          "Hello! I'm **MediGuide**, your AI medical information assistant. How can I help you today?",
        timestamp: new Date(),
      },
    ])
  }, [])

  return {
    messages,
    isLoading,
    send,
    injectUserMessage,
    injectAssistantMessage,
    clearMessages,
  }
}
