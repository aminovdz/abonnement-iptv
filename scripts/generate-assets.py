import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUTPUT_DIR = "/Users/Mc/Documents/antigravity/iptv FRANCE/public/images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"

def get_font(size, bold=False):
    path = FONT_BOLD if bold else FONT_REGULAR
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def draw_radial_glow(draw, center_x, center_y, radius, color, max_alpha=120):
    r, g, b = color
    steps = 40
    for i in range(steps, 0, -1):
        cur_radius = int(radius * (i / steps))
        alpha = int(max_alpha * (1.0 - (i / steps)) ** 1.8)
        bbox = [
            center_x - cur_radius,
            center_y - cur_radius,
            center_x + cur_radius,
            center_y + cur_radius
        ]
        draw.ellipse(bbox, fill=(r, g, b, alpha))

def draw_rounded_card(img, bbox, fill_color, border_color, border_width=1, radius=20):
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    d.rounded_rectangle(bbox, radius=radius, fill=fill_color, outline=border_color, width=border_width)
    img.alpha_composite(overlay)

def create_og_banner():
    width, height = 1200, 630
    base = Image.new("RGBA", (width, height), (7, 8, 14, 255))
    glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)

    draw_radial_glow(glow_draw, 200, 150, 450, (0, 85, 212), max_alpha=90)
    draw_radial_glow(glow_draw, 1050, 500, 400, (220, 38, 38), max_alpha=75)
    draw_radial_glow(glow_draw, 600, 650, 500, (0, 85, 212), max_alpha=60)
    base.alpha_composite(glow_layer)

    grid_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid_layer)
    for x in range(0, width, 60):
        gd.line([(x, 0), (x, height)], fill=(255, 255, 255, 6), width=1)
    for y in range(0, height, 60):
        gd.line([(y, 0), (width, y)], fill=(255, 255, 255, 6), width=1)
    base.alpha_composite(grid_layer)

    card_bbox = [80, 70, width - 80, height - 70]
    draw_rounded_card(base, card_bbox, (18, 20, 34, 235), (255, 255, 255, 30), border_width=2, radius=28)

    draw = ImageDraw.Draw(base)
    tag_font = get_font(14, bold=True)
    draw.rounded_rectangle([120, 110, 390, 145], radius=18, fill=(0, 85, 212, 50), outline=(0, 85, 212, 120), width=1)
    draw.text((135, 120), "OFFRE OFFICIELLE FRANCE 2026", fill=(96, 165, 250, 255), font=tag_font)

    title_font = get_font(52, bold=True)
    draw.text((120, 175), "Abonnement IPTV France", fill=(255, 255, 255, 255), font=title_font)

    sub_font = get_font(24, bold=False)
    draw.text((120, 245), "Streaming 4K / 8K UHD • Technologie Anti-Freeze 9.8™ • Sans Coupure", fill=(180, 195, 220, 255), font=sub_font)

    badge_y = 310
    features = [
        ("Qualite Flux", "4K 60 FPS Reelle", (96, 165, 250)),
        ("Stabilite", "99.98% Anti-Coupure", (16, 185, 129)),
        ("Assistance", "WhatsApp 7j/7 en Francais", (245, 158, 11)),
        ("Tarif Annuel", "55 € / an (Lecteur Inclus)", (239, 68, 68))
    ]

    card_w = 220
    gap = 20
    start_x = 120
    for idx, (lbl, val, col) in enumerate(features):
        bx = start_x + idx * (card_w + gap)
        draw.rounded_rectangle([bx, badge_y, bx + card_w, badge_y + 85], radius=16, fill=(10, 12, 22, 200), outline=(255, 255, 255, 20), width=1)
        draw.text((bx + 16, badge_y + 16), lbl, fill=(150, 150, 170, 255), font=get_font(12, bold=False))
        draw.text((bx + 16, badge_y + 42), val, fill=col, font=get_font(14, bold=True))

    bot_y = 440
    draw.line([(120, bot_y), (width - 120, bot_y)], fill=(255, 255, 255, 25), width=1)
    bot_font = get_font(16, bold=True)
    draw.text((120, bot_y + 25), "✓ Compatible Smart TV connectees, cles 4K, boitiers TV, smartphones & PC", fill=(220, 225, 240, 255), font=bot_font)
    draw.text((120, bot_y + 55), "✓ Activation automatique en 2 minutes chrono • Garantie 24h satisfait ou rembourse", fill=(140, 155, 180, 255), font=get_font(14, bold=False))

    draw.rounded_rectangle([width - 340, bot_y + 20, width - 120, bot_y + 75], radius=14, fill=(16, 185, 129, 30), outline=(16, 185, 129, 80), width=1)
    draw.text((width - 325, bot_y + 35), "★ 4.94 / 5 (2 460+ Avis Clients)", fill=(52, 211, 153, 255), font=get_font(13, bold=True))

    out_path = os.path.join(OUTPUT_DIR, "og-banner.webp")
    base.convert("RGB").save(out_path, "WEBP", quality=92)
    print("Created:", out_path)

def create_hero_bg():
    width, height = 1920, 1080
    base = Image.new("RGBA", (width, height), (7, 8, 14, 255))
    glow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow_layer)

    draw_radial_glow(gd, 300, 250, 700, (0, 85, 212), max_alpha=85)
    draw_radial_glow(gd, 1650, 400, 650, (220, 38, 38), max_alpha=70)
    draw_radial_glow(gd, 960, 900, 800, (0, 85, 212), max_alpha=50)
    base.alpha_composite(glow_layer)

    grid_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(grid_layer)
    for x in range(0, width, 80):
        g_draw.line([(x, 0), (x, height)], fill=(255, 255, 255, 5), width=1)
    for y in range(0, height, 80):
        g_draw.line([(0, y), (width, y)], fill=(255, 255, 255, 5), width=1)
    base.alpha_composite(grid_layer)

    out_path = os.path.join(OUTPUT_DIR, "hero-bg.webp")
    base.convert("RGB").save(out_path, "WEBP", quality=90)
    print("Created:", out_path)

def create_editorial_image(filename, category, title, subtitle, highlight_badge, badge_color, spec_lines=None):
    width, height = 1200, 675
    base = Image.new("RGBA", (width, height), (8, 10, 18, 255))
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)

    draw_radial_glow(gd, 200, 200, 450, badge_color, max_alpha=70)
    draw_radial_glow(gd, 1000, 500, 450, (0, 85, 212), max_alpha=60)
    base.alpha_composite(glow)

    grid = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    grd = ImageDraw.Draw(grid)
    for x in range(0, width, 50):
        grd.line([(x, 0), (x, height)], fill=(255, 255, 255, 4), width=1)
    for y in range(0, height, 50):
        grd.line([(0, y), (width, y)], fill=(255, 255, 255, 4), width=1)
    base.alpha_composite(grid)

    card_bbox = [60, 60, width - 60, height - 60]
    draw_rounded_card(base, card_bbox, (14, 17, 30, 230), (255, 255, 255, 25), border_width=2, radius=24)

    draw = ImageDraw.Draw(base)

    r, g, b = badge_color
    draw.rounded_rectangle([100, 100, 380, 140], radius=16, fill=(r, g, b, 40), outline=(r, g, b, 120), width=1)
    draw.text((115, 112), category.upper(), fill=(r, g, b, 255), font=get_font(13, bold=True))

    draw.text((100, 175), title, fill=(255, 255, 255, 255), font=get_font(40, bold=True))
    draw.text((100, 245), subtitle, fill=(175, 190, 215, 255), font=get_font(20, bold=False))

    fbox = [100, 310, width - 100, 500]
    draw.rounded_rectangle(fbox, radius=18, fill=(8, 10, 18, 180), outline=(255, 255, 255, 18), width=1)

    draw.rounded_rectangle([130, 340, 560, 385], radius=14, fill=(r, g, b, 30), outline=(r, g, b, 80), width=1)
    draw.text((150, 352), highlight_badge, fill=(255, 255, 255, 255), font=get_font(14, bold=True))

    spec_font = get_font(15, bold=False)
    if spec_lines:
        draw.text((130, 410), spec_lines[0], fill=(210, 220, 240, 255), font=spec_font)
        draw.text((130, 445), spec_lines[1], fill=(210, 220, 240, 255), font=spec_font)
    else:
        draw.text((130, 410), "✓ Serveurs interconnectes TH2 Paris & LyonIX • Latence < 10 ms", fill=(210, 220, 240, 255), font=spec_font)
        draw.text((130, 445), "✓ Flux stabilises 4K UHD 60 FPS • Technologie Anti-Freeze 9.8™ integree", fill=(210, 220, 240, 255), font=spec_font)

    draw.text((100, 545), "Abonnement IPTV France — Plateforme Officielle 2026", fill=(120, 135, 160, 255), font=get_font(14, bold=True))
    draw.text((width - 360, 545), "www.abonnement-iptv.cloud", fill=(96, 165, 250, 255), font=get_font(14, bold=True))

    out_path = os.path.join(OUTPUT_DIR, filename)
    base.convert("RGB").save(out_path, "WEBP", quality=92)
    print("Created:", out_path)

# 1. OpenGraph Banner
create_og_banner()

# 2. Hero Background
create_hero_bg()

# 3. Blog 1: Ligue 1 Streaming 4K
create_editorial_image(
    "ligue-1-streaming-4k.webp",
    "Sport & Football France",
    "Regarder la Ligue 1 en Direct 4K UHD",
    "Guide 2026 : 100% des Matchs de Football en 4K UHD pour 55 € / an",
    "⚽ DISPOSITIF SPÉCIAL LIGUE 1 • STREAMING 4K",
    (220, 38, 38),
    [
        "✓ 100% des matchs de Ligue 1 & coupes européennes en direct",
        "✓ Qualité 4K 60 FPS réelle • Zéro décalage de score avec les voisins"
    ]
)

# 4. Blog 2: Legalite IPTV France
create_editorial_image(
    "iptv-legal-france.webp",
    "Cadre Juridique & Arcom",
    "L'IPTV est-il Légal en France ?",
    "Réglementation, Sécurité des Données et Respect de la Vie Privée",
    "⚖️ ANALYSE JURIDIQUE & PROTECTION RGPD",
    (0, 85, 212),
    [
        "✓ Chiffrement SSL 256 bits intégral • Aucune conservation de logs",
        "✓ Analyse des textes de loi, rôle de l'Arcom et droits des consommateurs"
    ]
)

# 5. Blog 3: Meilleures Applications IPTV
create_editorial_image(
    "apps-iptv-guide.webp",
    "Tutoriels & Appareils",
    "Top 5 des Meilleures Applications IPTV",
    "TiviMate, IBO Player & IPTV Smarters : Guide de Configuration Pas-à-Pas",
    "📺 OPTIMISÉ SMART TV & BOÎTIERS MULTIMÉDIAS 4K",
    (16, 185, 129),
    [
        "✓ Zapping instantané sous la seconde (< 0,8 s) • Replay 7 jours complet",
        "✓ Compatible Smart TV connectées, clés 4K, boîtiers de salon et mobiles"
    ]
)

# 6. Blog 4: Code IPTV Gratuit & Test
create_editorial_image(
    "code-iptv-gratuit.webp",
    "Guide d'Achat & Test 24h",
    "Code IPTV Gratuit vs Ligne Privée Dédiée",
    "Pourquoi les Codes Publics Coupent-ils ? Obtenir un Accès Stable 24h",
    "⚡ ACTIVATION EXPRESS EN 2 MINUTES SUR WHATSAPP",
    (245, 158, 11),
    [
        "✓ Bande passante dédiée 10 Gbps exclusive sans saturation",
        "✓ Identifiants Xtream Codes sécurisés livrés en 2 minutes chrono"
    ]
)

# 7. Landing V2: Sports Streaming 4K
create_editorial_image(
    "sports-streaming-4k.webp",
    "Sport en Direct 60 FPS",
    "Football, Ligue 1 & Compétitions en 4K UHD",
    "Tous les championnats français et européens en direct sans interruption",
    "⚽ DISPOSITIF SPORT 4K 60FPS • TECHNOLOGIE ANTI-FREEZE",
    (220, 38, 38),
    [
        "✓ Ligue 1, Champions League, Top 14 Rugby, Formule 1 & Tennis",
        "✓ Latence réduite à < 8 ms via serveurs TH2 Paris & LyonIX"
    ]
)

# 8. Landing V3: Cinema & Series VOD 4K
create_editorial_image(
    "cinema-vod-4k.webp",
    "Cinéma & Séries Ultra HD",
    "Plus de 85 000 Films & Séries en 4K HDR",
    "Catalogue VOD illimité avec son Dolby Digital 5.1 et sous-titres français",
    "🎬 VOD ILLIMITÉE 4K HDR • ACTUALISÉE CHAQUE SEMAINE",
    (168, 85, 247),
    [
        "✓ Dernières sorties cinéma, intégrales de séries et documentaires 4K",
        "✓ Choix des langues (VF / VOSTFR) et reprise de lecture multi-écrans"
    ]
)

# 9. Comparison Hub & Pages: Comparatif IPTV France
create_editorial_image(
    "comparatif-iptv-france.webp",
    "Baromètre Indépendant 2026",
    "Comparatif des Meilleurs Abonnements IPTV",
    "Classement des offres en France : stabilité des serveurs, prix et support",
    "🏆 CLASSÉ N°1 DU MARCHÉ FRANÇAIS • NOTE 4.94 / 5",
    (245, 158, 11),
    [
        "✓ Formule 12 Mois à 55 € tout inclus vs 75 € à 90 € chez les concurrents",
        "✓ Lecteur Premium inclus offert • Garantie satisfait ou remboursé 24h"
    ]
)

# 10. Regional Network: Reseau France CDN
create_editorial_image(
    "reseau-france-cdn.webp",
    "Couverture Nationale Fibre",
    "Réseau CDN Déployé sur les Métropoles Françaises",
    "Paris, Marseille, Lyon, Toulouse, Nice, Nantes, Strasbourg, Bordeaux, Lille",
    "🇫🇷 DORSALE OPTIQUE DIRECTE • LATENCE MOYENNE 7 MS",
    (0, 85, 212),
    [
        "✓ Interconnexion directe Telehouse TH2, LyonIX et Interxion MRS",
        "✓ 100% compatible avec les box fibre optique de tous les opérateurs"
    ]
)

# 11. Referral: Programme de Parrainage
create_editorial_image(
    "programme-parrainage-iptv.webp",
    "Programme de Parrainage",
    "Parrainez vos Proches et Gagnez 1 Mois Offert",
    "Pour chaque ami parrainé, bénéficiez de 30 jours d'abonnement supplémentaires",
    "🎁 1 MOIS OFFERT POUR VOUS • 10% DE RÉDUCTION POUR VOTRE FILLEUL",
    (16, 185, 129),
    [
        "✓ Parrainages cumulables sans aucune limite dans le temps",
        "✓ Activation immédiate sur simple message à notre support WhatsApp"
    ]
)

# 12. Support & Contact: Support Technique France
create_editorial_image(
    "support-technique-france.webp",
    "Assistance Francophone 24/7",
    "Support Technique Dédié 7j/7 sur WhatsApp",
    "Nos techniciens vous accompagnent en direct pour l'installation et le paramétrage",
    "💬 RÉPONSE GARANTIE EN MOINS DE 3 MINUTES PAR WHATSAPP",
    (0, 85, 212),
    [
        "✓ Configuration guidée pas-à-pas pour Smart TV et boîtiers multimédias",
        "✓ Assistance réactive en français 365 jours par an sans interruption"
    ]
)

# 13. Refund: Garantie Remboursement 24h
create_editorial_image(
    "garantie-remboursement-24h.webp",
    "Sécurité & Engagement",
    "Garantie 24 Heures Satisfait ou Remboursé",
    "Testez la qualité et la stabilité de nos flux en toute sérénité",
    "🛡️ REMBOURSEMENT INTÉGRAL EN 24H SANS FORMALITÉ",
    (16, 185, 129),
    [
        "✓ Aucun risque financier : testez nos chaînes 4K et notre Anti-Freeze 9.8™",
        "✓ Remboursement direct sur votre moyen de paiement sous 24 heures"
    ]
)

# 14. Interface Lecteur IPTV
create_editorial_image(
    "interface-lecteur-iptv.webp",
    "Lecteur Multimédia Inclus",
    "Interface Épurée & Lecteur Premium Offert",
    "Une navigation ultra-rapide et ergonomique sur tous vos écrans de salon",
    "📺 APPLICATION LECTEUR PREMIUM OFFERTE AVEC LE FORFAIT 12 MOIS",
    (96, 165, 250),
    [
        "✓ Zapping ultra-fluide sous la seconde (< 0,8 s) • Favoris organisés",
        "✓ Guide électronique des programmes EPG et fonction Replay 7 jours"
    ]
)

# 15. Abonnement 12 Mois Flagship Hero
create_editorial_image(
    "abonnement-iptv-12-mois.webp",
    "Formule Bestseller 2026",
    "Abonnement IPTV 12 Mois — 55 €",
    "Seulement ~4,16 €/mois • Lecteur Premium Offert Inclus • 4K 60 FPS Anti-Freeze",
    "★ NOTRE OFFRE LA PLUS POPULAIRE & ÉCONOMIQUE EN FRANCE",
    (16, 185, 129),
    [
        "✓ 12 Mois d'accès illimité sans engagement • Licence Lecteur Premium offerte",
        "✓ Activation immédiate sur WhatsApp en 2 min • Garantie 24h satisfait ou remboursé"
    ]
)

# 16. Pack 12 Mois Bundle
create_editorial_image(
    "pack-12-mois-bundle.webp",
    "Pack Tout Compris 55 €",
    "Le Pack Complet 12 Mois + Lecteur",
    "Tout ce dont vous avez besoin pour un streaming ultra-fluide sur vos écrans",
    "🎁 LECTEUR MULTIMÉDIA PREMIUM INCLUS GRATUITEMENT (VALEUR 15 €)",
    (147, 51, 234),
    [
        "✓ Flux 4K & 8K HDR optimisés pour la fibre optique • Anti-Freeze 9.8™",
        "✓ Guide des programmes EPG complet + Replay 7 jours + Multi-langues VF/VO"
    ]
)

# 17. Comparatif 12 Mois vs Mensuel
create_editorial_image(
    "comparatif-12-mois-vs-mensuel.webp",
    "Économie Garantie",
    "12 Mois (55 €) vs Forfait Mensuel (96 €)",
    "Économisez plus de 41 € par an avec la formule recommandée",
    "💰 45% D'ÉCONOMIE IMMÉDIATE + LECTEUR OFFERT",
    (245, 158, 11),
    [
        "✓ Formule 12 Mois = 4,16 € / mois vs 8 € / mois en formule découverte",
        "✓ Tranquillité garantie 365 jours sans risque d'interruption lors des matchs"
    ]
)

# 18. Smart TV Device Image
create_editorial_image(
    "smart-tv-streaming-4k.webp",
    "Smart TV Connectée",
    "Streaming Direct sur Smart TV 4K",
    "Compatible téléviseurs connectés récents (systèmes TV intégrés)",
    "📺 LECTURE DIRECTE SANS DÉCODEUR NI CÂBLE SUPERFLU",
    (0, 85, 212),
    [
        "✓ Compatible téléviseurs connectés avec systèmes récents",
        "✓ Qualité 4K 60 FPS • Télécommande native • Zapping sous la seconde"
    ]
)

# 19. Boîtier TV & Clé Stick Image
create_editorial_image(
    "boitier-tv-streaming-4k.webp",
    "Clés & Boîtiers HDMI",
    "Boîtiers TV & Clés Multimédias 4K",
    "Transformez n'importe quel écran en lecteur haute performance",
    "⚡ PERFORMANCE MAXIMALE • ANTI-FREEZE 9.8™",
    (220, 38, 38),
    [
        "✓ Compatible clés TV 4K, boîtiers multimédias et passerelles HDMI",
        "✓ Fluidité maximale, décodage matériel HEVC/H.265 et son Dolby Digital"
    ]
)

# 20. Mobile Streaming Image
create_editorial_image(
    "mobile-streaming-4k.webp",
    "Nomade & Mobile",
    "Smartphones & Tablettes 4G / 5G",
    "Emportez votre télévision partout en déplacement et vacances",
    "📱 COMPATIBLE TOUS SMARTPHONES & TABLETTES",
    (16, 185, 129),
    [
        "✓ Compatible Android & iOS • Fonction de diffusion Cast vers grand écran",
        "✓ Consommation de données optimisée • Flux adaptatif basse latence"
    ]
)

# 21. PC & Laptop Streaming Image
create_editorial_image(
    "pc-streaming-4k.webp",
    "Ordinateurs & Mac",
    "PC Windows, Mac & Web Player",
    "Visionnez directement depuis votre navigateur ou logiciel favori",
    "💻 COMPATIBLE WINDOWS, MACOS & LECTEURS WEB",
    (99, 102, 241),
    [
        "✓ Lecteur Web accessible sans installation • Compatible lecteurs PC",
        "✓ Multitâche fluide et reprise de lecture en un clic"
    ]
)

# 22. French IPTV Hero Asset
create_editorial_image(
    "french-iptv-hero.webp",
    "French IPTV Streaming 2026",
    "Best French IPTV Service Worldwide",
    "Watch French Channels, Ligue 1 & VOD in 4K 60 FPS Anti-Freeze",
    "🇫🇷 OFFICIAL FRENCH IPTV CHANNELS • 55 € / YEAR (PLAYER INCLUDED)",
    (0, 85, 212),
    [
        "✓ 100% French Channels, Sports in French commentary, VOD in VF & VOSTFR",
        "✓ Anti-Freeze 9.8™ • Worldwide CDN streaming • Instant WhatsApp setup"
    ]
)

# 23. French IPTV Worldwide Access
create_editorial_image(
    "french-iptv-worldwide.webp",
    "Expats & Global Access",
    "French IPTV Anywhere in the World",
    "USA, UK, Canada, Europe, Dubai & Worldwide Access with Zero Geoblocking",
    "🌍 LOW-LATENCY GLOBAL CDN NETWORK • 99.98% UPTIME",
    (16, 185, 129),
    [
        "✓ No VPN required • Direct high-speed connection from any country",
        "✓ Compatible with Smart TVs, 4K streaming sticks, tablets, phones & PC"
    ]
)

print("All visual assets successfully generated in:", OUTPUT_DIR)
