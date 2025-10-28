import subprocess, inspect
from pathlib import Path

# stretch_sounds needs as src the path to the sound file you want to play and as
# length the duration you want the sound to play (in ms)

def stretch_sound(src: str, length: int) -> str:
    caller_dir = Path(inspect.stack()[1].filename).resolve().parent
    src_path   = (caller_dir / src).resolve() 
    AUDIO_CACHE = caller_dir / "assets" / "audio_cache"
    AUDIO_CACHE.mkdir(parents=True, exist_ok=True)

    out = AUDIO_CACHE / f"{Path(src_path).stem}_{length}.wav"
    if out.exists(): return str(out)

    duration = float(subprocess.check_output(
        ["ffprobe","-v","error","-show_entries","format=duration","-of","default=nk=1:nw=1", str(src_path)],
        text=True).strip())
    direction = duration / length
    chain = []
    while direction > 2.0: chain.append(2.0); direction /= 2.0
    while direction < 0.5: chain.append(0.5); direction /= 0.5
    chain.append(direction)

    filt = ",".join([f"atempo={a}" for a in chain]) + f",apad,atrim=duration={length}"
    subprocess.run([
        "ffmpeg","-y","-i", str(src_path),
        "-filter:a", filt,
        "-acodec", "pcm_s16le", "-ar", "48000", "-ac", "2",
        str(out)
    ], check=True)
    return str(out)
