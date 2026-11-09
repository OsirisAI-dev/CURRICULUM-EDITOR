"""
Moteur d'icônes vectorisées modernes et anti-aliasées pour l'Éditeur de CV.
Dessine des glyphes ultra-nets avec PIL (supersampling 4x + LANCZOS)
et les convertit en CTkImage compatibles thèmes clair et sombre.
"""
from __future__ import annotations

from typing import Dict, Tuple
from PIL import Image, ImageDraw
import customtkinter as ctk


def _draw_cv_icon(name: str, color_hex: str, size: int = 24) -> Image.Image:
    scale = 4
    dim = size * scale
    img = Image.new("RGBA", (dim, dim), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    s = scale
    st = max(int(1.8 * s), 2)  # Épaisseur du trait

    if name in ("user", "profile"):
        # Silhouette humaine
        cx = 12 * s
        # Tête
        d.ellipse([cx - 4*s, 3*s, cx + 4*s, 11*s], outline=color_hex, width=st)
        # Buste
        d.arc([3*s, 12*s, 21*s, 24*s], start=180, end=360, fill=color_hex, width=st)
        d.line([3*s, 18*s, 3*s, 22*s], fill=color_hex, width=st)
        d.line([21*s, 18*s, 21*s, 22*s], fill=color_hex, width=st)

    elif name in ("briefcase", "experience"):
        # Mallette professionnelle
        x0, y0, x1, y1 = 3*s, 7*s, 21*s, 20*s
        d.rounded_rectangle([x0, y0, x1, y1], radius=2*s, outline=color_hex, width=st)
        # Poignée
        d.line([8*s, 7*s, 8*s, 4*s], fill=color_hex, width=st)
        d.line([8*s, 4*s, 16*s, 4*s], fill=color_hex, width=st)
        d.line([16*s, 4*s, 16*s, 7*s], fill=color_hex, width=st)
        # Ligne médiane
        d.line([x0, 13*s, x1, 13*s], fill=color_hex, width=st)
        # Serrure
        d.rectangle([11*s, 12*s, 13*s, 15*s], fill=color_hex)

    elif name in ("graduation", "education"):
        # Toque d'étudiant
        pts = [(12*s, 4*s), (22*s, 9*s), (12*s, 14*s), (2*s, 9*s)]
        d.polygon(pts, outline=color_hex)
        d.line([(12*s, 4*s), (22*s, 9*s)], fill=color_hex, width=st)
        d.line([(22*s, 9*s), (12*s, 14*s)], fill=color_hex, width=st)
        d.line([(12*s, 14*s), (2*s, 9*s)], fill=color_hex, width=st)
        d.line([(2*s, 9*s), (12*s, 4*s)], fill=color_hex, width=st)
        # Base inférieure
        d.arc([6*s, 11*s, 18*s, 19*s], start=0, end=180, fill=color_hex, width=st)
        # Gland / Cordon
        d.line([20*s, 10*s, 20*s, 18*s], fill=color_hex, width=st)
        d.ellipse([19*s, 18*s, 21*s, 20*s], fill=color_hex)

    elif name in ("certificate", "award"):
        # Diplôme / Badge
        cx, cy, r = 12*s, 10*s, 6*s
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color_hex, width=st)
        # Rubans descendants
        d.line([9*s, 15*s, 7*s, 22*s], fill=color_hex, width=st)
        d.line([7*s, 22*s, 10*s, 20*s], fill=color_hex, width=st)
        d.line([10*s, 20*s, 12*s, 16*s], fill=color_hex, width=st)
        d.line([15*s, 15*s, 17*s, 22*s], fill=color_hex, width=st)
        d.line([17*s, 22*s, 14*s, 20*s], fill=color_hex, width=st)
        d.line([14*s, 20*s, 12*s, 16*s], fill=color_hex, width=st)

    elif name in ("skill", "zap"):
        # Éclair de compétence
        pts = [
            (13*s, 2*s), (6*s, 13*s), (12*s, 13*s),
            (10*s, 22*s), (18*s, 10*s), (12*s, 10*s)
        ]
        d.polygon(pts, fill=color_hex)

    elif name in ("globe", "language"):
        # Globe terrestre
        cx, cy, r = 12*s, 12*s, 9*s
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color_hex, width=st)
        d.line([cx - r, cy, cx + r, cy], fill=color_hex, width=st)
        d.ellipse([cx - 4*s, cy - r, cx + 4*s, cy + r], outline=color_hex, width=st)

    elif name in ("heart", "hobby"):
        # Cœur
        d.ellipse([4*s, 4*s, 12*s, 12*s], fill=color_hex)
        d.ellipse([12*s, 4*s, 20*s, 12*s], fill=color_hex)
        pts = [(4*s, 9*s), (20*s, 9*s), (12*s, 21*s)]
        d.polygon(pts, fill=color_hex)

    elif name in ("pen", "signature"):
        # Stylo plume / signature
        d.line([18*s, 4*s, 20*s, 6*s], fill=color_hex, width=st)
        d.line([6*s, 16*s, 18*s, 4*s], fill=color_hex, width=st)
        d.line([8*s, 18*s, 20*s, 6*s], fill=color_hex, width=st)
        d.polygon([(4*s, 20*s), (8*s, 18*s), (6*s, 16*s)], fill=color_hex)
        # Ligne de signature
        d.line([3*s, 22*s, 21*s, 22*s], fill=color_hex, width=st)

    elif name in ("palette", "style"):
        # Palette de peintre
        cx, cy, r = 12*s, 12*s, 9*s
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color_hex, width=st)
        d.ellipse([13*s, 13*s, 16*s, 16*s], fill=color_hex)  # Trou pouce
        d.ellipse([8*s, 7*s, 10*s, 9*s], fill=color_hex)
        d.ellipse([13*s, 6*s, 15*s, 8*s], fill=color_hex)
        d.ellipse([7*s, 12*s, 9*s, 14*s], fill=color_hex)

    elif name in ("download", "export"):
        # Flèche vers le bas dans un bac
        cx = 12 * s
        d.line([cx, 4*s, cx, 15*s], fill=color_hex, width=st)
        d.line([cx - 4*s, 11*s, cx, 15*s], fill=color_hex, width=st)
        d.line([cx + 4*s, 11*s, cx, 15*s], fill=color_hex, width=st)
        d.line([4*s, 15*s, 4*s, 20*s], fill=color_hex, width=st)
        d.line([4*s, 20*s, 20*s, 20*s], fill=color_hex, width=st)
        d.line([20*s, 20*s, 20*s, 15*s], fill=color_hex, width=st)

    elif name in ("eye", "preview"):
        # Œil
        d.arc([2*s, 5*s, 22*s, 19*s], start=195, end=345, fill=color_hex, width=st)
        d.arc([2*s, 5*s, 22*s, 19*s], start=15, end=165, fill=color_hex, width=st)
        d.ellipse([10*s, 10*s, 14*s, 14*s], fill=color_hex)

    elif name == "plus":
        # Plus épais
        d.line([4*s, 12*s, 20*s, 12*s], fill=color_hex, width=st + s)
        d.line([12*s, 4*s, 12*s, 20*s], fill=color_hex, width=st + s)

    elif name == "trash":
        # Poubelle
        d.line([4*s, 6*s, 20*s, 6*s], fill=color_hex, width=st)
        d.line([9*s, 4*s, 15*s, 4*s], fill=color_hex, width=st)
        d.line([6*s, 6*s, 7*s, 20*s], fill=color_hex, width=st)
        d.line([7*s, 20*s, 17*s, 20*s], fill=color_hex, width=st)
        d.line([17*s, 20*s, 18*s, 6*s], fill=color_hex, width=st)
        d.line([10*s, 9*s, 10*s, 17*s], fill=color_hex, width=st)
        d.line([14*s, 9*s, 14*s, 17*s], fill=color_hex, width=st)

    elif name == "save":
        # Disquette
        x0, y0, x1, y1 = 4*s, 3*s, 20*s, 21*s
        d.rounded_rectangle([x0, y0, x1, y1], radius=2*s, outline=color_hex, width=st)
        d.rectangle([x0 + 3*s, y0, x1 - 3*s, y0 + 6*s], fill=color_hex)
        d.rectangle([x0 + 3*s, y1 - 8*s, x1 - 3*s, y1], outline=color_hex, width=st)

    elif name == "sparkles":
        # Étoile
        cx, cy = 12*s, 12*s
        pts = [
            (cx, cy - 8*s), (cx + 2*s, cy - 2*s),
            (cx + 8*s, cy), (cx + 2*s, cy + 2*s),
            (cx, cy + 8*s), (cx - 2*s, cy + 2*s),
            (cx - 8*s, cy), (cx - 2*s, cy - 2*s)
        ]
        d.polygon(pts, fill=color_hex)

    elif name == "theme":
        # Demi-lune
        cx, cy, r = 12*s, 12*s, 8*s
        d.arc([cx - r, cy - r, cx + r, cy + r], start=60, end=300, fill=color_hex, width=st)
        d.arc([cx - 4*s, cy - r, cx + r, cy + r], start=60, end=300, fill=color_hex, width=st)

    elif name == "doc_pdf":
        # Document avec badge P
        x0, y0, x1, y1 = 4*s, 2*s, 20*s, 22*s
        d.rounded_rectangle([x0, y0, x1, y1], radius=2*s, outline=color_hex, width=st)
        d.rectangle([6*s, 7*s, 18*s, 17*s], fill=color_hex)

    elif name == "doc_word":
        # Document avec lignes W
        x0, y0, x1, y1 = 4*s, 2*s, 20*s, 22*s
        d.rounded_rectangle([x0, y0, x1, y1], radius=2*s, outline=color_hex, width=st)
        d.line([7*s, 8*s, 9*s, 16*s], fill=color_hex, width=st)
        d.line([9*s, 16*s, 11*s, 10*s], fill=color_hex, width=st)
        d.line([11*s, 10*s, 13*s, 16*s], fill=color_hex, width=st)
        d.line([13*s, 16*s, 15*s, 8*s], fill=color_hex, width=st)

    elif name == "folder_open":
        # Dossier ouvert
        x0, y0, x1, y1 = 2*s, 5*s, 22*s, 20*s
        d.rounded_rectangle([x0, y0 + 2*s, x1 - 3*s, y1 - 2*s], radius=2*s, outline=color_hex, width=st)
        d.line([(x0 + 2*s, y1), (x1, y1)], fill=color_hex, width=st)

    elif name == "refresh":
        # Flèche circulaire
        cx, cy, r = 12*s, 12*s, 7*s
        d.arc([cx - r, cy - r, cx + r, cy + r], start=45, end=330, fill=color_hex, width=st)
        px, py = cx + r - s, cy
        d.polygon([(px - 2*s, py - 3*s), (px + 3*s, py), (px - 2*s, py + 3*s)], fill=color_hex)

    else:
        # Cercle par défaut
        d.ellipse([4*s, 4*s, 20*s, 20*s], outline=color_hex, width=st)

    return img.resize((size, size), Image.Resampling.LANCZOS)


class CVIcons:
    """Gestionnaire de cache pour icônes CustomTkinter."""

    def __init__(self):
        self._cache: Dict[Tuple[str, int, str, str], ctk.CTkImage] = {}

    def get_icon(
        self,
        name: str,
        size: int = 18,
        light_color: str = "#1e3a8a",
        dark_color: str = "#60a5fa"
    ) -> ctk.CTkImage:
        key = (name, size, light_color, dark_color)
        if key in self._cache:
            return self._cache[key]

        img_l = _draw_cv_icon(name, light_color, size=size)
        img_d = _draw_cv_icon(name, dark_color, size=size)

        ci = ctk.CTkImage(light_image=img_l, dark_image=img_d, size=(size, size))
        self._cache[key] = ci
        return ci

    def get_white_icon(self, name: str, size: int = 18) -> ctk.CTkImage:
        return self.get_icon(name, size=size, light_color="#ffffff", dark_color="#ffffff")


_cv_icons_singleton = None


def get_cv_icons() -> CVIcons:
    global _cv_icons_singleton
    if _cv_icons_singleton is None:
        _cv_icons_singleton = CVIcons()
    return _cv_icons_singleton
