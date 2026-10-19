"""Pregătește mostrele audio pentru publicare.

Taie fiecare MP3 din assets/audio/ la 60 de secunde, îl re-encodează la
128 kbps / 44,1 kHz stereo, aplică un fade-out scurt la final și rescrie
metadatele ID3 (titlu, artist, album, gen), ca titlul din fișier să coincidă
cu titlul afișat pe card și cu proprietatea `song` din obiectul `tracks`.

Dependențe (în afara repository-ului, ex. într-un virtualenv):

    pip install miniaudio lameenc mutagen numpy

Rulare din rădăcina repository-ului:

    python3 tools/optimize_samples.py

Scriptul suprascrie fișierele din assets/audio/; păstrează înregistrările
sursă, în versiune completă, în afara repository-ului.
"""
import os
import sys

import numpy as np
import miniaudio
import lameenc
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TCON, TENC, COMM

SR = 44100
CH = 2
BITRATE = 128
LIMIT_S = 60.0
FADE_S = 2.5
ARTIST = "Poveste pe Note"
ALBUM = "Mostre demonstrative"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TRACKS = [
    ("assets/audio/locul-meu-e-langa-tine.mp3", "The Beautiful Life", "Romantic pop"),
    ("assets/audio/mama-primul-meu-acasa.mp3", "Nights You Stayed Awake", "Baladă emoționantă"),
    ("assets/audio/legenda-din-gasca.mp3", "The Legend They Whisper", "Pop vesel"),
]


def encode(pcm: bytes) -> bytes:
    enc = lameenc.Encoder()
    enc.set_bit_rate(BITRATE)
    enc.set_in_sample_rate(SR)
    enc.set_channels(CH)
    enc.set_quality(2)  # 2 = calitate ridicată
    return bytes(enc.encode(pcm) + enc.flush())


def process(path: str, title: str, genre: str) -> None:
    before = os.path.getsize(path)
    src = MP3(path).info

    decoded = miniaudio.decode_file(
        path,
        output_format=miniaudio.SampleFormat.SIGNED16,
        nchannels=CH,
        sample_rate=SR,
    )
    samples = np.frombuffer(decoded.samples, dtype="<i2").astype(np.float32)

    trimmed = samples[: int(LIMIT_S * SR) * CH]

    # fade-out pe ultimii FADE_S secunde, ca fragmentul să nu se oprească brusc
    fade = int(FADE_S * SR) * CH
    if len(trimmed) > fade:
        ramp = np.repeat(np.linspace(1.0, 0.0, fade // CH, dtype=np.float32), CH)
        trimmed[len(trimmed) - len(ramp):] *= ramp

    pcm = np.clip(trimmed, -32768, 32767).astype("<i2").tobytes()
    tmp = path + ".new"
    with open(tmp, "wb") as fh:
        fh.write(encode(pcm))

    tags = ID3()
    tags.add(TIT2(encoding=3, text=title))
    tags.add(TPE1(encoding=3, text=ARTIST))
    tags.add(TALB(encoding=3, text=ALBUM))
    tags.add(TCON(encoding=3, text=genre))
    tags.add(TENC(encoding=3, text="Poveste pe Note"))
    tags.add(COMM(encoding=3, lang="ron", desc="",
                  text="Fragment demonstrativ de 60 de secunde."))
    tags.save(tmp)
    os.replace(tmp, path)

    info = MP3(path).info
    after = os.path.getsize(path)
    print(f"{os.path.relpath(path, ROOT)}: {src.length:.0f}s/{src.bitrate // 1000}kbps/"
          f"{before / 1048576:.1f}MB -> {info.length:.0f}s/{info.bitrate // 1000}kbps/"
          f"{after / 1048576:.1f}MB  [{title}]")


def main() -> int:
    missing = [rel for rel, _, _ in TRACKS if not os.path.exists(os.path.join(ROOT, rel))]
    if missing:
        print("Lipsesc fișierele:", ", ".join(missing), file=sys.stderr)
        return 1
    for rel, title, genre in TRACKS:
        process(os.path.join(ROOT, rel), title, genre)
    return 0


if __name__ == "__main__":
    sys.exit(main())
