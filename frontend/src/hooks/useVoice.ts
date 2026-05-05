import { useState, useRef, useCallback } from 'react'
import { voiceConversation } from '../lib/api'

export type VoiceState = 'idle' | 'recording' | 'processing'

interface UseVoiceOptions {
  sessionId: string
  onTranscript: (text: string) => void
  onResponse: (text: string) => void
  onError: (msg: string) => void
}

export function useVoice({ sessionId, onTranscript, onResponse, onError }: UseVoiceOptions) {
  const [voiceState, setVoiceState] = useState<VoiceState>('idle')
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const chunksRef = useRef<Blob[]>([])

  const startRecording = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const mimeType = MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
        ? 'audio/webm;codecs=opus'
        : 'audio/webm'
      const mr = new MediaRecorder(stream, { mimeType })
      chunksRef.current = []
      mr.ondataavailable = (e) => {
        if (e.data.size > 0) chunksRef.current.push(e.data)
      }
      mr.onstop = async () => {
        stream.getTracks().forEach((t) => t.stop())
        const blob = new Blob(chunksRef.current, { type: mimeType })
        setVoiceState('processing')
        try {
          const data = await voiceConversation(sessionId, blob)
          onTranscript(data.transcript)
          onResponse(data.response)
          // Play audio response
          if (data.audio_b64) {
            const bytes = Uint8Array.from(atob(data.audio_b64), (c) => c.charCodeAt(0))
            const audioBlob = new Blob([bytes], { type: 'audio/mpeg' })
            const url = URL.createObjectURL(audioBlob)
            const audio = new Audio(url)
            audio.onended = () => URL.revokeObjectURL(url)
            audio.play().catch(() => {})
          }
        } catch (err: unknown) {
          onError(err instanceof Error ? err.message : 'Voice processing failed')
        } finally {
          setVoiceState('idle')
        }
      }
      mediaRecorderRef.current = mr
      mr.start()
      setVoiceState('recording')
    } catch {
      onError('Microphone access denied. Please allow microphone permission.')
    }
  }, [sessionId, onTranscript, onResponse, onError])

  const stopRecording = useCallback(() => {
    if (mediaRecorderRef.current && voiceState === 'recording') {
      mediaRecorderRef.current.stop()
    }
  }, [voiceState])

  const toggleRecording = useCallback(() => {
    if (voiceState === 'idle') startRecording()
    else if (voiceState === 'recording') stopRecording()
  }, [voiceState, startRecording, stopRecording])

  return { voiceState, toggleRecording, startRecording, stopRecording }
}
