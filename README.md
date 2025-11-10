# LiveKit Voice Agent – Interruption Handling Enhancement

**Author:** Priyanshu M  
**Repository:** https://github.com/PeKkaPie95/SalesCodeSubmission

---

## 🧠 Overview

This submission enhances a LiveKit-based real-time voice agent to make spoken interactions more natural and interruption-aware.

In real conversations, users often produce hesitation sounds such as **“umm”**, **“haan”**, **“hmm”**, which *should not* interrupt the agent while it is speaking.  
However, meaningful user intent such as **“wait”**, **“stop”**, or **“one second”** *should* immediately interrupt.

This project adds a **speech meaning filter layer** *without modifying LiveKit's VAD logic*, as required.

---

## 🎯 Objectives Achieved

| Goal | Status | Implementation Detail |
|------|:------:|----------------------|
| Ignore filler/hesitation words while agent is speaking | Filter based on customizable filler list |
| Immediately stop TTS when meaningful user speech is detected | Calls `session.agent.stop_speaking()` |
| Do **not** modify LiveKit VAD | Pure extension layer logic |
| Dynamically configurable filler list | Loaded via `IGNORED_FILLERS` environment variable |
| Low confidence noise suppression | Speech ignored if confidence < threshold |

---

## ⚙️ How It Works

The agent maintains a flag indicating whether **TTS is currently playing**:

```python
@session.on("agent_speech_started")
def _on_agent_speaking_started(*_):
    agent_is_speaking = True

@session.on("agent_speech_ended")
def _on_agent_speaking_ended(*_):
    agent_is_speaking = False
When a transcription event arrives:

@session.on("transcription")
async def handle_transcription(text: str, confidence: float, **kwargs):
    # If agent is not speaking → normal user speech handling
    if not agent_is_speaking:
        print(f"[USER SPEAKING] {text}")
        return

    # If agent is speaking → decide whether to interrupt
    if is_meaningful_speech(text, confidence):
        print(f"[INTERRUPT] {text}")
        await session.agent.stop_speaking()   # interrupts TTS immediately
    else:
        print(f"[IGNORED FILLER] {text}")

Meaning-based Speech Detection
IGNORED_FILLERS = set(
    word.strip().lower() for word in os.getenv("IGNORED_FILLERS", "uh,umm,hmm,haan").split(",")
)

def is_meaningful_speech(text: str, confidence: float, threshold: float = 0.75) -> bool:
    if confidence < threshold:
        return False

    words = text.lower().strip().split()

    # Ignore if entire utterance is only fillers
    if all(word in IGNORED_FILLERS for word in words):
        return False

    return True

Testing

A small test script verifies behavior:

from realtime_with_tts import is_meaningful_speech

test("umm", 0.95)                # ignored
test("haan", 0.90)               # ignored
test("wait one second", 0.95)    # interrupt
test("umm okay stop", 0.96)      # interrupt
test("mmff", 0.20)               # noise ignored (low confidence)

Expected Output
Input: 'umm' -> meaningful=False
Input: 'haan' -> meaningful=False
Input: 'wait one second' -> meaningful=True
Input: 'umm okay stop' -> meaningful=True
Input: 'mmff' -> meaningful=False

Run Instructions
Install dependencies
pip install livekit-agents livekit-plugins-openai python-dotenv

Optional: customize filler list
export IGNORED_FILLERS="uh,umm,hmm,haan"

Run the agent
python realtime_with_tts.py
