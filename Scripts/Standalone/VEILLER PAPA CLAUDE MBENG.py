"""
Generer_Invitation_Veillee.py
-----------------------------
• Produit une image A4 (300 dpi) au format PNG
• Design ivoire + liseré or + zone photo
• Texte centré : titre, nom, dates, détails, déroulé
"""

import os
from PIL import Image, ImageDraw, ImageFont

# --------------------------------------------------------------------------
# 1. PARAMÈTRES GÉNÉRAUX
# --------------------------------------------------------------------------
WIDTH, HEIGHT = 2480, 3508        # A4 @300 dpi
BACKGROUND   = (246, 245, 240)    # ivoire
GOLD         = (203, 161, 53)     # or
MARGIN       = 120                # marge pour le cadre

OUTPUT_DIR   = "output"           # dossier où sera enregistré le PNG
FILENAME     = "invitation_veillee_fotie.png"

# --------------------------------------------------------------------------
# 2. CHARGEMENT DES POLICES (Arial → Unicode OK)
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# POLICES : tentative TrueType, sinon police par défaut
# --------------------------------------------------------------------------
try:
    font_path = r"C:\Windows\Fonts\arial.ttf"      # change si besoin
    TITLE_FONT    = ImageFont.truetype(font_path, 140)
    SUBTITLE_FONT = ImageFont.truetype(font_path, 64)
    BODY_FONT     = ImageFont.truetype(font_path, 58)
except Exception as e:
    print("⚠️  Problème police :", e, "\n→ passage à la police par défaut.")
    TITLE_FONT = SUBTITLE_FONT = BODY_FONT = ImageFont.load_default()


# --------------------------------------------------------------------------
# 3. OUTIL : TEXTE CENTRÉ (compatible Pillow 9 & 10)
# --------------------------------------------------------------------------
def center_text(draw, text, y, font, color=(0, 0, 0)):
    """
    Dessine 'text' centré horizontalement à la coordonnée verticale 'y'
    et renvoie la nouvelle position verticale (bas du texte).
    """
    if hasattr(draw, "textbbox"):                   # Pillow ≥10
        bbox = draw.textbbox((0, 0), text, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    else:                                           # Pillow 9.x
        w, h = draw.textsize(text, font=font)

    draw.text(((WIDTH - w) / 2, y), text, font=font, fill=color)
    return y + h

# --------------------------------------------------------------------------
# 4. CRÉATION DU CANVAS
# --------------------------------------------------------------------------
img  = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
draw = ImageDraw.Draw(img)

# Cadre or
draw.rectangle(
    [MARGIN, MARGIN, WIDTH - MARGIN, HEIGHT - MARGIN],
    outline=GOLD, width=8
)

# --------------------------------------------------------------------------
# 5. CONTENU
# --------------------------------------------------------------------------
y = MARGIN + 150

# En-tête
y = center_text(draw, "CÉRÉMONIE DE VEILLÉE", y, SUBTITLE_FONT, GOLD)
y += 60
y = center_text(draw, "En hommage à notre père", y, BODY_FONT)
y += 40

# Nom + dates
y = center_text(draw, "FOTIE JEAN CLAUDE", y, TITLE_FONT)
y += 40
y = center_text(draw, "vers 1946 – 21 mai 2025", y, SUBTITLE_FONT, GOLD)

y += 100

# Zone photo
PHOTO_W, PHOTO_H = 900, 1200
photo_x = (WIDTH - PHOTO_W) // 2
draw.rectangle(
    [photo_x, y, photo_x + PHOTO_W, y + PHOTO_H],
    outline=GOLD, width=6
)
center_text(draw, "PHOTO ICI", y + PHOTO_H / 2 - 40, SUBTITLE_FONT, GOLD)
y += PHOTO_H + 100

# Détails pratiques
y = center_text(draw, "Date : [Jour • Date • Heure]", y, BODY_FONT)
y += 20
y = center_text(draw, "Lieu : Kreuzstraße 1, 67227 Frankenthal (Allemagne)", y, BODY_FONT)

y += 100

# Participants
center_text(draw, "Veillée réservée à ses enfants :", y, BODY_FONT, GOLD)
y += 70
center_text(draw, "Jacques • Mireille • Christelle • Anny • Flore", y, BODY_FONT)

y += 150

# Programme
draw.line([(MARGIN + 200, y), (WIDTH - MARGIN - 200, y)], fill=GOLD, width=4)
y += 40
center_text(draw, "Déroulement prévisionnel", y, SUBTITLE_FONT, GOLD)
y += 80

for item in [
    "Accueil & temps de recueillement",
    "Partage de souvenirs et lectures",
    "Prière / moment de silence",
    "Collation conviviale"
]:
    y = center_text(draw, f"– {item}", y, BODY_FONT)

# Footer
FOOTER = (
    "Merci de respecter cette intimité familiale "
    "et de venir dans une tenue sobre."
)
draw.text(
    (MARGIN + 100, HEIGHT - MARGIN - 150),
    FOOTER,
    font=BODY_FONT,
    fill=(0, 0, 0)
)

# --------------------------------------------------------------------------
# 6. ENREGISTREMENT
# --------------------------------------------------------------------------
os.makedirs(OUTPUT_DIR, exist_ok=True)
file_path = os.path.join(OUTPUT_DIR, FILENAME)
img.save(file_path)
print("✅ Invitation générée :", os.path.abspath(file_path))
