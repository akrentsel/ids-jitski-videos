"""Generate voiceover audio using ElevenLabs TTS (pre-1.x SDK)."""
import os
from pathlib import Path
from elevenlabs import generate, set_api_key

set_api_key(os.environ["ELEVENLABS_API_KEY"])
VOICE = os.environ.get("ELEVENLABS_VOICE_ID", "SAxJUlDKRc79XAyeWyMu")  # Morgan
MODEL = "eleven_multilingual_v2"

scenes = {
    "scene1": [
        "AI coding agents are getting remarkably good. They write code, run the tests, and fix their own mistakes.",
        "But some software has to be more than well-tested. It has to be provably correct. On every input, every time.",
        "Think distributed systems, where bugs hide in rare interleavings of messages that no test suite will ever reach.",
    ],
    "scene2": [
        "The gold standard is formal verification. You write a specification, an implementation, and a machine-checked proof that they always agree.",
        "The catch: doing this by hand takes experts months, sometimes years, per system.",
        "So can today's coding agents just do it for us? Not really. Given seven key-value store specifications, state of the art agents verified only two.",
        "And the failure mode is structural. They write all the code first, then face the entire proof at once. A sheer cliff, with no feedback along the way.",
    ],
    "scene3": [
        "This paper's idea is called Inductive Deductive Synthesis, or IDS. The key insight: don't build the proof after the code. Grow them together, incrementally.",
        "You start with the full specification, every property the system must satisfy, an empty implementation, and an empty proof.",
        "The agent takes a small step: define one piece of the implementation, and prove one small property about it. Anything unfinished is marked with an explicit placeholder. An I O U, called Admitted.",
        "And here's the trick. The Rocq proof assistant grades every partial state. If the file type-checks, the design is still viable, so the agent banks the progress and takes another step.",
        "A bit more implementation. A bit more proof. Step by step the I O Us get paid off, until the specification is fully implemented, and fully proven.",
    ],
    "scene4": [
        "What if a step fails? That's not wasted work. It's signal. A partial proof that gets stuck rules out a dead-end design before more effort is piled on top.",
        "IDS backtracks to the last good state and pivots. When one big monolithic store made the proof intractable, it split the data per key, and the proof fell apart into small, easy cases.",
    ],
    "scene5": [
        "The results: IDS verified all seven specifications. Seven out of seven, where the best coding agents managed two.",
        "On average, six point eight hours and about a hundred dollars per system. Against months of expert effort, that's roughly two hundred times faster.",
        "And because IDS benchmarks candidates as it goes, its verified implementations run up to three times faster than published, hand-written ones.",
    ],
    "scene6": [
        "Verified software used to be a human-labor bottleneck. IDS turns it into a compute problem. Grow the code and its proof together, and let the checker keep score.",
        "The paper is Inductive Deductive Synthesis: Enabling AI to Generate Formally Verified Systems. Check it out to learn more.",
    ],
}

audio_dir = Path("audio")
audio_dir.mkdir(exist_ok=True)

for scene_name, segments in scenes.items():
    print(f"\n=== {scene_name} ===")
    seg_files = []
    for i, text in enumerate(segments):
        out_path = audio_dir / f"{scene_name}_seg{i}.mp3"
        if out_path.exists():
            print(f"  [cached] {out_path.name}")
            seg_files.append(str(out_path))
            continue
        print(f"  Generating: {text[:60]}...")
        audio = generate(text=text, voice=VOICE, model=MODEL)
        out_path.write_bytes(audio)
        seg_files.append(str(out_path))

    concat_file = audio_dir / f"{scene_name}_concat.txt"
    with open(concat_file, "w") as f:
        for sf in seg_files:
            f.write(f"file '{os.path.basename(sf)}'\n")

print("\nDone!")
