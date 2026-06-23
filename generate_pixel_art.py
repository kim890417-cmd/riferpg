# -*- coding: utf-8 -*-
"""LIFE RPG 픽셀 아트 계급 일러스트 16장 생성기.

pollinations.ai (flux 모델) 로 16장 생성 → PNG 저장.
초록 배경으로 생성하여 composite_art.py 의
크로마키 + 픽셀화 + 배경 합성 파이프라인에 넘긴다.

실행:  python generate_pixel_art.py
"""
import time
from pathlib import Path
from urllib.parse import quote

import requests

API_URL   = "https://image.pollinations.ai/prompt"
RAW_DIR   = Path(__file__).parent / "art" / "_raw"
SIZE      = (832, 1216)
SEED      = 42
MODEL     = "flux"

BASE = ("fantasy RPG character, full body standing from head to feet centered, "
        "game character sprite, 16-bit retro pixel art, SNES style, "
        "solid bright green screen background, retro game character design, "
        "front view, crisp pixel outline, ")

RANKS = {
    "peasant": {
        "m": "medieval peasant man, poor simple tunic, humble posture, barefoot, dirt on face",
        "f": "medieval peasant woman, poor simple dress, humble posture, barefoot, worn cloth",
    },
    "squire": {
        "m": "young squire man, leather armor vest, training sword at side, eager expression, sturdy boots",
        "f": "young squire woman, leather armor, training sword at side, determined expression, boots",
    },
    "knight": {
        "m": "heroic knight man, polished steel plate armor, blue cape, visor up, brave stance",
        "f": "heroic knight woman, polished steel plate armor, blue cape, visor up, brave stance",
    },
    "lord": {
        "m": "fantasy lord man, ornate half-plate armor, noble red cape, confident posture, holding gauntlets",
        "f": "fantasy noble lady, ornate half-plate armor, elegant cape, confident posture",
    },
    "noble": {
        "m": "wealthy nobleman, luxurious embroidered tunic, fur-trimmed cloak, jeweled pendant, elegant posture",
        "f": "wealthy noblewoman, luxurious embroidered gown, fur-trimmed cloak, jeweled necklace, elegant posture",
    },
    "king": {
        "m": "majestic king, golden crown, royal ermine robe, holding golden scepter, regal stance",
        "f": "majestic queen, golden crown, royal ermine gown, holding golden scepter, regal stance",
    },
    "emperor": {
        "m": "powerful emperor, grand imperial crown, golden armor and cape, commanding stance, aura of authority",
        "f": "powerful empress, grand imperial crown, golden armor and cape, commanding stance, aura of authority",
    },
    "legend": {
        "m": "legendary godlike male hero, glowing divine golden aura, radiant celestial armor, ethereal wings, transcendent",
        "f": "legendary goddess-like female hero, glowing divine golden aura, radiant celestial armor, ethereal wings, transcendent",
    },
}


def generate_one(pos_prompt: str, out_path: Path, timeout: int = 120) -> None:
    prompt = quote(pos_prompt)
    url = (f"{API_URL}/{prompt}"
           f"?width={SIZE[0]}&height={SIZE[1]}&seed={SEED}&model={MODEL}&nologo=true")
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    with open(out_path, "wb") as f:
        f.write(resp.content)
    # pollinations.ai ratelimit 방지
    time.sleep(1.5)


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    jobs = [(slug, g) for slug in RANKS for g in ("m", "f")]
    print(f"pollinations.ai ({MODEL}) - pixel art {len(jobs)}장 생성 시작\n")

    for i, (slug, g) in enumerate(jobs, 1):
        name = f"{slug}-{g}"
        pos = BASE + RANKS[slug][g]
        t0 = time.time()
        print(f"[{i:2}/{len(jobs)}] {name} 생성 중...", end="", flush=True)
        try:
            generate_one(pos, RAW_DIR / f"{name}.png")
            print(f" 완료 ({time.time()-t0:.0f}s)")
        except Exception as e:
            print(f" 실패: {e}")

    print(f"\n=== 끝! {RAW_DIR} 확인 후 composite_art.py 실행 ===")


if __name__ == "__main__":
    main()
