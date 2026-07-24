#!/usr/bin/env python3
"""lpc_build.py — MultiUs「代码捏人」管线

基于 Universal LPC Spritesheet Character Generator 的素材与图层定义，
用 PIL 逐层 alpha 合成角色 sprite sheet，并裁出正面头像。

用法:
    python tools/lpc_build.py tools/chars.json            # 构建配置里的所有角色
    python tools/lpc_build.py tools/chars.json --only oscar

配置格式 (JSON):
{
  "characters": [
    {
      "name": "oscar",
      "body": "male",                    // male/female/teen/child/muscular/pregnant
      "face_zoom": 6,                    // 可选，头像放大倍数，默认 6
      "layers": [
        {"def": "body",          "variant": "light"},
        {"def": "feet_shoes",    "variant": "charcoal"},
        {"def": "legs_pants",    "variant": "blue"},
        {"def": "torso_clothes_longsleeve", "variant": "charcoal"},
        {"def": "head_human_male", "variant": "light"},   // 关键！body 是无头的
        {"def": "eyes",          "variant": "gray"},
        {"def": "eyebrows_thin", "variant": "black"},
        {"def": "hair_messy1",   "variant": "black"}
      ]
    }
  ]
}

def 对应 vendor/lpc/sheet_definitions/<def>.json；variant 是该图层定义的
variants 之一（含空格的 variant 自动转为下划线文件名）。图层按定义里的
zPos 升序叠加（与官方生成器一致）。缺素材时会明确报错并跳过该角色。

注意：Universal LPC 的 body 素材是「无头身体」（modular heads），
必须搭配 head_human_male / head_human_female 图层（zPos 100，本地补写的
定义，数据来自生成器 index.html），否则角色没有头、脸色发黑。

关键 zPos 链: body 10 < shoes 15 < pants 20 < torso 35
             < head 100 < eyes 105 < eyebrows 106 < hair 120

输出:
    assets/chars/<name>.png        完整 sprite sheet (832x2944, 64px 帧)
    assets/chars/<name>_face.png   正面头像（朝南站立帧头部，最近邻放大）

帧布局 (LPC universal, 64x64 帧, 每行动画 4 方向 n/w/s/e):
    spellcast 0-3 / thrust 4-7 / walk 8-11 / slash 12-15 / shoot 16-19 /
    hurt 20 / climb 21 / idle 22-25 / jump 26-29 / sit 30-33 / run 34-37 ...
    朝南行走 = 第 10 行, 共 9 帧; 第 0 帧即站立姿势。
"""

import argparse
import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
LPC = ROOT / "vendor" / "lpc"
SHEET_DEFS = LPC / "sheet_definitions"
SPRITES = LPC / "spritesheets"
OUT_DIR = ROOT / "assets" / "chars"

FRAME = 64
SHEET_W, SHEET_H = 832, 2944  # 46 rows * 64

# 朝南行走帧（row 10）第 0 帧 = 站立姿势，所有图层都包含这一帧
SOUTH_FRAME_X, SOUTH_FRAME_Y = 0, 10 * FRAME
# 头部搜索区域（帧内上半部分、中间列，避开两侧手臂），
# 实际裁剪框由 alpha bbox 自动确定
HEAD_REGION = (14, 0, 50, 36)
HEAD_MARGIN = 1

# body 类型回退顺序：有些图层只定义了部分体型
BODY_FALLBACKS = {
    "male": ["male", "muscular", "teen", "female"],
    "muscular": ["muscular", "male", "teen"],
    "female": ["female", "pregnant", "teen", "male"],
    "pregnant": ["pregnant", "female"],
    "teen": ["teen", "male", "female"],
    "child": ["child", "male"],
}


def resolve_layer(body_type, layer_spec, warnings):
    """根据 sheet definition 解析图层的 PNG 路径和 zPos。"""
    def_name = layer_spec["def"]
    variant = layer_spec["variant"]
    def_path = SHEET_DEFS / f"{def_name}.json"
    if not def_path.exists():
        raise FileNotFoundError(f"sheet definition 不存在: {def_path}")
    definition = json.loads(def_path.read_text(encoding="utf-8"))

    entries = []  # (zPos, png_path)
    for key, layer in definition.items():
        if not key.startswith("layer_"):
            continue
        prefix = None
        for bt in BODY_FALLBACKS.get(body_type, [body_type]):
            if bt in layer:
                prefix = layer[bt]
                break
        if prefix is None:
            warnings.append(f"  [!] {def_name}.{key} 不支持体型 {body_type}，跳过")
            continue
        png = SPRITES / prefix / f"{variant.replace(' ', '_')}.png"
        if not png.exists():
            raise FileNotFoundError(f"素材缺失: {png} (def={def_name}, variant={variant})")
        entries.append((int(layer.get("zPos", 0)), png))
    return entries


def build_character(char):
    name = char["name"]
    body_type = char.get("body", "male")
    warnings = []

    layers = []
    for spec in char["layers"]:
        layers.extend(resolve_layer(body_type, spec, warnings))
    layers.sort(key=lambda t: t[0])  # zPos 升序，与官方生成器一致

    canvas = Image.new("RGBA", (SHEET_W, SHEET_H), (0, 0, 0, 0))
    for zpos, png in layers:
        img = Image.open(png).convert("RGBA")
        if img.size[0] != SHEET_W:
            raise ValueError(f"{png} 宽度异常: {img.size}")
        canvas.alpha_composite(img, (0, 0))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    sheet_path = OUT_DIR / f"{name}.png"
    canvas.save(sheet_path)

    # 头像：朝南站立帧的头部区域（自动按 alpha bbox 裁剪），最近邻放大保持像素感
    zoom = int(char.get("face_zoom", 6))
    fx, fy = SOUTH_FRAME_X, SOUTH_FRAME_Y
    frame = canvas.crop((fx, fy, fx + FRAME, fy + FRAME))
    region = frame.crop(HEAD_REGION)
    bbox = region.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError(f"{name}: 朝南帧头部区域为空")
    left = max(0, bbox[0] - HEAD_MARGIN)
    top = max(0, bbox[1] - HEAD_MARGIN)
    right = min(region.width, bbox[2] + HEAD_MARGIN)
    bottom = min(region.height, bbox[3] + HEAD_MARGIN)
    head = region.crop((left, top, right, bottom))
    face = head.resize((head.width * zoom, head.height * zoom), Image.NEAREST)
    face_path = OUT_DIR / f"{name}_face.png"
    face.save(face_path)

    # 简单 QA：非透明像素占比
    alpha = canvas.getchannel("A")
    opaque = sum(1 for v in alpha.getdata() if v > 0)
    ratio = opaque / (SHEET_W * SHEET_H)

    for w in warnings:
        print(w)
    print(f"[OK] {name}: {sheet_path} ({ratio:.2%} 非透明) + {face_path}")
    return sheet_path, face_path


def main():
    ap = argparse.ArgumentParser(description="LPC 代码捏人管线")
    ap.add_argument("config", help="角色配置 JSON 路径")
    ap.add_argument("--only", help="只构建指定名字的角色")
    args = ap.parse_args()

    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    for char in config["characters"]:
        if args.only and char["name"] != args.only:
            continue
        try:
            build_character(char)
        except (FileNotFoundError, ValueError) as e:
            print(f"[FAIL] {char['name']}: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
