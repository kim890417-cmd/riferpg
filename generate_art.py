# -*- coding: utf-8 -*-
"""LIFE RPG 계급 일러스트 16장 자동 생성기.

ComfyUI(127.0.0.1:8188)에 16개 프롬프트를 자동 큐잉 → PNG 받기 → WebP 변환 →
life_rpg/art/<슬러그>-<성별>.webp 로 바로 저장. 한 번 실행으로 전부 완료.

설정은 주인님이 직접 뽑으신 haemong_00002_.png 메타데이터에서 추출한 값 그대로:
  sd_xl_base.safetensors / 832x1216 / 20 steps / cfg 7 / dpmpp_2m+karras / seed 42
스타일 일관성을 위해 베이스 프롬프트와 seed를 고정하고 계급·성별 묘사만 바꾼다.

사전 조건: ComfyUI 서버가 켜져 있어야 함 (run_nvidia_gpu.bat).
실행:  python generate_art.py
"""
import io
import json
import time
from pathlib import Path

import requests
from PIL import Image

COMFYUI_URL = "http://127.0.0.1:8188"
CHECKPOINT  = "sd_xl_base.safetensors"
ART_DIR     = Path(__file__).parent / "art"
SIZE        = (832, 1216)
SEED        = 42          # 고정 = 같은 인물이 진화하는 느낌
STEPS       = 20
CFG         = 7.0
SAMPLER     = "dpmpp_2m"
SCHEDULER   = "karras"

BASE = ("fantasy RPG character portrait, upper body, face in upper-center, "
        "painterly illustration, clean background, soft cinematic lighting, "
        "detailed face, game character art, vertical composition, masterpiece, "
        "high detail, ")

NEG = ("ugly, blurry, low quality, deformed, text, watermark, bad anatomy, "
       "extra limbs, cropped face, full body, lowres")

# 계급 8단계 x 성별(m/f) — 베이스 뒤에 붙는 묘사
RANKS = {
    "peasant": {
        "m": "poor peasant man, simple linen tunic, humble expression, worn cloth, dirt stains",
        "f": "poor peasant woman, simple linen dress, humble expression, worn cloth, dirt stains",
    },
    "squire": {
        "m": "young squire man, leather armor, training sword, eager determined expression, castle courtyard",
        "f": "young squire woman, leather armor, training sword, eager determined expression, castle courtyard",
    },
    "knight": {
        "m": "heroic knight man, polished steel plate armor, blue heraldic tabard, brave expression",
        "f": "heroic knight woman, polished steel plate armor, blue heraldic tabard, brave expression",
    },
    "lord": {
        "m": "fantasy lord man, ornate half-plate armor, noble cape with family crest, confident expression",
        "f": "fantasy noble lady, ornate half-plate armor, noble cape with family crest, confident expression",
    },
    "noble": {
        "m": "wealthy nobleman, luxurious embroidered robes, fur-trimmed cloak, jewels, elegant proud expression",
        "f": "wealthy noblewoman, luxurious embroidered gown, fur-trimmed cloak, jewels, elegant proud expression",
    },
    "king": {
        "m": "majestic king, golden crown, royal ermine robe, holding scepter, regal expression, throne room",
        "f": "majestic queen, golden crown, royal ermine gown, holding scepter, regal expression, throne room",
    },
    "emperor": {
        "m": "powerful emperor, grand ornate imperial crown, golden imperial armor and cape, commanding awe-inspiring expression",
        "f": "powerful empress, grand ornate imperial crown, golden imperial gown and cape, commanding awe-inspiring expression",
    },
    "legend": {
        "m": "legendary godlike male hero, glowing divine golden aura, radiant celestial armor, ethereal wings of light, transcendent serene expression",
        "f": "legendary goddess-like female hero, glowing divine golden aura, radiant celestial armor, ethereal wings of light, transcendent serene expression",
    },
}


def build_workflow(pos_prompt: str) -> dict:
    return {
        "1": {"class_type": "CheckpointLoaderSimple",
              "inputs": {"ckpt_name": CHECKPOINT}},
        "2": {"class_type": "CLIPTextEncode",
              "inputs": {"text": pos_prompt, "clip": ["1", 1]}},
        "3": {"class_type": "CLIPTextEncode",
              "inputs": {"text": NEG, "clip": ["1", 1]}},
        "5": {"class_type": "EmptyLatentImage",
              "inputs": {"width": SIZE[0], "height": SIZE[1], "batch_size": 1}},
        "4": {"class_type": "KSampler",
              "inputs": {"model": ["1", 0], "positive": ["2", 0], "negative": ["3", 0],
                         "latent_image": ["5", 0], "seed": SEED, "steps": STEPS,
                         "cfg": CFG, "sampler_name": SAMPLER,
                         "scheduler": SCHEDULER, "denoise": 1.0}},
        "6": {"class_type": "VAEDecode",
              "inputs": {"samples": ["4", 0], "vae": ["1", 2]}},
        "7": {"class_type": "SaveImage",
              "inputs": {"images": ["6", 0], "filename_prefix": "rpgart"}},
    }


def generate_one(pos_prompt: str, out_path: Path, timeout: int = 240) -> None:
    wf = build_workflow(pos_prompt)
    resp = requests.post(f"{COMFYUI_URL}/prompt", json={"prompt": wf})
    resp.raise_for_status()
    prompt_id = resp.json()["prompt_id"]

    start = time.time()
    while time.time() - start < timeout:
        hist = requests.get(f"{COMFYUI_URL}/history/{prompt_id}").json()
        if prompt_id in hist:
            for node_out in hist[prompt_id].get("outputs", {}).values():
                if "images" in node_out:
                    img = node_out["images"][0]
                    url = (f"{COMFYUI_URL}/view?filename={img['filename']}"
                           f"&subfolder={img.get('subfolder', '')}"
                           f"&type={img.get('type', 'output')}")
                    png = requests.get(url).content
                    im = Image.open(io.BytesIO(png)).convert("RGB")
                    if im.size != SIZE:
                        im = im.resize(SIZE, Image.LANCZOS)
                    im.save(out_path, "webp", quality=90)
                    return
        time.sleep(2)
    raise TimeoutError(f"시간 초과: {out_path.name}")


def main() -> None:
    try:
        if requests.get(f"{COMFYUI_URL}/system_stats", timeout=3).status_code != 200:
            raise RuntimeError
    except Exception:
        print("ComfyUI 서버가 꺼져 있습니다. run_nvidia_gpu.bat 로 켠 뒤 다시 실행하세요.")
        return

    ART_DIR.mkdir(exist_ok=True)
    jobs = [(slug, g) for slug in RANKS for g in ("m", "f")]
    print(f"총 {len(jobs)}장 생성 시작 (저장 위치: {ART_DIR})\n")

    for i, (slug, g) in enumerate(jobs, 1):
        name = f"{slug}-{g}"
        pos = BASE + RANKS[slug][g]
        t0 = time.time()
        print(f"[{i:2}/{len(jobs)}] {name} 생성 중...", end="", flush=True)
        try:
            generate_one(pos, ART_DIR / f"{name}.webp")
            print(f" 완료 ({time.time()-t0:.0f}s)")
        except Exception as e:
            print(f" 실패: {e}")

    print(f"\n=== 끝! {ART_DIR} 확인하세요 ===")


if __name__ == "__main__":
    main()
