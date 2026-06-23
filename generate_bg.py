# -*- coding: utf-8 -*-
"""LIFE RPG 계급 배경 8장 자동 생성기.

각 계급의 '세계' 배경(인물 없음)을 ComfyUI로 생성 → WebP 변환 →
life_rpg/art/bg-<슬러그>.webp 로 저장. 계급 진화 연출의 전체 배경으로 사용.

설정은 generate_art.py(인물)와 동일한 체크포인트/샘플러를 쓰되,
베이스 프롬프트를 'no people, 풍경'으로 바꾼다. 성별 구분 없음(계급당 1장).
"""
import io
import time
from pathlib import Path

import requests
from PIL import Image

COMFYUI_URL = "http://127.0.0.1:8188"
CHECKPOINT  = "sd_xl_base.safetensors"
ART_DIR     = Path(__file__).parent / "art"
SIZE        = (832, 1216)   # 폰 전체화면(세로) 배경
SEED        = 42
STEPS       = 20
CFG         = 7.0
SAMPLER     = "dpmpp_2m"
SCHEDULER   = "karras"

BASE = ("fantasy environment concept art, scenery background, wide establishing shot, "
        "atmospheric, cinematic lighting, painterly digital painting, masterpiece, "
        "high detail, no people, ")

NEG = ("people, person, human, character, portrait, crowd, text, watermark, "
       "ugly, blurry, low quality, deformed, lowres")

# 계급 8단계 배경 (계급 슬러그와 동일하게 맞춤)
BGS = {
    "peasant": "muddy poor village, thatched roof cottages, dirt road, overcast grey sky, humble farmland",
    "squire":  "castle training courtyard, stone walls, wooden training dummies, dawn light, morning mist",
    "knight":  "epic battlefield, iron castle gate, dramatic stormy sky, torches, war banners",
    "lord":    "vast green hills, manor house on hilltop, golden hour sunlight, peaceful countryside",
    "noble":   "elegant palace garden, marble columns, blooming flowers, soft warm light, fountain",
    "king":    "grand throne room, red carpet, tall stained glass windows, golden candlelight",
    "emperor": "imperial golden palace, vast empire cityscape, golden spires, majestic blue sky",
    "legend":  "ancient divine ruins, floating islands, ethereal glowing light, mythical atmosphere, aurora sky",
}


def build_workflow(pos_prompt: str) -> dict:
    return {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": CHECKPOINT}},
        "2": {"class_type": "CLIPTextEncode", "inputs": {"text": pos_prompt, "clip": ["1", 1]}},
        "3": {"class_type": "CLIPTextEncode", "inputs": {"text": NEG, "clip": ["1", 1]}},
        "5": {"class_type": "EmptyLatentImage",
              "inputs": {"width": SIZE[0], "height": SIZE[1], "batch_size": 1}},
        "4": {"class_type": "KSampler",
              "inputs": {"model": ["1", 0], "positive": ["2", 0], "negative": ["3", 0],
                         "latent_image": ["5", 0], "seed": SEED, "steps": STEPS,
                         "cfg": CFG, "sampler_name": SAMPLER, "scheduler": SCHEDULER,
                         "denoise": 1.0}},
        "6": {"class_type": "VAEDecode", "inputs": {"samples": ["4", 0], "vae": ["1", 2]}},
        "7": {"class_type": "SaveImage", "inputs": {"images": ["6", 0], "filename_prefix": "rpgbg"}},
    }


def generate_one(pos_prompt: str, out_path: Path, timeout: int = 240) -> None:
    resp = requests.post(f"{COMFYUI_URL}/prompt", json={"prompt": build_workflow(pos_prompt)})
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
                    im.save(out_path, "webp", quality=88)
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
    jobs = list(BGS.items())
    print(f"배경 {len(jobs)}장 생성 시작 (저장 위치: {ART_DIR})\n")
    for i, (slug, desc) in enumerate(jobs, 1):
        name = f"bg-{slug}"
        t0 = time.time()
        print(f"[{i}/{len(jobs)}] {name} 생성 중...", end="", flush=True)
        try:
            generate_one(BASE + desc, ART_DIR / f"{name}.webp")
            print(f" 완료 ({time.time()-t0:.0f}s)")
        except Exception as e:
            print(f" 실패: {e}")
    print(f"\n=== 끝! {ART_DIR} 확인하세요 ===")


if __name__ == "__main__":
    main()
