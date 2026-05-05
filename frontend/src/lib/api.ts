const BASE = '/api'

export interface ChatResponse {
  session_id: string
  response: string
}

export interface TranscribeResponse {
  session_id: string
  transcript: string
}

export interface UploadResponse {
  session_id: string
  doc_id: string
  filename: string
  chunks_stored: number
}

export interface VoiceConversationResponse {
  session_id: string
  transcript: string
  response: string
  audio_b64: string
}

export async function sendChat(session_id: string, message: string): Promise<ChatResponse> {
  const res = await fetch(`${BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id, message }),
  })
  if (!res.ok) throw new Error(`Chat error: ${res.statusText}`)
  return res.json()
}

export async function transcribeAudio(session_id: string, blob: Blob): Promise<TranscribeResponse> {
  const form = new FormData()
  form.append('audio', blob, 'recording.webm')
  form.append('session_id', session_id)
  const res = await fetch(`${BASE}/voice/transcribe`, { method: 'POST', body: form })
  if (!res.ok) throw new Error(`Transcribe error: ${res.statusText}`)
  return res.json()
}

export async function synthesizeSpeech(session_id: string, text: string): Promise<ArrayBuffer> {
  const res = await fetch(`${BASE}/voice/synthesize`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id, text }),
  })
  if (!res.ok) throw new Error(`Synthesize error: ${res.statusText}`)
  return res.arrayBuffer()
}

export async function voiceConversation(
  session_id: string,
  blob: Blob,
): Promise<VoiceConversationResponse> {
  const form = new FormData()
  form.append('audio', blob, 'recording.webm')
  form.append('session_id', session_id)
  const res = await fetch(`${BASE}/voice/conversation`, { method: 'POST', body: form })
  if (!res.ok) throw new Error(`Voice conversation error: ${res.statusText}`)
  return res.json()
}

export async function uploadDocument(session_id: string, file: File): Promise<UploadResponse> {
  const form = new FormData()
  form.append('file', file)
  form.append('session_id', session_id)
  const res = await fetch(`${BASE}/documents/upload`, { method: 'POST', body: form })
  if (!res.ok) {
    const detail = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(detail.detail || res.statusText)
  }
  return res.json()
}
