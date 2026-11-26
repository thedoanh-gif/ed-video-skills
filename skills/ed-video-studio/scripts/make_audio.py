#!/usr/bin/env python3
"""Generate an original, royalty-free music bed and a matching SFX set with code (no samples).

Usage:
  python3 make_audio.py music --out audio/theme.wav --mood calm|bright|focus --bpm 100 --seconds 90 [--seed 7]
  python3 make_audio.py sfx --out audio/sfx/

music: soft pad chords + plucked arpeggio + light kick/hat, loops cleanly at the end of a bar,
       mastered to about -18 LUFS (sits under narration after ducking).
sfx:   whoosh.wav, pop.wav, tick.wav, chime.wav, stamp.wav, swipe.wav, click.wav

Same --mood/--bpm/--seed => same track: record them in the Series Kit so every episode shares it.
Needs numpy (pip install numpy) and ffmpeg (for loudness normalisation).
"""
import argparse, subprocess, wave
from pathlib import Path
import numpy as np

SR = 44100
MOODS = {  # chord roots (semitones from A3=220Hz) with chord types
    "calm":   {"prog": [(0, "maj7"), (-4, "maj7"), (5, "min7"), (3, "maj7")], "bright": 0.6},
    "bright": {"prog": [(3, "maj"), (10, "maj"), (0, "min"), (8, "maj")], "bright": 1.0},
    "focus":  {"prog": [(0, "min7"), (-2, "maj7"), (-4, "maj7"), (-5, "dom7")], "bright": 0.7},
}
SHAPES = {"maj": [0, 4, 7], "min": [0, 3, 7], "maj7": [0, 4, 7, 11], "min7": [0, 3, 7, 10], "dom7": [0, 4, 7, 10]}


def f(semi, base=220.0):
    return base * 2 ** (semi / 12)


def env(n, a=0.01, r=0.3):
    t = np.arange(n) / SR
    e = np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / max(r, 1e-4))
    return e


def write(path, x, stereo=True):
    x = np.clip(x, -1, 1)
    if stereo and x.ndim == 1:
        x = np.stack([x, x], 1)
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2 if stereo else 1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())


def loudnorm(path, target):
    tmp = Path(path).with_suffix(".tmp.wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(path), "-af", f"loudnorm=I={target}:TP=-2:LRA=11",
                    "-ar", str(SR), str(tmp)], check=True)
    tmp.replace(path)


def music(out, mood, bpm, seconds, seed):
    rng = np.random.default_rng(seed)
    M = MOODS[mood]; beat = 60 / bpm; bar = 4 * beat
    bars = max(4, int(round(seconds / bar / 4)) * 4)  # whole 4-bar phrases -> clean loop
    N = int(bars * bar * SR); L = np.zeros(N); R = np.zeros(N)
    t_all = np.arange(N) / SR
    for b in range(bars):
        root, kind = M["prog"][b % 4]
        s0 = int(b * bar * SR); n = min(int(bar * SR), N - s0); t = np.arange(n) / SR
        # pad: detuned saws softened by averaging harmonics, slow attack
        pad = np.zeros(n)
        for iv in SHAPES[kind]:
            for det in (-0.08, 0.08):
                fr = f(root + iv + det / 1, 220) / 2
                pad += sum(np.sin(2 * np.pi * fr * k * t) / k ** 1.6 for k in range(1, 6))
        pad *= np.minimum(1, t / 0.6) * np.clip((bar - t) / 0.3, 0, 1) * 0.045
        L[s0:s0 + n] += pad; R[s0:s0 + n] += pad
        # arpeggio: plucks on 8th notes, panned alternately
        notes = SHAPES[kind] + [12 + SHAPES[kind][0]]
        for i in range(8):
            if rng.random() < 0.15:
                continue
            semi = root + notes[[0, 1, 2, 3, 2, 1, 2, 3][i] % len(notes)] + 12
            st = s0 + int(i * beat / 2 * SR); m = int(0.5 * SR)
            if st + m > N:
                m = N - st
            tt = np.arange(m) / SR; fr = f(semi)
            pl = (np.sin(2 * np.pi * fr * tt) + 0.3 * M["bright"] * np.sin(2 * np.pi * 2 * fr * tt)) * env(m, 0.004, 0.18) * 0.11
            pan = 0.35 if i % 2 else -0.35
            L[st:st + m] += pl * (1 - pan); R[st:st + m] += pl * (1 + pan)
        # bass on beats 1 and 3
        for q in (0, 2):
            st = s0 + int(q * beat * SR); m = int(beat * 1.8 * SR); m = min(m, N - st)
            tt = np.arange(m) / SR
            bs = np.sin(2 * np.pi * f(root - 12, 220) / 2 * tt) * env(m, 0.01, 0.5) * 0.16
            L[st:st + m] += bs; R[st:st + m] += bs
        # soft kick + hat
        for q in range(4):
            st = s0 + int(q * beat * SR)
            if q in (0, 2):
                m = min(int(0.25 * SR), N - st); tt = np.arange(m) / SR
                k = np.sin(2 * np.pi * (50 + 80 * np.exp(-tt * 30)) * tt) * env(m, 0.002, 0.09) * 0.22
                L[st:st + m] += k; R[st:st + m] += k
            hs = st + int(beat / 2 * SR); m = int(0.05 * SR)
            if hs + m < N:
                h = rng.standard_normal(m) * env(m, 0.001, 0.015) * 0.025
                h = np.diff(np.concatenate([[0], h]))  # crude high-pass
                L[hs:hs + m] += h; R[hs:hs + m] += h
    fade = int(0.02 * SR)  # tiny edge fades keep the loop click-free
    for ch in (L, R):
        ch[:fade] *= np.linspace(0, 1, fade); ch[-fade:] *= np.linspace(1, 0, fade)
    x = np.stack([L, R], 1); x /= max(1e-6, np.abs(x).max()) / 0.8
    write(out, x); loudnorm(out, -18)
    print(f"OK {out}: {bars} ô nhịp, {bars * bar:.1f}s, mood={mood}, bpm={bpm}, seed={seed} (lặp liền mạch)")


def sfx(out):
    out = Path(out); rng = np.random.default_rng(1)
    n = int(0.6 * SR); t = np.arange(n) / SR
    noise = rng.standard_normal(n)
    sweep = np.convolve(noise, np.ones(40) / 40, mode="same") * np.sin(np.pi * t / t[-1]) ** 2  # whoosh
    write(out / "whoosh.wav", sweep / np.abs(sweep).max() * 0.5)
    m = int(0.12 * SR); tt = np.arange(m) / SR
    write(out / "pop.wav", np.sin(2 * np.pi * (600 + 900 * np.exp(-tt * 40)) * tt) * env(m, 0.002, 0.03) * 0.6)
    m = int(0.05 * SR); tt = np.arange(m) / SR
    write(out / "tick.wav", np.sin(2 * np.pi * 2200 * tt) * env(m, 0.001, 0.008) * 0.5)
    m = int(1.6 * SR); tt = np.arange(m) / SR
    ch = sum(np.sin(2 * np.pi * fr * tt) * a for fr, a in ((880, 0.5), (1320, 0.3), (1760, 0.15), (2637, 0.08)))
    write(out / "chime.wav", ch * env(m, 0.003, 0.6) * 0.45)
    m = int(0.25 * SR); tt = np.arange(m) / SR
    th = np.sin(2 * np.pi * (90 + 120 * np.exp(-tt * 35)) * tt) * env(m, 0.001, 0.07)
    cr = rng.standard_normal(m) * env(m, 0.001, 0.02) * 0.4
    write(out / "stamp.wav", (th + cr) * 0.6)
    m = int(0.3 * SR); tt = np.arange(m) / SR
    sw = np.convolve(rng.standard_normal(m), np.ones(12) / 12, mode="same") * np.sin(np.pi * tt / tt[-1]) * np.linspace(0.3, 1, m)
    write(out / "swipe.wav", sw / np.abs(sw).max() * 0.35)
    m = int(0.03 * SR); tt = np.arange(m) / SR
    write(out / "click.wav", rng.standard_normal(m) * env(m, 0.0005, 0.004) * 0.5)
    print(f"OK {out}: whoosh, pop, tick, chime, stamp, swipe, click")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kind", choices=["music", "sfx"])
    ap.add_argument("--out", required=True)
    ap.add_argument("--mood", default="calm", choices=MOODS)
    ap.add_argument("--bpm", type=int, default=100)
    ap.add_argument("--seconds", type=float, default=90)
    ap.add_argument("--seed", type=int, default=7)
    a = ap.parse_args()
    music(a.out, a.mood, a.bpm, a.seconds, a.seed) if a.kind == "music" else sfx(a.out)


if __name__ == "__main__":
    main()
