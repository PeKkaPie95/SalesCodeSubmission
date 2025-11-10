# LiveKit Voice Agent – Interruption Handling Enhancement

**Author:** Priyanshu M  
**Repository:** https://github.com/PeKkaPie95/SalesCodeSubmission

## Overview
This submission implements interruption-aware conversational behavior for a LiveKit-based voice agent. The agent should continue speaking when the user expresses hesitation (e.g., *“umm”*, *“haan”*, *“hmm”*), but should stop immediately when the user expresses meaningful intent to interrupt (e.g., *“wait”*, *“stop”*, *“one second”*).

This improves natural conversation flow and prevents accidental interruptions.

---

## Key Features Implemented
1. **Detects when the agent is currently speaking** using event hooks.
2. **Filters filler/hesitation words** using a configurable list:
3. **Uses ASR confidence scores** to ignore background noise.
4. **Immediately stops agent TTS** when a real interruption is detected:
```python
await session.agent.stop_speaking()

I have implemented interruption-aware voice handling for the LiveKit voice agent. 
The agent now ignores filler/hesitation words (e.g., “umm”, “hmm”, “haan”) *only while the agent is speaking*, 
but still allows the user to interrupt intentionally when meaning is detected (e.g., “stop”, “wait”, “one second”).

Key Points:
• No VAD or STT parameters were modified (as required)
• Filler list is configurable via environment variable (IGNORED_FILLERS)
• Confidence threshold filters out noise
• Real interruptions cause immediate TTS stop using session.agent.stop_speaking()
• Behavior is tested locally using test_filler_interrupts.py

Repository:
https://github.com/PeKkaPie95/SalesCodeSubmission
