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
