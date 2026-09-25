#!/usr/bin/env python3
"""
Downloads and converts cinematic ultra-HD photos into public/images/*.webp
Includes both our AI-generated cinema/stadium masterpieces and curated high-resolution photography.
"""

import os
import ssl
import urllib.request
from PIL import Image, ImageEnhance, ImageFilter

OUTPUT_DIR = "/Users/Mc/Documents/antigravity/iptv FRANCE/public/images"
BRAIN_DIR = "/Users/Mc/.gemini/antigravity/brain/03e82bdb-2777-49e8-b90a-ddf96c23141e"
os.makedirs(OUTPUT_DIR, exist_ok=True)

AI_ASSETS = {
    "interface-lecteur-iptv.webp": os.path.join(BRAIN_DIR, "home_cinema_oled_1790349296144.jpg"),
    "abonnement-iptv-12-mois.webp": os.path.join(BRAIN_DIR, "home_cinema_oled_1790349296144.jpg"),
    "pack-12-mois-bundle.webp": os.path.join(BRAIN_DIR, "home_cinema_oled_1790349296144.jpg"),
    "ligue-1-streaming-4k.webp": os.path.join(BRAIN_DIR, "stadium_football_action_1790349329903.jpg"),
    "sports-streaming-4k.webp": os.path.join(BRAIN_DIR, "stadium_football_action_1790349329903.jpg"),
    "cinema-vod-4k.webp": os.path.join(BRAIN_DIR, "private_home_theater_1790349365995.jpg"),
}

UNSPLASH_ASSETS = {
    "french-iptv-hero.webp": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=1400&h=788&q=90",
    "french-iptv-worldwide.webp": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1400&h=788&q=90",
    "reseau-france-cdn.webp": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1400&h=788&q=90",
    "support-technique-france.webp": "https://images.unsplash.com/photo-1534536281715-e28d76689b4d?auto=format&fit=crop&w=1400&h=788&q=90",
    "smart-tv-streaming-4k.webp": "https://images.unsplash.com/photo-1593784991095-a205069470b6?auto=format&fit=crop&w=1400&h=788&q=90",
    "apps-iptv-guide.webp": "https://images.unsplash.com/photo-1577741314755-048d8525d31e?auto=format&fit=crop&w=1400&h=788&q=90",
    "boitier-tv-streaming-4k.webp": "https://images.unsplash.com/photo-1546868871-7041f2a55e12?auto=format&fit=crop&w=1400&h=788&q=90",
    "pc-streaming-4k.webp": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=1400&h=788&q=90",
    "mobile-streaming-4k.webp": "https://images.unsplash.com/photo-1512499617640-c74ae3a79d37?auto=format&fit=crop&w=1400&h=788&q=90",
    "iptv-legal-france.webp": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&w=1400&h=788&q=90",
    "code-iptv-gratuit.webp": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1400&h=788&q=90",
    "programme-parrainage-iptv.webp": "https://images.unsplash.com/photo-1511632765486-a01980e01a18?auto=format&fit=crop&w=1400&h=788&q=90",
    "garantie-remboursement-24h.webp": "https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=1400&h=788&q=90",
    "comparatif-iptv-france.webp": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1400&h=788&q=90",
    "comparatif-12-mois-vs-mensuel.webp": "https://images.unsplash.com/photo-1600566753376-12c8ab7fb75b?auto=format&fit=crop&w=1400&h=788&q=90",
}

def resize_and_crop(img, target_width=1200, target_height=675):
    """Crops and resizes image to exact target dimensions while preserving aspect ratio."""
    img_ratio = img.width / img.height
    target_ratio = target_width / target_height

    if img_ratio > target_ratio:
        # Image is wider than target
        new_width = int(img.height * target_ratio)
        offset_x = (img.width - new_width) // 2
        img = img.crop((offset_x, 0, offset_x + new_width, img.height))
    else:
        # Image is taller than target
        new_height = int(img.width / target_ratio)
        offset_y = (img.height - new_height) // 2
        img = img.crop((0, offset_y, img.width, offset_y + new_height))

    return img.resize((target_width, target_height), Image.Resampling.LANCZOS)

def process_ai_images():
    print("Processing AI-generated cinematic assets...")
    for filename, source_path in AI_ASSETS.items():
        if os.path.exists(source_path):
            with Image.open(source_path) as img:
                img_rgb = img.convert("RGB")
                processed = resize_and_crop(img_rgb, 1200, 675)
                # Enhance subtle sharpness and contrast for cinematic crispness
                enhancer = ImageEnhance.Contrast(processed)
                processed = enhancer.enhance(1.05)
                out_path = os.path.join(OUTPUT_DIR, filename)
                processed.save(out_path, "WEBP", quality=88)
                print(f"  ✓ Saved AI asset: {filename} ({os.path.getsize(out_path) // 1024} KB)")
        else:
            print(f"  ✗ Missing source: {source_path}")

def process_hero_bg():
    print("Generating atmospheric hero-bg.webp...")
    source_path = AI_ASSETS["interface-lecteur-iptv.webp"]
    if os.path.exists(source_path):
        with Image.open(source_path) as img:
            img_rgb = img.convert("RGB")
            processed = resize_and_crop(img_rgb, 1920, 1080)
            # Apply subtle dark mood lighting and soft blur
            brightness = ImageEnhance.Brightness(processed)
            processed = brightness.enhance(0.4)
            processed = processed.filter(ImageFilter.GaussianBlur(radius=6))
            out_path = os.path.join(OUTPUT_DIR, "hero-bg.webp")
            processed.save(out_path, "WEBP", quality=85)
            print(f"  ✓ Saved hero-bg: hero-bg.webp ({os.path.getsize(out_path) // 1024} KB)")

def process_og_banner():
    print("Generating og-banner.webp...")
    source_path = AI_ASSETS["interface-lecteur-iptv.webp"]
    if os.path.exists(source_path):
        with Image.open(source_path) as img:
            img_rgb = img.convert("RGB")
            processed = resize_and_crop(img_rgb, 1200, 630)
            out_path = os.path.join(OUTPUT_DIR, "og-banner.webp")
            processed.save(out_path, "WEBP", quality=88)
            print(f"  ✓ Saved og-banner: og-banner.webp ({os.path.getsize(out_path) // 1024} KB)")

def download_unsplash_images():
    print("Downloading curated cinematic photography from Unsplash...")
    ctx = ssl._create_unverified_context()
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}

    for filename, url in UNSPLASH_ASSETS.items():
        out_path = os.path.join(OUTPUT_DIR, filename)
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
                from io import BytesIO
                data = resp.read()
                with Image.open(BytesIO(data)) as img:
                    img_rgb = img.convert("RGB")
                    processed = resize_and_crop(img_rgb, 1200, 675)
                    enhancer = ImageEnhance.Contrast(processed)
                    processed = enhancer.enhance(1.04)
                    processed.save(out_path, "WEBP", quality=88)
                    print(f"  ✓ Downloaded & converted: {filename} ({os.path.getsize(out_path) // 1024} KB)")
        except Exception as e:
            print(f"  ✗ Error downloading {filename}: {e}")

if __name__ == "__main__":
    process_ai_images()
    process_hero_bg()
    process_og_banner()
    download_unsplash_images()
    print("\nAll cinematic images successfully created!")
