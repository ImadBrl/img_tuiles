import rasterio
from rasterio.windows import Window
import numpy as np
from pathlib import Path
from tqdm import tqdm
import json

def tile_image_with_coords(image_path, tile_size=640, output_dir="tiles"):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    coords_dir = output_dir / "coords"
    coords_dir.mkdir(exist_ok=True)

    with rasterio.open(image_path) as src:
        width, height = src.width, src.height
        count = src.count  # Doit être 4 si la bande des coordonnées est incluse

        stride = tile_size // 2  # Chevauchement de 50%

        # Parcours de l'image avec glissement de 50% du tile_size
        for y in tqdm(range(0, height - tile_size + 1, stride)):
            for x in range(0, width - tile_size + 1, stride):
                window = Window(x, y, tile_size, tile_size)

                # Lire les 3 bandes RGB
                rgb = src.read([1, 2, 3], window=window)

                # Lire la bande 4 contenant les coordonnées (si elle existe)
                # if count >= 4:
                #     coords_band = src.read(4, window=window)

                # Sauvegarde de l’image RGB
                tile_id = f"{y}_{x}"
                rgb_path = output_dir / f"tile_{tile_id}.tif"

                profile = src.profile.copy()
                profile.update({
                    "count": 3,
                    "height": tile_size,
                    "width": tile_size,
                    "transform": rasterio.windows.transform(window, src.transform),
                    "driver": "GTiff"
                })

                with rasterio.open(rgb_path, 'w', **profile) as dst:
                    dst.write(rgb)

                # Sauvegarde des coordonnées sous forme numpy (si bande 4)
                # if count >= 4:
                #     np.save(coords_dir / f"tile_{tile_id}.npy", coords_band)


#print(f"Tuiles RGB + matrices de coordonnées enregistrées dans {output_dir}")

# Utilisation
tile_image_with_coords("C:/Users/imad-/Desktop/Sat det/code/test/img.tif", tile_size=640, output_dir="output_til")
