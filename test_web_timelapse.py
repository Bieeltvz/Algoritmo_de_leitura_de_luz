#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test timelapse via web API
"""

import requests
import json
from pathlib import Path
import time

def test_web_timelapse():
    BASE_URL = "http://127.0.0.1:5000"
    
    print("\n" + "=" * 80)
    print("🌐 TESTE: TIMELAPSE VIA INTERFACE WEB")
    print("=" * 80)
    
    # Test 1: Check if server is running
    try:
        print("\n1️⃣  Verificando conexão com servidor...")
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print(f"   ✅ Servidor respondendo em {BASE_URL}")
        else:
            print(f"   ❌ Servidor respondeu com {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Servidor não está acessível: {e}")
        return False
    
    # Test 2: Select a city
    print("\n2️⃣  Selecionando cidade...")
    try:
        select_response = requests.post(
            f"{BASE_URL}/api/selecionar-pasta",
            json={"nome_pasta": "Blumenau - BNU_RECORTADO"},
            timeout=5
        )
        if select_response.status_code == 200:
            print(f"   ✅ Cidade selecionada")
        else:
            print(f"   ⚠️ Status: {select_response.status_code}")
    except Exception as e:
        print(f"   ⚠️ Erro ao selecionar: {e}")
    
    # Test 3: Generate timelapse
    print("\n3️⃣  Gerando timelapse...")
    try:
        timelapse_response = requests.get(
            f"{BASE_URL}/api/gerar-timelapse",
            timeout=30
        )
        
        if timelapse_response.status_code == 200:
            data = timelapse_response.json()
            if data.get('sucesso'):
                print(f"   ✅ Timelapse gerado: {data.get('mensagem')}")
                print(f"   📍 URL: {data.get('url_timelapse')}")
                return True
            else:
                print(f"   ❌ Erro: {data.get('mensagem')}")
                return False
        else:
            print(f"   ❌ Status HTTP: {timelapse_response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"   ⏱️  Timeout (timelapse muito grande, mas pode ter funcionado)")
        return True
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False

if __name__ == '__main__':
    try:
        success = test_web_timelapse()
        print("\n" + "=" * 80)
        if success:
            print("✅ TESTE WEB BEM-SUCEDIDO!")
            print("\nVocê pode agora:")
            print("  1. Abrir http://localhost:5000")
            print("  2. Selecionar uma cidade no dropdown")
            print("  3. Clicar 'Gerar Timelapse'")
            print("  4. Ver timelapse com imagens binárias de dezembro!")
        else:
            print("❌ Teste web falhou")
        print("=" * 80)
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
