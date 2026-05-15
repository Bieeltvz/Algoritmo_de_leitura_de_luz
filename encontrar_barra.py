#!/usr/bin/env python3
import os
from pathlib import Path

# Procurar pasta Barra Velha
docs = Path.home() / "Documents"
print("Procurando pasta Barra Velha...")

for folder in docs.glob("*Barra*"):
    print(f"\nEncontrado: {folder}")
    
    # Procurar subpastas Raster
    for raster_folder in folder.glob("*/Raster/*"):
        tiff_files = list(raster_folder.glob("*.tif")) + list(raster_folder.glob("*.tiff"))
        print(f"  {raster_folder.name}: {len(tiff_files)} arquivos TIFF")
        if tiff_files[:3]:
            for f in tiff_files[:3]:
                print(f"    - {f.name}")
