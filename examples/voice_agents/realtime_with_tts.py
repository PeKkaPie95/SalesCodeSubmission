import os
import logging

from dotenv import load_dotenv

from livekit.agents import JobContext, WorkerOptions, cli
from livekit.agents.llm import function_tool
from livekit.agents.voice import Agent, AgentSession
from livekit.agents.voice.room_io import RoomOutputOptions
from livekit.plugins import openai  # noqa: F401

logger = logging.getLogger("realtime-with-tts")
logger.setLevel(logging.INFO)

load_dotenv()
IGNORED_FILLERS = set(
    word.strip().lower() for word in os.getenv("IGNORED_FILLERS", "uh,umm,hmm,haan").split(",")
)

agent_is_speaking = False

# This example is showing a half-cascade realtime LLM usage where we:
# - use a multimodal/realtime LLM that takes audio input, generating text output
# - then use a separate TTS to synthesize audio output
#
# This approach fully utilizes the realtime LLM's ability to understand directly from audio
# and yet maintains control of the pipeline, including using custom voices with TTS

def is_meaningful_speech(text: str, confidence: float, threshold: float = 0.75) -> bool:
    if confidence < threshold:
        return False

    words = text.lower().strip().split()

    # If all words are fillers, ignore it
    if all(word in IGNORED_FILLERS for word in words):
        return False

    return True


class WeatherAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="You are a helpful assistant.",
            llm=openai.realtime.RealtimeModel(modalities=["text"]),
            # llm=google.beta.realtime.RealtimeModel(modalities=[Modality.TEXT]),
            tts=openai.TTS(voice="ash"),
        )

    @function_tool
    async def get_weather(self, location: str):
        """Called when the user asks about the weather.

        Args:
            location: The location to get the weather for
        """

        logger.info(f"getting weather for {location}")
        return f"The weather in {location} is sunny, and the temperature is 20 degrees Celsius."


async def entrypoint(ctx: JobContext):
    session = AgentSession()

    await session.start(
        agent=WeatherAgent(),
        room=ctx.room,
        room_output_options=RoomOutputOptions(
            transcription_enabled=True,
            audio_enabled=True,  # you can also disable audio output to use text modality only
        ),
    )

    # --------------------------
    # BEGIN: interruption handling logic
    # --------------------------

    global agent_is_speaking

    # Track when agent starts speaking (TTS active)
    @session.on("agent_speech_started")
    def _on_agent_speaking_started(*_):
        global agent_is_speaking
        agent_is_speaking = True

    # Track when agent finishes speaking (TTS stopped)
    @session.on("agent_speech_ended")
    def _on_agent_speaking_ended(*_):
        global agent_is_speaking
        agent_is_speaking = False

    # Handle transcription events and decide whether to interrupt
    @session.on("transcription")
    async def handle_transcription(text: str, confidence: float, **kwargs):
        global agent_is_speaking

        # Case 1: Agent is *not* speaking → treat normally
        if not agent_is_speaking:
            print(f"[USER SPEAKING] {text}")
            return

        # Case 2: Agent *is* speaking → check if meaningful interruption
        if is_meaningful_speech(text, confidence):
            print(f"[INTERRUPT] {text}")
            await session.agent.stop_speaking()  # stops TTS immediately
        else:
            print(f"[IGNORED FILLER] {text}")

    # --------------------------
    # END interruption handling logic
    # --------------------------

    # Initial greeting
    session.generate_reply(instructions="say hello to the user in English")



if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
