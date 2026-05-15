"""
TESTES UNITÁRIOS PARA O ALGORITMO DE ANÁLISE DE LUZ
"""

import unittest
import numpy as np
from leitura_de_luz import AnalisadorLuzSatelite, EstatisticasImagem


class TestAnalisadorLuzSatelite(unittest.TestCase):
    """Testes para a classe AnalisadorLuzSatelite"""
    
    def setUp(self):
        """Preparar para cada teste"""
        self.analisador = AnalisadorLuzSatelite(metodo_outlier='iqr', limiar_iqr=3.0)
    
    # ========== TESTES DE DIMENSÃO ==========
    
    def test_validar_dimensoes_corretas(self):
        """Deve aceitar imagem 500x500"""
        imagem = np.zeros((500, 500))
        self.assertTrue(self.analisador.validar_dimensoes(imagem))
    
    def test_validar_dimensoes_incorretas(self):
        """Deve rejeitar imagem com dimensões diferentes"""
        imagem = np.zeros((512, 512))
        self.assertFalse(self.analisador.validar_dimensoes(imagem))
    
    def test_validar_dimensoes_pequena(self):
        """Deve rejeitar imagem pequena"""
        imagem = np.zeros((100, 100))
        self.assertFalse(self.analisador.validar_dimensoes(imagem))
    
    # ========== TESTES DE DETECÇÃO DE NULOS ==========
    
    def test_detectar_pixels_nulos_zeros(self):
        """Deve detectar pixels com valor zero"""
        imagem = np.array([[0, 1], [2, 0]], dtype=float)
        mascara = self.analisador.detectar_pixels_nulos(imagem)
        
        esperado = np.array([[True, False], [False, True]])
        np.testing.assert_array_equal(mascara, esperado)
    
    def test_detectar_pixels_nulos_nan(self):
        """Deve detectar pixels com NaN"""
        imagem = np.array([[np.nan, 1], [2, 3]], dtype=float)
        mascara = self.analisador.detectar_pixels_nulos(imagem)
        
        self.assertTrue(mascara[0, 0])
        self.assertFalse(mascara[0, 1])
    
    def test_detectar_pixels_nulos_nenhum(self):
        """Deve não detectar nulos quando não existem"""
        imagem = np.ones((500, 500))
        mascara = self.analisador.detectar_pixels_nulos(imagem)
        
        self.assertEqual(np.sum(mascara), 0)
    
    # ========== TESTES DE DETECÇÃO DE OUTLIERS ==========
    
    def test_calcular_threshold_iqr(self):
        """Deve calcular threshold corretamente com IQR"""
        imagem = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float).reshape(5, 2)
        mascara_nula = np.zeros((5, 2), dtype=bool)
        
        threshold = self.analisador.calcular_threshold_outlier(imagem, mascara_nula)
        
        # Com IQR, threshold deve estar acima do valor máximo
        self.assertGreater(threshold, 10)
    
    def test_detectar_outliers(self):
        """Deve detectar valores acima do threshold"""
        imagem = np.array([[1, 2], [3, 100]], dtype=float)
        mascara = self.analisador.detectar_outliers(imagem, threshold=50)
        
        esperado = np.array([[False, False], [False, True]])
        np.testing.assert_array_equal(mascara, esperado)
    
    # ========== TESTES DE VALIDAÇÃO COMPLETA ==========
    
    def test_validar_pixels_imagem_perfeita(self):
        """Deve validar imagem sem erros"""
        imagem = np.full((500, 500), 100.0)
        mascara_valida, metricas = self.analisador.validar_pixels(imagem)
        
        # Todos os pixels devem ser válidos
        self.assertEqual(metricas['pixels_nulos'], 0)
        self.assertEqual(metricas['pixels_outliers'], 0)
        self.assertEqual(np.sum(mascara_valida), 250000)
    
    def test_validar_pixels_com_nulos(self):
        """Deve identificar pixels nulos"""
        imagem = np.full((500, 500), 100.0)
        imagem[0:10, 0:10] = 0  # 100 pixels nulos
        
        mascara_valida, metricas = self.analisador.validar_pixels(imagem)
        
        self.assertEqual(metricas['pixels_nulos'], 100)
    
    # ========== TESTES DE PROCESSAMENTO ==========
    
    def test_processar_imagem_valida(self):
        """Deve processar imagem válida sem erros"""
        imagem = np.random.normal(100, 20, (500, 500))
        imagem = np.clip(imagem, 1, 255)
        
        stats = self.analisador.processar_imagem(imagem)
        
        self.assertIsInstance(stats, EstatisticasImagem)
        self.assertEqual(stats.total_pixels, 250000)
        self.assertGreater(stats.percentual_valido, 0)
    
    def test_processar_imagem_dimensao_invalida(self):
        """Deve lançar erro para dimensão incorreta"""
        imagem = np.zeros((256, 256))
        
        with self.assertRaises(ValueError):
            self.analisador.processar_imagem(imagem)
    
    def test_processar_sequencia_multiplas_imagens(self):
        """Deve processar múltiplas imagens"""
        imagens = [
            np.random.normal(100, 20, (500, 500)) for _ in range(3)
        ]
        imagens = [np.clip(img, 1, 255) for img in imagens]
        
        resultados = self.analisador.processar_sequencia(imagens)
        
        self.assertEqual(len(resultados), 3)
        for stats in resultados:
            self.assertIsInstance(stats, EstatisticasImagem)
    
    # ========== TESTES DE ESTATÍSTICAS ==========
    
    def test_calculo_media(self):
        """Deve calcular média corretamente"""
        imagem = np.full((500, 500), 50.0)
        stats = self.analisador.processar_imagem(imagem)
        
        self.assertAlmostEqual(stats.intensidade_media, 50.0, places=1)
    
    def test_calculo_mediana(self):
        """Deve calcular mediana corretamente"""
        # Distribuição uniforme
        imagem = np.random.uniform(50, 150, (500, 500))
        stats = self.analisador.processar_imagem(imagem)
        
        # Mediana deve estar entre 50 e 150
        self.assertGreater(stats.intensidade_mediana, 50)
        self.assertLess(stats.intensidade_mediana, 150)
    
    def test_calculo_desvio_padrao(self):
        """Deve calcular desvio padrão"""
        imagem = np.random.normal(100, 30, (500, 500))
        imagem = np.clip(imagem, 1, 255)
        
        stats = self.analisador.processar_imagem(imagem)
        
        self.assertGreater(stats.desvio_padrao, 0)
    
    # ========== TESTES DE MÉTODOS ==========
    
    def test_metodo_iqr(self):
        """Deve funcionar com método IQR"""
        analisador = AnalisadorLuzSatelite(metodo_outlier='iqr', limiar_iqr=2.0)
        imagem = np.random.normal(100, 20, (500, 500))
        imagem = np.clip(imagem, 1, 255)
        
        stats = analisador.processar_imagem(imagem)
        self.assertGreater(stats.percentual_valido, 0)
    
    def test_metodo_zscore(self):
        """Deve funcionar com método Z-Score"""
        analisador = AnalisadorLuzSatelite(metodo_outlier='zscore', limiar_zscore=2.5)
        imagem = np.random.normal(100, 20, (500, 500))
        imagem = np.clip(imagem, 1, 255)
        
        stats = analisador.processar_imagem(imagem)
        self.assertGreater(stats.percentual_valido, 0)
    
    # ========== TESTES DE CASOS EXTREMOS ==========
    
    def test_imagem_todos_nulos(self):
        """Deve lidar com imagem totalmente nula"""
        imagem = np.zeros((500, 500))
        stats = self.analisador.processar_imagem(imagem)
        
        self.assertEqual(stats.pixels_validos, 0)
        self.assertEqual(stats.pixels_nulos, 250000)
    
    def test_imagem_todos_outliers(self):
        """Deve lidar com imagem de todos outliers"""
        imagem = np.full((500, 500), 1.0)
        # Adicionar alguns pixels normais para calcular threshold
        imagem[0:100, 0:100] = 50
        
        # Resto são outliers (muito baixos comparado aos 50)
        stats = self.analisador.processar_imagem(imagem)
        
        # Deve ter detectado muitos outliers
        self.assertGreater(stats.pixels_outliers, 0)
    
    def test_imagem_com_nan_e_zeros(self):
        """Deve lidar com mistura de NaN e zeros"""
        imagem = np.random.normal(100, 20, (500, 500))
        imagem[0:100, 0] = 0  # zeros
        imagem[100:200, 0] = np.nan  # NaN
        imagem = np.clip(imagem, 1, 255)
        
        stats = self.analisador.processar_imagem(imagem)
        
        self.assertGreater(stats.pixels_nulos, 0)
        self.assertLess(stats.percentual_valido, 100)
    
    # ========== TESTES DE RELATÓRIO ==========
    
    def test_gerar_relatorio_formato(self):
        """Deve gerar relatorio com formato correto"""
        imagem = np.random.normal(100, 20, (500, 500))
        imagem = np.clip(imagem, 1, 255)
        
        stats = self.analisador.processar_imagem(imagem)
        relatorio = self.analisador.gerar_relatorio(stats)
        
        # Verificar que relatorio contem informacoes esperadas
        self.assertIn("RELAT", relatorio)  # Parte de RELATÓRIO
        self.assertIn("Pixels validos", relatorio.replace("á", "a"))
        self.assertIn("Media", relatorio.replace("é", "e"))
        self.assertIn("Status geral", relatorio)
    
    def test_relatorio_qualidade_aceita(self):
        """Relatório deve indicar ACEITA para qualidade > 90%"""
        imagem = np.full((500, 500), 100.0)
        stats = self.analisador.processar_imagem(imagem)
        relatorio = self.analisador.gerar_relatorio(stats)
        
        self.assertIn("ACEITA", relatorio)
    
    # ========== TESTES DE LIMITES ==========
    
    def test_limiar_iqr_afeta_deteccao(self):
        """Limiar maior deve detectar menos outliers"""
        imagem = np.random.normal(100, 30, (500, 500))
        imagem = np.clip(imagem, 1, 255)
        
        # IQR com limiar alto
        analisador_alto = AnalisadorLuzSatelite(metodo_outlier='iqr', limiar_iqr=5.0)
        stats_alto = analisador_alto.processar_imagem(imagem)
        
        # IQR com limiar baixo
        analisador_baixo = AnalisadorLuzSatelite(metodo_outlier='iqr', limiar_iqr=1.0)
        stats_baixo = analisador_baixo.processar_imagem(imagem)
        
        # Limiar baixo deve detectar mais outliers
        self.assertGreater(stats_baixo.pixels_outliers, stats_alto.pixels_outliers)


class TestEstatisticasImagem(unittest.TestCase):
    """Testes para a dataclass EstatisticasImagem"""
    
    def test_criar_estatisticas(self):
        """Deve criar EstatisticasImagem corretamente"""
        stats = EstatisticasImagem(
            total_pixels=250000,
            pixels_validos=240000,
            pixels_nulos=10000,
            pixels_outliers=0,
            percentual_valido=96.0,
            intensidade_media=100.5,
            intensidade_mediana=100.0,
            intensidade_minima=10.0,
            intensidade_maxima=200.0,
            desvio_padrao=25.0,
            threshold_outlier=150.0
        )
        
        self.assertEqual(stats.pixels_validos, 240000)
        self.assertAlmostEqual(stats.percentual_valido, 96.0)


# ============================================================================
# RUNNER
# ============================================================================

if __name__ == '__main__':
    # Configurar teste com mais verbosidade
    unittest.main(verbosity=2)
