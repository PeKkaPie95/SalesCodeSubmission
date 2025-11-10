from realtime_with_tts import is_meaningful_speech, IGNORED_FILLERS

def test(text, confidence):
    result = is_meaningful_speech(text, confidence)
    print(f"Input: '{text}' (conf={confidence}) -> meaningful={result}")

print("Filler-only cases while agent speaking:")
test("umm", 0.95)
test("haan", 0.90)
test("hmm hmm", 0.98)

print("\nMeaningful interruption cases:")
test("wait one second", 0.95)
test("stop", 0.94)
test("umm okay stop", 0.96)

print("\nLow confidence (background noise):")
test("mmff", 0.20)
