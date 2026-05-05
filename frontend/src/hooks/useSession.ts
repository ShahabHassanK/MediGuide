import { useState } from 'react'

function generateId(): string {
  return `session_${Date.now()}_${Math.random().toString(36).slice(2, 9)}`
}

export function useSession() {
  const [sessionId] = useState<string>(() => {
    const stored = sessionStorage.getItem('mg_session_id')
    if (stored) return stored
    const id = generateId()
    sessionStorage.setItem('mg_session_id', id)
    return id
  })

  return { sessionId }
}
