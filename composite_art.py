# -*- coding: utf-8 -*-
"""LIFE RPG 픽셀 아트 합성 파이프라인.

1. generate_pixel_art.py 가 생성한 초록배경 PNG 로드
2. 크로마키 → 배경 제거 (알파 채널)
3. 픽셀화 (16-bit SD 느낌)
4. 계급별 배경(bg-*.webp) 위에 합성
5. art/{slug}-{gender}.webp 로 저장
6. 펫 이미지도 동일하게 픽셀화

실행:  python composite_art.py
"""
from pathlib import Path

from PIL import Image

ART_DIR   = Path(__file__).parent / "art"
RAW_DIR   = ART_DIR / "_raw"
BLOCK_SIZE = 10  # 픽셀 블록 크기 — 832/10=83, 1216/10=121 → 16-bit SD 느낌
PET_BLOCK  = 6   # 펫은 좀 더 촘촘하게

RANKS = ["peasant", "squire", "knight", "lord", "noble", "king", "emperor", "legend"]


def chroma_key(img: Image.Image, tolerance: int = 55) -> Image.Image:
    """초록 배경(#00FF00)을 투명하게 제거."""
    rgba = img.convert("RGBA")
    data = bytearray(rgba.tobytes())
    for i in range(0, len(data), 4):
        r, g, b = data[i], data[i+1], data[i+2]
        # g 가 r, b 보다 tolerance 이상 높으면 → 초록배경
        if g > r + tolerance and g > b + tolerance:
            data[i+3] = 0  # alpha = 0
    return Image.frombytes("RGBA", rgba.size, bytes(data))


def pixelate(img: Image.Image, block_size: int) -> Image.Image:
    """픽셀화: 다운스케일 → LANCZOS 평균 → NI 업스케일."""
    w, h = img.size
    sw = max(1, w // block_size)
    sh = max(1, h // block_size)
    small = img.resize((sw, sh), Image.LANCZOS)
    return small.resize((w, h), Image.NEAREST)


def composite_character(char_path: Path, bg_path: Path, out_path: Path) -> None:
    """픽셀 아트 캐릭터를 배경 위에 합성."""
    # 캐릭터 로드 → 크로마키 → 픽셀화
    raw = Image.open(char_path)
    clean = chroma_key(raw)
    pixelated = pixelate(clean, BLOCK_SIZE)

    # 배경 로드 (bg-*.webp) → 캐릭터와 같은 크기로 리사이즈
    bg = Image.open(bg_path).convert("RGBA")
    bg = bg.resize(pixelated.size, Image.LANCZOS)

    # 합성: 캐릭터를 배경 위에 얹음
    composed = Image.alpha_composite(bg, pixelated)

    # 저장
    final = composed.convert("RGB")
    final.save(out_path, "webp", quality=90)
    print(f"  → {out_path.name} 저장 완료")


def pixelate_pet(pet_path: Path) -> None:
    """펫 이미지 픽셀화."""
    img = Image.open(pet_path).convert("RGBA")
    px = pixelate(img, PET_BLOCK)
    px.convert("RGB").save(pet_path, "webp", quality=90)
    print(f"  [pet] {pet_path.name} pix 완료")


def main() -> None:
    if not RAW_DIR.exists():
        print(f"오류: {RAW_DIR} 가 없습니다. 먼저 generate_pixel_art.py 를 실행하세요.")
        return

    # ── 캐릭터 합성 ──
    print("=== 캐릭터 합성 시작 ===")
    for slug in RANKS:
        for g in ("m", "f"):
            char_png = RAW_DIR / f"{slug}-{g}.png"
            bg_webp  = ART_DIR / f"bg-{slug}.webp"
            out_webp = ART_DIR / f"{slug}-{g}.webp"
            if not char_png.exists():
                print(f"  ⚠️ {char_png.name} 없음, 스킵")
                continue
            if not bg_webp.exists():
                print(f"  ⚠️ {bg_webp.name} 없음, 스킵")
                continue
            composite_character(char_png, bg_webp, out_webp)

    # ── 펫 픽셀화 ──
    print("\n=== 펫 픽셀화 시작 ===")
    pets_dir = ART_DIR / "pets"
    if pets_dir.exists():
        for pet in sorted(pets_dir.glob("*.webp")):
            pixelate_pet(pet)
    else:
        print("  펫 디렉토리 없음")

    print("\n=== 모든 작업 완료! ===")


if __name__ == "__main__":
    main()
