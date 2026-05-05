import { Mic, MicOff, Loader2 } from 'lucide-react'
import type { VoiceState } from '../hooks/useVoice'

interface VoiceButtonProps {
  voiceState: VoiceState
  onToggle: () => void
}

export function VoiceButton({ voiceState, onToggle }: VoiceButtonProps) {
  const isRecording = voiceState === 'recording'
  const isProcessing = voiceState === 'processing'
  const disabled = isProcessing

  return (
    <button
      onClick={onToggle}
      disabled={disabled}
      title={
        isRecording
          ? 'Stop recording'
          : isProcessing
            ? 'Processing…'
            : 'Start voice conversation'
      }
      className={`
        relative w-10 h-10 rounded-xl flex items-center justify-center transition-all duration-200 shrink-0
        ${isRecording ? 'bg-red-500/20 border border-red-500/50 recording-pulse' : ''}
        ${isProcessing ? 'bg-violet-500/10 border border-violet-500/30 cursor-not-allowed opacity-60' : ''}
        ${!isRecording && !isProcessing ? 'glass hover:bg-white/[0.08] hover:border-violet-500/30' : ''}
      `}
    >
      {isProcessing ? (
        <Loader2 size={18} className="text-violet-400 animate-spin" />
      ) : isRecording ? (
        <MicOff size={18} className="text-red-400" />
      ) : (
        <Mic size={18} className="text-white/60" />
      )}
    </button>
  )
}
