#!/usr/bin/env python3
"""
Demonstração: Criar timelapse sintético com algoritmo corrigido
Simula 10 anos de dados (2014-2024) com crescimento progressivo
"""

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
import base64
from pathlib import Path
from mapa_crescimento import MapaCrescimento

m = MapaCrescimento()

print("=== Gerando timelapse demonstrativo ===\n")

# Simular 10 imagens (2014, 2015, ..., 2023, 2024)
anos = list(range(2014, 2025))
imagens = []

# Criar progressão temporal realista
for i, ano in enumerate(anos):
    # Imagem base com ruído
    np.random.seed(42 + ano)
    img = np.ones((256, 256), dtype=np.float32) * (50 + i * 2)
    img += np.random.normal(0, 1, (256, 256))
    
    # Adicionar crescimento em área urbana (100x100 pixels)
    crescimento = (ano - 2014) / 10.0 * 30  # 0 a 30 de crescimento em 10 anos
    img[50:150, 50:150] += crescimento + np.random.normal(0, 0.5, (100, 100))
    
    imagens.append(img)
    print(f"{ano}: valor médio = {img.mean():.1f}")

print()

# Calcular mapa de crescimento (2014 vs 2024)
mapa_crescimento = m._calcular_mapa_crescimento(imagens[0], imagens[-1])

if mapa_crescimento is not None:
    pixels_0 = np.sum(mapa_crescimento == 0)
    pixels_1 = np.sum(mapa_crescimento == 1)
    pixels_2 = np.sum(mapa_crescimento == 2)
    total = mapa_crescimento.size
    
    print(f"Mapa de crescimento (2014-2024):")
    print(f"  Sem mudança: {pixels_0} ({pixels_0/total*100:.1f}%)")
    print(f"  Amarelo:     {pixels_1} ({pixels_1/total*100:.1f}%)")
    print(f"  Vermelho:    {pixels_2} ({pixels_2/total*100:.1f}%)")
    print()

# Criar HTML com timelapse
html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Timelapse de Crescimento (Algoritmo Corrigido)</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        .container {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 1000px;
            width: 90%;
        }
        
        h1 {
            text-align: center;
            color: #333;
            margin: 0 0 10px 0;
        }
        
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 20px;
            font-size: 14px;
        }
        
        .imagem-container {
            display: flex;
            justify-content: center;
            align-items: center;
            background: #f5f5f5;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            width: 100%;
            height: 600px;
        }
        
        .imagem-container img {
            width: 95%;
            height: 95%;
            object-fit: contain;
            display: block;
            image-rendering: high-quality;
            filter: contrast(1.2);
        }
        
        .controles {
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }
        
        button {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            transition: background 0.3s;
        }
        
        button:hover {
            background: #764ba2;
        }
        
        button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        
        .slider-container {
            display: flex;
            gap: 10px;
            align-items: center;
        }
        
        input[type="range"] {
            flex: 1;
            height: 8px;
            border-radius: 5px;
            background: #ddd;
            outline: none;
            -webkit-appearance: none;
        }
        
        input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: #667eea;
            cursor: pointer;
        }
        
        input[type="range"]::-moz-range-thumb {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: #667eea;
            cursor: pointer;
            border: none;
        }
        
        .info {
            background: #f0f0f0;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-size: 14px;
            color: #333;
        }
        
        .frame-info {
            font-weight: bold;
            font-size: 16px;
            margin-bottom: 10px;
        }
        
        .legend {
            display: flex;
            gap: 20px;
            justify-content: center;
            flex-wrap: wrap;
            margin-top: 15px;
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 13px;
        }
        
        .legend-color {
            width: 20px;
            height: 20px;
            border-radius: 3px;
        }
        
        .loading {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.5);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="loading" id="loading">
        <div class="spinner"></div>
    </div>
    
    <div class="container">
        <h1>🛰️ Timelapse de Crescimento Urbano</h1>
        <p class="subtitle">Visualização do crescimento de luz noturna (2014-2024) com algoritmo corrigido</p>
        
        <div class="imagem-container">
            <img id="timelapse-image" src="" alt="Timelapse">
        </div>
        
        <div class="controles">
            <button id="btn-play">▶️ Play</button>
            <button id="btn-pause">⏸️ Pause</button>
            <button id="btn-first">⏮️ Início</button>
            <button id="btn-last">⏭️ Fim</button>
        </div>
        
        <div class="slider-container">
            <span style="font-size: 12px; color: #666;">2014</span>
            <input type="range" id="slider-frames" min="0" max="9" value="0" step="1">
            <span style="font-size: 12px; color: #666;">2024</span>
        </div>
        
        <div class="info">
            <div class="frame-info" id="frame-info">Ano: 2014 (Quadro 1 de 10)</div>
            <p style="margin: 5px 0; font-size: 13px;">
                Este timelapse simula o crescimento de iluminação noturna ao longo de 10 anos.
                Use os controles para navegar entre os quadros.
            </p>
            <div class="legend">
                <div class="legend-item">
                    <div class="legend-color" style="background: #FFD700;"></div>
                    <span>Crescimento moderado</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #FF4444;"></div>
                    <span>Crescimento forte</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #999;"></div>
                    <span>Sem crescimento</span>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        const data = {
            anos: [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
            imagens: [IMAGENS_AQUI]
        };
        
        let indice_atual = 0;
        let tocando = false;
        const intervalo = 500; // ms entre frames
        let timer = null;
        
        function atualizar_frame(indice) {
            indice_atual = indice;
            const img = data.imagens[indice];
            document.getElementById('timelapse-image').src = 'data:image/png;base64,' + img;
            
            const ano = data.anos[indice];
            const total = data.imagens.length;
            document.getElementById('frame-info').innerText = `Ano: ${ano} (Quadro ${indice + 1} de ${total})`;
            document.getElementById('slider-frames').value = indice;
        }
        
        function play() {
            if (tocando) return;
            tocando = true;
            timer = setInterval(() => {
                indice_atual++;
                if (indice_atual >= data.imagens.length) {
                    indice_atual = 0;
                }
                atualizar_frame(indice_atual);
            }, intervalo);
        }
        
        function pause() {
            tocando = false;
            if (timer) clearInterval(timer);
        }
        
        document.getElementById('btn-play').onclick = play;
        document.getElementById('btn-pause').onclick = pause;
        document.getElementById('btn-first').onclick = () => atualizar_frame(0);
        document.getElementById('btn-last').onclick = () => atualizar_frame(data.imagens.length - 1);
        document.getElementById('slider-frames').onchange = (e) => atualizar_frame(parseInt(e.target.value));
        
        // Inicializar
        atualizar_frame(0);
    </script>
</body>
</html>
"""

# Converter cada imagem para PNG base64
print("Convertendo imagens para base64...")
imagens_base64 = []

for i, img_array in enumerate(imagens):
    # Normalizar e aplicar overlay
    img_cinza = np.clip(img_array, 0, 255).astype(np.uint8)
    
    # Se for a primeira ou última, não aplicar overlay
    if i == 0 or i == len(imagens) - 1:
        mapa = m._calcular_mapa_crescimento(imagens[0], imagens[i])
    else:
        # Progressivamente mostrar crescimento
        mapa = m._calcular_mapa_crescimento(imagens[0], imagens[i])
    
    if mapa is not None:
        resultado = m._aplicar_overlay_crescimento(img_cinza, mapa)
    else:
        resultado = np.stack([img_cinza] * 3, axis=2)
    
    # Converter para PIL
    img_pil = Image.fromarray(resultado.astype(np.uint8), mode='RGB')
    img_pil = img_pil.resize((900, 900))
    
    # Para base64
    from io import BytesIO
    buffer = BytesIO()
    img_pil.save(buffer, format='PNG')
    img_base64 = base64.b64encode(buffer.getvalue()).decode()
    imagens_base64.append(img_base64)
    print(f"  {i+1}/{len(imagens)} - {anos[i]}")

# Inserir as imagens no HTML
imagens_json = ',\n        '.join([f'"{img}"' for img in imagens_base64])
html_content = html_content.replace('IMAGENS_AQUI', imagens_json)

# Salvar arquivo
output_file = 'timelapse_demo_corrigido.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"\n✅ Timelapse gerado: {output_file}")
print(f"   Tamanho: {len(html_content) / (1024*1024):.1f} MB")
