/**
 * @fileoverview Script de Interatividade - Análise de Imagens de Satélite
 * 
 * Sistema web para análise de intensidade de luz em imagens TIFF/GeoTIFF
 * de satélites noturnos. Gerencia o fluxo de upload, processamento e 
 * visualização de resultados através de uma API REST.
 * 
 * @author Sistema de Análise de Luz Noturna
 * @version 2.0
 * @requires Bootstrap 5.3.0
 * @requires Bootstrap Icons 1.11.0
 */

// ============================================================================
// VARIÁVEIS GLOBAIS
// ============================================================================

/**
 * Armazena informações da imagem selecionada
 * @type {Object|null}
 * @property {string} nome - Nome do arquivo
 * @property {string} [tipo] - Tipo de origem ('upload' ou 'lista')
 * @property {string} [caminho] - Caminho completo (para imagens da pasta padrão)
 */
let imagemSelecionada = null;

/**
 * ID do intervalo de atualização de status (para poder parar quando terminar)
 * @type {number|null}
 */
let intervaloAtualizacaoStatus = null;

// ============================================================================
// INICIALIZAÇÃO
// ============================================================================

/**
 * Inicializa a aplicação quando o DOM está pronto
 * Carrega pastas disponíveis e configura listeners
 */
document.addEventListener('DOMContentLoaded', function() {
    // Carrega pastas disponíveis
    carregarPastasDisponiveis();
    // Desabilitado: carregarImagens();
});

// ============================================================================
// GERENCIAMENTO DE PASTAS
// ============================================================================

/**
 * Carrega lista de pastas disponíveis e popula dropdown
 * Descoberta automática de cidades em Documents
 * @returns {Promise<void>}
 */
async function carregarPastasDisponiveis() {
    try {
        const response = await fetch('/api/listar-pastas');
        const dados = await response.json();
        
        if (dados.sucesso) {
            // Atualizar nome da pasta atual na navbar
            const pastaAtualElement = document.getElementById('pasta-atual-nome');
            if (pastaAtualElement) {
                // Mostrar cidade/tipo_recorte em vez de apenas nome técnico
                const pastaAtual = dados.pastas.find(p => p.selecionada);
                if (pastaAtual) {
                    pastaAtualElement.textContent = `${pastaAtual.cidade} - ${pastaAtual.tipo_recorte}`;
                } else {
                    pastaAtualElement.textContent = dados.pasta_atual;
                }
            }
            
            // Preencher dropdown
            const listaPastas = document.getElementById('lista-pastas');
            listaPastas.innerHTML = '';
            
            if (dados.pastas.length === 0) {
                const li = document.createElement('li');
                const a = document.createElement('a');
                a.className = 'dropdown-item';
                a.href = '#';
                a.textContent = 'Nenhuma cidade encontrada em Documents';
                li.appendChild(a);
                listaPastas.appendChild(li);
                return;
            }
            
            dados.pastas.forEach(pasta => {
                const li = document.createElement('li');
                const a = document.createElement('a');
                a.className = 'dropdown-item';
                a.href = '#';
                
                // Mostrar cidade, tipo de recorte e contador de imagens
                a.innerHTML = `
                    <div class="d-flex justify-content-between align-items-center w-100">
                        <div>
                            <strong>${pasta.cidade}</strong><br>
                            <small class="text-muted">${pasta.tipo_recorte}</small>
                        </div>
                        <div class="text-end">
                            <small class="text-muted">${pasta.total_imagens} img</small>
                            ${pasta.selecionada ? '<i class="bi bi-check-lg ms-2"></i>' : ''}
                        </div>
                    </div>
                `;
                
                a.onclick = (e) => {
                    e.preventDefault();
                    selecionarPasta(pasta.nome);
                };
                li.appendChild(a);
                listaPastas.appendChild(li);
            });
        }
    } catch (erro) {
        console.error('Erro ao carregar pastas:', erro);
    }
}

/**
 * Seleciona uma pasta para trabalhar
 * Descobre automaticamente cidades em Documents
 * @param {string} nomePasta - Nome da pasta a selecionar
 * @returns {Promise<void>}
 */
async function selecionarPasta(nomePasta) {
    try {
        const response = await fetch('/api/selecionar-pasta', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ nome_pasta: nomePasta })
        });
        
        const dados = await response.json();
        
        if (dados.sucesso) {
            // Atualizar UI com nome amigável (cidade - tipo recorte)
            document.getElementById('pasta-atual-nome').textContent = 
                `${dados.cidade} - ${dados.total_imagens} img`;
            
            // Limpar tabelas e status da cidade anterior
            limparDadosCidade();
            
            // Mostrar notificação detalhada
            mostrarNotificacao(`✅ ${dados.nome_amigavel} (${dados.total_imagens} imagens)`, 'success');
            
            // Recarregar pastas para atualizar checkmark
            setTimeout(carregarPastasDisponiveis, 500);
            
            // Carregar dados da nova cidade (se existirem)
            setTimeout(atualizarResultados, 1000);
        } else {
            mostrarNotificacao('❌ Erro: ' + dados.mensagem, 'danger');
        }
    } catch (erro) {
        console.error('Erro ao selecionar pasta:', erro);
        mostrarNotificacao('❌ Erro ao selecionar pasta', 'danger');
    }
}

/**
 * Limpa tabelas e dados da cidade anterior
 * @returns {void}
 */
function limparDadosCidade() {
    // Limpar tabela de resultados
    const tabelaResultados = document.getElementById('tbody-resultados');
    if (tabelaResultados) {
        tabelaResultados.innerHTML = '<tr><td colspan="6" class="text-center text-muted">Nenhum resultado ainda</td></tr>';
    }
    
    // Limpar tabela de tendências
    const tabelaTendencias = document.getElementById('tbody-tendencias');
    if (tabelaTendencias) {
        tabelaTendencias.innerHTML = '<tr><td colspan="5" class="text-center text-muted">Nenhuma tendência calculada</td></tr>';
    }
    
    // Resetar status
    const statusProcessados = document.getElementById('status-processados');
    const statusResultados = document.getElementById('status-resultados');
    const statusTexto = document.getElementById('status-texto');
    
    if (statusProcessados) statusProcessados.textContent = '0';
    if (statusResultados) statusResultados.textContent = '0';
    if (statusTexto) statusTexto.innerHTML = '<i class="text-muted">Aguardando processamento...</i>';
    
    // Limpar resumo estatístico
    document.getElementById('resumo-total').textContent = '0';
    document.getElementById('resumo-media').textContent = '-';
    document.getElementById('resumo-minimo').textContent = '-';
    document.getElementById('resumo-maximo').textContent = '-';
}

/**
 * Mostra notificação temporária
 * @param {string} mensagem - Mensagem a exibir
 * @param {string} tipo - Tipo de alerta (success, danger, info, warning)
 */
function mostrarNotificacao(mensagem, tipo = 'info') {
    const container = document.body;
    const alerta = document.createElement('div');
    alerta.className = `alert alert-${tipo} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x`;
    alerta.style.zIndex = '9999';
    alerta.style.marginTop = '100px';
    alerta.innerHTML = `
        ${mensagem}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    container.appendChild(alerta);
    
    // Remover após 3 segundos
    setTimeout(() => {
        alerta.remove();
    }, 3000);
}

// ============================================================================
// GERENCIAMENTO DE UPLOAD
// ============================================================================

/**
 * Processa arquivo selecionado através do file picker
 * 
 * Valida se o arquivo é TIFF/TIFF, lê em formato ArrayBuffer
 * e inicia a análise via {@link analisarArquivoUpload}
 * 
 * @param {Event} event - Evento de mudança do input file
 * @returns {void}
 */
function handleFilePicker(event) {
    const file = event.target.files[0];
    if (!file) return;

    // Validar extensão
    if (!file.name.toLowerCase().endsWith('.tif') && !file.name.toLowerCase().endsWith('.tiff')) {
        alert('Por favor, selecione um arquivo .tif ou .tiff');
        return;
    }

    // Ler arquivo como ArrayBuffer para envio seguro
    const reader = new FileReader();
    reader.onload = function(e) {
        analisarArquivoUpload(file.name, e.target.result);
    };
    reader.readAsArrayBuffer(file);
}

/**
 * Inicia análise de arquivo enviado via upload
 * 
 * Envia arquivo para o backend via POST em /api/analisar-upload,
 * gerencia estados visuais (loading, erro, resultados) e trata
 * respostas da API.
 * 
 * @param {string} nomeArquivo - Nome do arquivo TIFF
 * @param {ArrayBuffer} dados - Conteúdo binário do arquivo
 * @returns {void}
 * 
 * @emits loading - Mostra spinner de carregamento
 * @emits resultados - Exibe estatísticas se sucesso
 * @emits erro - Exibe mensagem de erro se falha
 */
function analisarArquivoUpload(nomeArquivo, dados) {
    imagemSelecionada = { nome: nomeArquivo, tipo: 'upload' };
    
    // Remover seleção anterior
    document.querySelectorAll('.imagem-item').forEach(item => {
        item.classList.remove('active');
    });

    // Mostrar painel de loading, ocultar outros
    document.getElementById('painel-inicial').style.display = 'none';
    document.getElementById('painel-resultados').style.display = 'none';
    document.getElementById('painel-erro').style.display = 'none';
    document.getElementById('painel-loading').style.display = 'block';

    // Preparar FormData para envio
    const formData = new FormData();
    formData.append('file', new Blob([dados], { type: 'application/octet-stream' }), nomeArquivo);

    // Fazer requisição POST
    fetch('/api/analisar-upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('painel-loading').style.display = 'none';
        
        if (data.erro) {
            exibirErro(data.erro);
            return;
        }

        exibirResultados(data);
    })
    .catch(error => {
        console.error('Erro ao processar upload:', error);
        document.getElementById('painel-loading').style.display = 'none';
        exibirErro('Erro ao processar o arquivo');
    });
}

// ============================================================================
// GERENCIAMENTO DE LISTA DE IMAGENS (LEGADO)
// ============================================================================

/**
 * Carrega e exibe lista de imagens da pasta padrão
 * 
 * Busca imagens via GET em /api/listar-imagens, agrupa por ano
 * e cria elementos interativos para seleção.
 * 
 * @deprecated Esta função está desabilitada em favor do file picker
 * @returns {void}
 */
function carregarImagens() {
    fetch('/api/listar-imagens')
        .then(response => response.json())
        .then(data => {
            const listaImagens = document.getElementById('lista-imagens');
            listaImagens.innerHTML = '';

            if (data.length === 0) {
                listaImagens.innerHTML = '<p class="text-muted p-3">Nenhuma imagem encontrada</p>';
                return;
            }

            data.forEach(anoData => {
                // Cabeçalho agrupado por ano
                const anoHeader = document.createElement('div');
                anoHeader.className = 'ano-header';
                anoHeader.innerHTML = `<i class="bi bi-calendar3"></i> ${anoData.ano} (${anoData.total})`;
                listaImagens.appendChild(anoHeader);

                // Criar botão para cada imagem
                anoData.imagens.forEach(img => {
                    const itemLink = document.createElement('button');
                    itemLink.className = 'list-group-item list-group-item-action imagem-item';
                    itemLink.innerHTML = `
                        <div class="d-flex justify-content-between align-items-start">
                            <div class="text-start">
                                <strong>${img.nome}</strong>
                                <br/>
                                <small class="text-muted">${img.tamanho_kb.toFixed(1)} KB</small>
                            </div>
                            <i class="bi bi-chevron-right"></i>
                        </div>
                    `;
                    itemLink.onclick = function() {
                        selecionarImagem(img.caminho, img.nome);
                    };
                    listaImagens.appendChild(itemLink);
                });
            });
        })
        .catch(error => {
            console.error('Erro ao carregar imagens:', error);
            document.getElementById('lista-imagens').innerHTML = 
                '<p class="text-danger p-3">Erro ao carregar imagens</p>';
        });
}

/**
 * Seleciona imagem da lista e inicia análise
 * 
 * Registra seleção, atualiza visual, exibe loading
 * e chama {@link analisarImagem}
 * 
 * @deprecated Esta função está desabilitada em favor do file picker
 * @param {string} caminho - Caminho completo do arquivo TIFF
 * @param {string} nome - Nome do arquivo para exibição
 * @returns {void}
 */
function selecionarImagem(caminho, nome) {
    imagemSelecionada = { caminho, nome };
    
    // Atualizar visual de seleção
    document.querySelectorAll('.imagem-item').forEach(item => {
        item.classList.remove('active');
    });
    event.target.closest('.imagem-item').classList.add('active');

    // Mostrar loading
    document.getElementById('painel-inicial').style.display = 'none';
    document.getElementById('painel-resultados').style.display = 'none';
    document.getElementById('painel-erro').style.display = 'none';
    document.getElementById('painel-loading').style.display = 'block';

    analisarImagem(caminho);
}

/**
 * Analisa imagem via API
 * 
 * Envia caminho da imagem para backend via POST em /api/analisar
 * 
 * @deprecated Esta função está desabilitada em favor do file picker
 * @param {string} caminho - Caminho do arquivo no servidor
 * @returns {void}
 */
function analisarImagem(caminho) {
    fetch('/api/analisar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ caminho: caminho })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('painel-loading').style.display = 'none';
        
        if (data.erro) {
            exibirErro(data.erro);
            return;
        }

        exibirResultados(data);
    })
    .catch(error => {
        console.error('Erro:', error);
        document.getElementById('painel-loading').style.display = 'none';
        exibirErro('Erro ao conectar com o servidor');
    });
}

// ============================================================================
// EXIBIÇÃO DE RESULTADOS
// ============================================================================

/**
 * Exibe resultados da análise no painel de resultados
 * 
 * Popula todos os elementos DOM com dados de análise:
 * - Cabeçalho com dimensões e status
 * - Cards com estatísticas de pixels
 * - Tabela com estatísticas de intensidade
 * 
 * @param {Object} data - Objeto com dados de análise retornado pela API
 * @param {string} data.nome_arquivo - Nome do arquivo analisado
 * @param {string} data.dimensoes - Dimensões da imagem (ex: "27 × 40")
 * @param {string} data.total_pixels - Total de pixels formatado
 * @param {string} data.status - Status qualitativo (✓ ACEITA, ⚠ VERIFICAR, ✗ REJEITADA)
 * @param {string} data.status_class - Classe CSS (success, warning, danger)
 * @param {string} data.pixels_validos - Contador de pixels válidos
 * @param {string} data.percentual_valido - Percentual de pixels válidos
 * @param {string} data.pixels_nulos - Contador de pixels nulos
 * @param {string} data.percentual_nulos - Percentual de pixels nulos
 * @param {string} data.pixels_nodata - Contador de pixels NoData
 * @param {string} data.percentual_nodata - Percentual de pixels NoData
 * @param {string} data.pixels_outliers - Contador de pixels outliers
 * @param {string} data.percentual_outliers - Percentual de pixels outliers
 * @param {string} data.intensidade_media - Média de intensidade luminosa
 * @param {string} data.intensidade_mediana - Mediana de intensidade
 * @param {string} data.intensidade_minima - Valor mínimo de intensidade
 * @param {string} data.intensidade_maxima - Valor máximo de intensidade
 * @param {string} data.desvio_padrao - Desvio padrão de intensidade
 * @param {string} data.threshold_outlier - Limite para detecção de outliers
 * @returns {void}
 */
function exibirResultados(data) {
    // Atualizar cabeçalho com informações do arquivo
    document.getElementById('resultado-titulo').textContent = data.nome_arquivo;
    document.getElementById('resultado-dimensoes').textContent = 
        `${data.dimensoes} pixels | Total: ${data.total_pixels}`;
    
    // Exibir status com cor apropriada
    const statusElement = document.getElementById('resultado-status');
    statusElement.textContent = data.status;
    statusElement.className = data.status_class;

    // === Estatísticas de Pixels ===
    document.getElementById('stat-pixels-validos').textContent = data.pixels_validos;
    document.getElementById('stat-percentual-validos').textContent = data.percentual_valido;
    
    document.getElementById('stat-pixels-nulos').textContent = data.pixels_nulos;
    document.getElementById('stat-percentual-nulos').textContent = data.percentual_nulos;
    
    document.getElementById('stat-pixels-nodata').textContent = data.pixels_nodata;
    document.getElementById('stat-percentual-nodata').textContent = data.percentual_nodata;
    
    document.getElementById('stat-pixels-outliers').textContent = data.pixels_outliers;
    document.getElementById('stat-percentual-outliers').textContent = data.percentual_outliers;

    // === Estatísticas de Intensidade Luminosa ===
    document.getElementById('stat-media').textContent = data.intensidade_media;
    document.getElementById('stat-mediana').textContent = data.intensidade_mediana;
    document.getElementById('stat-minima').textContent = data.intensidade_minima;
    document.getElementById('stat-maxima').textContent = data.intensidade_maxima;
    document.getElementById('stat-desvio').textContent = data.desvio_padrao;
    document.getElementById('stat-threshold').textContent = data.threshold_outlier;
    
    // Exibir threshold de crescimento de luz se disponível
    if (data.threshold_crescimento_luz) {
        document.getElementById('stat-crescimento-luz').textContent = data.threshold_crescimento_luz;
    }

    // Mostrar painel de resultados, ocultar outros
    document.getElementById('painel-resultados').style.display = 'block';
    document.getElementById('painel-erro').style.display = 'none';

    // Scroll suave até resultados
    document.getElementById('painel-resultados').scrollIntoView({ behavior: 'smooth' });
}

/**
 * Exibe mensagem de erro no painel de alerta
 * 
 * Oculta outros painéis e mostra alerta com mensagem
 * de erro para feedback ao usuário.
 * 
 * @param {string} mensagem - Mensagem de erro a exibir
 * @returns {void}
 */
function exibirErro(mensagem) {
    document.getElementById('painel-loading').style.display = 'none';
    document.getElementById('painel-resultados').style.display = 'none';
    document.getElementById('texto-erro').textContent = mensagem;
    document.getElementById('painel-erro').style.display = 'block';
}

/**
 * Retorna à tela inicial e limpa estado
 * 
 * Oculta painéis de resultados/erro, limpa seleção
 * de imagem e scroll até o topo.
 * 
 * @returns {void}
 */
function voltarParaInicial() {
    document.getElementById('painel-inicial').style.display = 'block';
    document.getElementById('painel-resultados').style.display = 'none';
    document.getElementById('painel-comparacao').style.display = 'none';
    document.getElementById('painel-erro').style.display = 'none';
    document.getElementById('painel-processamento-lote').style.display = 'none';
    
    // Esconder container de processamento e mostrar outros
    const containerProcessamento = document.getElementById('container-processamento');
    if (containerProcessamento) {
        containerProcessamento.style.display = 'none';
    }
    
    // Mostrar as outras rows
    const linhas = document.querySelectorAll('.container-fluid > .row');
    linhas.forEach((linha) => {
        linha.style.display = 'grid';
    });
    
    document.querySelectorAll('.imagem-item').forEach(item => {
        item.classList.remove('active');
    });
    imagemSelecionada = null;
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ============================================================================
// GERENCIADORES DE EVENTOS
// ============================================================================

/**
 * Fechar alertas ao clicar no botão close
 * Listener delegado para elementos com classe 'btn-close'
 */
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('btn-close')) {
        e.target.closest('.alert').style.display = 'none';
    }
});

// ============================================================================
// COMPARAÇÃO DE CRESCIMENTO DE LUZ
// ============================================================================

/**
 * Armazena dados dos arquivos para comparação
 */
let arquivosComparacao = {
    anterior: null,
    atual: null
};

/**
 * Monitora seleção de arquivos para comparação
 * Ativa botão quando ambos estão selecionados
 */
document.addEventListener('change', function(e) {
    if (e.target.id === 'file-anterior') {
        const files = e.target.files;
        if (files.length > 0) {
            const reader = new FileReader();
            reader.onload = function(evt) {
                arquivosComparacao.anterior = {
                    nome: files[0].name,
                    dados: evt.target.result
                };
                atualizarBotaoComparar();
            };
            reader.readAsArrayBuffer(files[0]);
        }
    }
    
    if (e.target.id === 'file-atual') {
        const files = e.target.files;
        if (files.length > 0) {
            const reader = new FileReader();
            reader.onload = function(evt) {
                arquivosComparacao.atual = {
                    nome: files[0].name,
                    dados: evt.target.result
                };
                atualizarBotaoComparar();
            };
            reader.readAsArrayBuffer(files[0]);
        }
    }
});

/**
 * Atualiza estado do botão comparar
 */
function atualizarBotaoComparar() {
    const btnComparar = document.getElementById('btn-comparar');
    const temAmbos = arquivosComparacao.anterior && arquivosComparacao.atual;
    btnComparar.disabled = !temAmbos;
}

/**
 * Inicia processo de comparação
 * Carrega e envia ambos os arquivos para análise e comparação
 */
function iniciarComparacao() {
    if (!arquivosComparacao.anterior || !arquivosComparacao.atual) {
        exibirErro('Selecione ambos os arquivos para comparação');
        return;
    }
    
    // Mostrar loading
    document.getElementById('painel-inicial').style.display = 'none';
    document.getElementById('painel-resultados').style.display = 'none';
    document.getElementById('painel-comparacao').style.display = 'none';
    document.getElementById('painel-erro').style.display = 'none';
    document.getElementById('painel-loading').style.display = 'block';
    document.getElementById('painel-loading').querySelector('p').textContent = 'Analisando e comparando imagens...';
    
    // Enviar arquivos e comparar
    enviarArquivosParaComparacao(arquivosComparacao.anterior, arquivosComparacao.atual);
}

/**
 * Envia arquivos para o servidor para análise e comparação
 */
function enviarArquivosParaComparacao(arquivoAnterior, arquivoAtual) {
    // Criar FormData com ambos os arquivos
    const formDataAnterior = new FormData();
    formDataAnterior.append('file', new Blob([arquivoAnterior.dados], { type: 'application/octet-stream' }), arquivoAnterior.nome);
    
    const formDataAtual = new FormData();
    formDataAtual.append('file', new Blob([arquivoAtual.dados], { type: 'application/octet-stream' }), arquivoAtual.nome);
    
    // Analisar primeiro arquivo
    fetch('/api/analisar-upload', {
        method: 'POST',
        body: formDataAnterior
    })
    .then(response => response.json())
    .then(dataAnterior => {
        if (dataAnterior.erro) {
            exibirErro('Erro ao analisar arquivo anterior: ' + dataAnterior.erro);
            document.getElementById('painel-loading').style.display = 'none';
            return;
        }
        
        // Analisar segundo arquivo
        fetch('/api/analisar-upload', {
            method: 'POST',
            body: formDataAtual
        })
        .then(response => response.json())
        .then(dataAtual => {
            if (dataAtual.erro) {
                exibirErro('Erro ao analisar arquivo atual: ' + dataAtual.erro);
                document.getElementById('painel-loading').style.display = 'none';
                return;
            }
            
            // Ambas as análises prontas, agora comparar
            compararComservidor(dataAnterior, dataAtual);
        })
        .catch(error => {
            console.error('Erro ao processar segundo arquivo:', error);
            exibirErro('Erro ao processar arquivos para comparação');
            document.getElementById('painel-loading').style.display = 'none';
        });
    })
    .catch(error => {
        console.error('Erro ao processar primeiro arquivo:', error);
        exibirErro('Erro ao processar arquivos para comparação');
        document.getElementById('painel-loading').style.display = 'none';
    });
}

/**
 * Chama a API para comparar dados já analisados
 */
function compararComservidor(dataAnterior, dataAtual) {
    // Extrair dados de intensidade para comparação local ou via API
    exibirResultadosComparacao(dataAnterior, dataAtual);
}

/**
 * Exibe resultados da comparação no painel
 */
function exibirResultadosComparacao(dataAnterior, dataAtual) {
    // Extrair valores numéricos
    const mediaAnterior = parseFloat(dataAnterior.intensidade_media);
    const mediaAtual = parseFloat(dataAtual.intensidade_media);
    const thresholdAnterior = parseFloat(dataAnterior.threshold_crescimento_luz);
    const thresholdAtual = parseFloat(dataAtual.threshold_crescimento_luz);
    const desvioAnterior = parseFloat(dataAnterior.desvio_padrao);
    
    // Calcular mudanças
    const crescimentoMedia = mediaAtual - mediaAnterior;
    const percentualCrescimento = (crescimentoMedia / mediaAnterior * 100);
    const diferencaThresholds = thresholdAtual - thresholdAnterior;
    const crescimentoSignificativo = crescimentoMedia > (desvioAnterior * 0.3);
    
    // Determinar status
    let statusCrescimento = '';
    let statusClass = '';
    if (percentualCrescimento > 5) {
        statusCrescimento = '🔴 CRESCIMENTO ALTO';
        statusClass = 'danger';
    } else if (percentualCrescimento > 1) {
        statusCrescimento = '🟡 CRESCIMENTO MODERADO';
        statusClass = 'warning';
    } else if (percentualCrescimento > -1) {
        statusCrescimento = '🟢 ESTÁVEL';
        statusClass = 'success';
    } else {
        statusCrescimento = '🔵 REDUÇÃO';
        statusClass = 'info';
    }
    
    // Gerar interpretação
    let interpretacao = '';
    if (percentualCrescimento > 10) {
        interpretacao = '⚠️ CRESCIMENTO MUITO ALTO: Indicativo de forte expansão urbana e aumento significativo de iluminação noturna.';
    } else if (percentualCrescimento > 5) {
        interpretacao = '📈 CRESCIMENTO ALTO: Desenvolvimento urbano significativo detectado. Aumento notável na infraestrutura de iluminação.';
    } else if (percentualCrescimento > 1) {
        interpretacao = '📊 CRESCIMENTO MODERADO: Desenvolvimento urbano gradual em curso. Pequeno aumento na iluminação.';
    } else if (percentualCrescimento > -1) {
        interpretacao = '➡️ ESTÁVEL: Pouca ou nenhuma mudança na intensidade de iluminação entre os períodos.';
    } else {
        interpretacao = '📉 REDUÇÃO: Queda na intensidade de iluminação detectada. Pode indicar economia de energia ou mudanças na infraestrutura.';
    }
    
    // Preencher painel
    document.getElementById('comp-arquivo-anterior').textContent = dataAnterior.nome_arquivo;
    document.getElementById('comp-arquivo-atual').textContent = dataAtual.nome_arquivo;
    document.getElementById('comp-media-anterior').textContent = dataAnterior.intensidade_media;
    document.getElementById('comp-media-atual').textContent = dataAtual.intensidade_media;
    document.getElementById('comp-crescimento-media').textContent = crescimentoMedia.toFixed(2);
    document.getElementById('comp-percentual-crescimento').textContent = percentualCrescimento.toFixed(2) + '%';
    document.getElementById('comp-status-crescimento').textContent = statusCrescimento;
    document.getElementById('comp-threshold-anterior').textContent = dataAnterior.threshold_crescimento_luz;
    document.getElementById('comp-threshold-atual').textContent = dataAtual.threshold_crescimento_luz;
    document.getElementById('comp-diferenca-thresholds').textContent = diferencaThresholds.toFixed(2);
    document.getElementById('comp-significativo').textContent = crescimentoSignificativo ? '✅ Sim' : '❌ Não';
    document.getElementById('comp-interpretacao').textContent = interpretacao;
    
    // Mostrar painel de comparação
    document.getElementById('painel-loading').style.display = 'none';
    document.getElementById('painel-comparacao').style.display = 'block';
    document.getElementById('painel-comparacao').scrollIntoView({ behavior: 'smooth' });
}

/**
 * Inicia nova comparação, limpando seleções
 */
function novaComparacao() {
    document.getElementById('file-anterior').value = '';
    document.getElementById('file-atual').value = '';
    document.getElementById('painel-comparacao').style.display = 'none';
    document.getElementById('painel-inicial').style.display = 'block';
    arquivosComparacao = { anterior: null, atual: null };
    atualizarBotaoComparar();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ============================================================================
// PROCESSAMENTO EM LOTE (PARALELO)
// ============================================================================

/**
 * Mostra painel de processamento em lote
 */
function mostrarPainelProcessamentoLote() {
    document.getElementById('painel-inicial').style.display = 'none';
    document.getElementById('painel-resultados').style.display = 'none';
    document.getElementById('painel-comparacao').style.display = 'none';
    document.getElementById('painel-erro').style.display = 'none';
    document.getElementById('painel-processamento-lote').style.display = 'block';
    
    // Mostrar container de processamento e esconder outros
    const containerProcessamento = document.getElementById('container-processamento');
    if (containerProcessamento) {
        containerProcessamento.style.display = 'grid';
    }
    
    // Esconder as outras rows
    const linhas = document.querySelectorAll('.container-fluid > .row');
    linhas.forEach((linha, index) => {
        if (index > 0) { // Pula a primeira que é o container-processamento
            linha.style.display = 'none';
        }
    });
    
    document.getElementById('painel-processamento-lote').scrollIntoView({ behavior: 'smooth' });
    
    // Carregar status e resultados iniciais
    atualizarStatusProcessamento();
    atualizarResultados();
}

/**
 * Mostra painel inicial
 */
function mostrarPainelInicial() {
    document.getElementById('painel-inicial').style.display = 'block';
    document.getElementById('painel-resultados').style.display = 'none';
    document.getElementById('painel-comparacao').style.display = 'none';
    document.getElementById('painel-erro').style.display = 'none';
    document.getElementById('painel-processamento-lote').style.display = 'none';
    
    // Esconder container de processamento e mostrar outros
    const containerProcessamento = document.getElementById('container-processamento');
    if (containerProcessamento) {
        containerProcessamento.style.display = 'none';
    }
    
    // Mostrar as outras rows
    const linhas = document.querySelectorAll('.container-fluid > .row');
    linhas.forEach((linha) => {
        linha.style.display = 'grid';
    });
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * Inicia processamento paralelo de todas as imagens
 */
function iniciarProcessamentoParalelo(forcar = false) {
    const btn = document.getElementById('btn-processar-paralelo');
    btn.disabled = true;
    btn.innerHTML = '<i class="bi bi-hourglass-split"></i> Processando...';
    
    const payload = {};
    if (forcar) {
        payload.forcar_reprocessamento = true;
    }
    
    fetch('/api/processar-paralelo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        if (data.sucesso) {
            const mensagem = forcar 
                ? '✅ Reprocessamento forçado iniciado!\n\nTodos os arquivos serão reprocessados com a nova normalização.\nTempo estimado: 5-10 minutos para ~120 imagens.'
                : '✅ Processamento iniciado em segundo plano!\n\nVocê será notificado quando terminar.\nTempo estimado: 5-10 minutos para ~120 imagens.';
            alert(mensagem);
            document.getElementById('div-status-processamento').style.display = 'block';
            atualizarStatusProcessamento();
            
            // Parar intervalo anterior se existir
            if (intervaloAtualizacaoStatus) {
                clearInterval(intervaloAtualizacaoStatus);
            }
            
            // Atualizar status a cada 2 segundos (mais rápido para feedback melhor)
            intervaloAtualizacaoStatus = setInterval(atualizarStatusProcessamento, 2000);
        } else {
            alert('❌ ' + data.erro);
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('❌ Erro ao iniciar processamento');
    })
    .finally(() => {
        btn.disabled = false;
        btn.innerHTML = '<i class="bi bi-play-fill"></i> Iniciar Processamento Paralelo';
    });
}

/**
 * Atualiza status de processamento
 */
function atualizarStatusProcessamento() {
    fetch('/api/status-processamento')
    .then(response => response.json())
    .then(data => {
        if (data.sucesso) {
            const processados = data.processados;
            const resultados = data.resultados;
            
            document.getElementById('status-processados').textContent = processados;
            document.getElementById('status-resultados').textContent = resultados;
            
            // Verificar se o processamento terminou
            // Processamento termina quando os arquivos existem e os números estabilizam
            const processamentoTerminou = (processados > 0 && processados === resultados) || 
                                         (processados > 0 && !data.cache_existe && data.resultados_existe);
            
            let statusTexto = '✓ Processamento completo!';
            let statusHTML = '<span class="text-success"><i class="bi bi-check-circle-fill"></i> Processamento completo!</span>';
            
            if (processados > 0 && processados > resultados) {
                statusTexto = '⏳ Processando...';
                statusHTML = '<span class="text-warning"><i class="bi bi-hourglass-split"></i> Processando...</span>';
            }
            
            document.getElementById('status-texto').innerHTML = statusHTML;
            
            // Se terminou, parar o intervalo e atualizar resultados
            if (processamentoTerminou) {
                console.log('Processamento finalizado! Parando atualizações...');
                if (intervaloAtualizacaoStatus) {
                    clearInterval(intervaloAtualizacaoStatus);
                    intervaloAtualizacaoStatus = null;
                }
                
                // Atualizar resultados automaticamente
                setTimeout(atualizarResultados, 500);
                
                // Notificar usuário
                if (Notification.permission === 'granted') {
                    new Notification('✅ Processamento Concluído!', {
                        body: `${resultados} imagens processadas com sucesso`,
                        icon: '/static/icon.png'
                    });
                }
            }
        }
    })
    .catch(error => console.error('Erro ao atualizar status:', error));
}

/**
 * Atualiza resultados e tendências
 */
function atualizarResultados() {
    console.log('🔄 atualizarResultados() chamado');
    
    // Carregar resultados
    fetch('/api/resultados')
    .then(response => response.json())
    .then(data => {
        console.log('✅ Resposta de resultados:', data);
        if (data.sucesso) {
            // Preencher tabela de resultados
            const tbody = document.getElementById('tbody-resultados');
            tbody.innerHTML = '';
            
            data.resultados.forEach(resultado => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><small>${resultado.arquivo}</small></td>
                    <td>${resultado.ano}</td>
                    <td>${resultado.mes}</td>
                    <td><strong>${resultado.intensidade_media}</strong></td>
                    <td>${resultado.threshold_crescimento}</td>
                    <td>${resultado.percentual_valido}%</td>
                `;
                tbody.appendChild(tr);
            });
            
            // Mostrar resumo estatístico
            document.getElementById('resumo-total').textContent = data.total_registros;
            document.getElementById('resumo-media').textContent = data.media_geral;
            document.getElementById('resumo-minimo').textContent = data.minimo;
            document.getElementById('resumo-maximo').textContent = data.maximo;
            
            document.getElementById('div-resultados-tabela').style.display = 'block';
            document.getElementById('div-resumo-stats').style.display = 'block';
        } else {
            // Mostrar mensagem de erro
            console.warn('⚠️ Sem resultados:', data.mensagem);
            mostrarNotificacao(`⚠️ ${data.mensagem}`, 'warning');
            
            // Limpar tabelas
            const tbody = document.getElementById('tbody-resultados');
            if (tbody) {
                tbody.innerHTML = '<tr><td colspan="6" class="text-center text-muted"><em>' + data.mensagem + '</em></td></tr>';
            }
            
            document.getElementById('div-resultados-tabela').style.display = 'block';
        }
    })
    .catch(error => {
        console.error('❌ Erro ao carregar resultados:', error);
        mostrarNotificacao('Erro ao carregar resultados: ' + error.message, 'danger');
    });
    
    // Carregar tendências
    console.log('📊 Iniciando carregamento de tendências...');
    fetch('/api/tendencias')
    .then(response => {
        console.log('📝 Resposta recebida, status:', response.status);
        return response.json();
    })
    .then(data => {
        console.log('✅ Dados de tendências:', data);
        if (data.sucesso) {
            console.log('📈 Preenchendo tabela com', data.tendencias.length, 'anos');
            // Preencher tabela de tendências
            const tbody = document.getElementById('tbody-tendencias');
            if (!tbody) {
                console.error('❌ Elemento tbody-tendencias não encontrado!');
                return;
            }
            
            tbody.innerHTML = '';
            
            data.tendencias.forEach(tendencia => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><strong>${tendencia.ano}</strong></td>
                    <td>${tendencia.media}</td>
                    <td>${tendencia.minimo}</td>
                    <td>${tendencia.maximo}</td>
                    <td>${tendencia.desvio}</td>
                    <td>${tendencia.registros}</td>
                `;
                tbody.appendChild(tr);
            });
            
            const divTendencias = document.getElementById('div-tendencias');
            if (divTendencias) {
                divTendencias.style.display = 'block';
                console.log('✅ Div-tendencias mostrada');
            } else {
                console.error('❌ Elemento div-tendencias não encontrado!');
            }
        } else {
            console.warn('⚠️ Tendências não disponíveis:', data.mensagem);
            const tbody = document.getElementById('tbody-tendencias');
            if (tbody) {
                tbody.innerHTML = '<tr><td colspan="6" class="text-center text-muted"><em>' + data.mensagem + '</em></td></tr>';
            }
        }
    })
    .catch(error => {
        console.error('❌ Erro ao carregar tendências:', error);
    });
}

/**
 * Volta para painel inicial
 */
function voltarParaInicial() {
    mostrarPainelInicial();
}

// ===== MAPA DO VALE DO ITAJAÍ =====
let mapa = null;
let areasRegionais = {};  // Armazena os círculos das cidades
let areaAtiva = null;     // Área atualmente destacada
const COR_ATIVA = '#667eea';
const COR_INATIVA = '#b0b8d4';
const RAIO_CIDADE = 4500;  // 4.5 km em metros para melhor visibilidade

/**
 * Inicializa o mapa interativo com áreas regionais das cidades
 * Adiciona suporte responsivo completo
 */
function inicializarMapa() {
    fetch('/api/coordenadas-cidades')
        .then(res => res.json())
        .then(data => {
            if (!data.sucesso) {
                console.error('Erro ao carregar coordenadas:', data);
                return;
            }
            
            const centro = data.centro;
            const zoom = data.zoom;
            
            // Inicializar Leaflet
            mapa = L.map('mapa', {
                zoomControl: true,
                scrollWheelZoom: true,
                dragging: true
            }).setView([centro.lat, centro.lng], zoom);
            
            // Adicionar layer do OpenStreetMap com melhor performance
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap',
                maxZoom: 19,
                minZoom: 9,
                crossOrigin: 'anonymous'
            }).addTo(mapa);
            
            // Adicionar círculos para cada cidade
            const cidades_array = Object.keys(data.cidades);
            cidades_array.forEach(cidade_chave => {
                const cidade = data.cidades[cidade_chave];
                
                // Criar círculo para a região da cidade com melhor visibilidade
                const circulo = L.circle([cidade.lat, cidade.lng], {
                    radius: RAIO_CIDADE,
                    color: COR_INATIVA,
                    weight: 2,
                    opacity: 0.4,
                    fillColor: COR_INATIVA,
                    fillOpacity: 0.08,
                    interactive: true,
                    className: 'cidade-circle'
                }).addTo(mapa);
                
                // Tooltip melhorado ao passar o mouse
                circulo.bindTooltip(`
                    <div style="font-weight: bold;">${cidade.nome_amigavel}</div>
                    <div style="font-size: 0.85em;">📊 ${cidade.total_imagens} imagens</div>
                `, {
                    permanent: false,
                    direction: 'top',
                    className: 'cidade-tooltip'
                });
                
                // Popup ao clicar
                circulo.bindPopup(`
                    <div style="text-align: center; min-width: 180px;">
                        <div style="font-weight: bold; font-size: 1.1em; margin-bottom: 5px;">
                            ${cidade.nome_amigavel}
                        </div>
                        <div style="font-size: 0.9em; color: #666;">
                            📊 ${cidade.total_imagens} imagens disponíveis
                        </div>
                        <button onclick="selecionarCidadeNoMapa('${cidade_chave}')" 
                                style="margin-top: 10px; padding: 5px 15px; background: #667eea; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;">
                            Selecionar
                        </button>
                    </div>
                `, {
                    maxWidth: 250
                });
                
                // Clique no círculo → seleciona a cidade
                circulo.on('click', () => {
                    selecionarCidadeNoMapa(cidade_chave);
                });
                
                // Efeito hover melhorado
                circulo.on('mouseover', () => {
                    circulo.setStyle({
                        weight: 3,
                        opacity: 0.6,
                        fillOpacity: 0.15,
                        color: '#667eea'
                    });
                    circulo.bringToFront();
                });
                
                circulo.on('mouseout', () => {
                    if (circulo !== areaAtiva) {
                        circulo.setStyle({
                            weight: 2,
                            opacity: 0.4,
                            fillOpacity: 0.08,
                            color: COR_INATIVA
                        });
                        circulo.bringToBack();
                    }
                });
                
                areasRegionais[cidade_chave] = circulo;
            });
            
            // Recalcular bounds de todas as cidades para melhor ajuste inicial
            const allBounds = [];
            Object.values(areasRegionais).forEach(circulo => {
                allBounds.push(circulo.getBounds());
            });
            if (allBounds.length > 0) {
                let bounds = allBounds[0];
                allBounds.slice(1).forEach(b => {
                    bounds.extend(b);
                });
                // Adicionar padding assimétrico: [top, left, bottom, right] - menos no topo por causa da navbar
                mapa.fitBounds(bounds, { padding: [20, 80, 80, 80], maxZoom: zoom });
            }
            
            // ✨ RESPONSIVIDADE: Redimensionar mapa ao fazer scroll/resize
            function atualizarTamanhoMapa() {
                if (mapa) {
                    setTimeout(() => {
                        mapa.invalidateSize();
                    }, 100);
                }
            }
            
            // Event listeners para responsividade
            window.addEventListener('resize', atualizarTamanhoMapa);
            window.addEventListener('orientationchange', atualizarTamanhoMapa);
            
            // Monitorar mudanças no tamanho do container
            let ultimaTamanho = null;
            setInterval(() => {
                const mapaContainer = document.getElementById('mapa-container');
                if (mapaContainer) {
                    const tamanhoBsAtual = mapaContainer.getBoundingClientRect().width;
                    if (ultimaTamanho !== tamanhoBsAtual) {
                        ultimaTamanho = tamanhoBsAtual;
                        atualizarTamanhoMapa();
                    }
                }
            }, 500);
            
            console.log('✅ Mapa inicializado com', cidades_array.length, 'cidades!');
            console.log('🗺️ Zoom inicial:', zoom);
        })
        .catch(error => {
            console.error('❌ Erro ao carregar mapa:', error);
        });
}

/**
 * Destaca uma cidade no mapa ao ser selecionada
 * Com melhor centralização e animação
 */
function destacarCidadeNoMapa(cidade_chave) {
    // Remover destaque anterior
    if (areaAtiva) {
        areaAtiva.setStyle({
            color: COR_INATIVA,
            weight: 2,
            opacity: 0.4,
            fillColor: COR_INATIVA,
            fillOpacity: 0.08
        });
        areaAtiva.bringToBack();
    }
    
    // Destacar nova cidade com efeito visual melhorado
    if (areasRegionais[cidade_chave]) {
        areaAtiva = areasRegionais[cidade_chave];
        areaAtiva.setStyle({
            color: COR_ATIVA,
            weight: 4,
            opacity: 0.8,
            fillColor: COR_ATIVA,
            fillOpacity: 0.2
        });
        areaAtiva.bringToFront();
        
        // Animar zoom e centralização suave
        if (areaAtiva.getBounds) {
            const bounds = areaAtiva.getBounds();
            mapa.fitBounds(bounds, { 
                padding: [20, 100, 100, 100],
                maxZoom: 13,
                animate: true,
                duration: 0.8
            });
        }
        
        // Abrir popup com info
        if (areaAtiva.openPopup) {
            areaAtiva.openPopup();
        }
    }
}

/**
 * Seleciona cidade ao clicar no mapa
 */
function selecionarCidadeNoMapa(cidade_chave) {
    // Destacar no mapa
    destacarCidadeNoMapa(cidade_chave);
    
    // Selecionar no dropdown também (sem disparar novamente)
    if (window.selecionarPasta_Original) {
        window.selecionarPasta_Original(cidade_chave);
    }
}

// Integração com seleção de pasta (wrapper da função original)
const selecionarPasta_Original = window.selecionarPasta;
window.selecionarPasta = function(chave) {
    selecionarPasta_Original(chave);
    
    // Atualizar mapa com novo destaque
    if (areasRegionais[chave]) {
        destacarCidadeNoMapa(chave);
    }
};

// ============================================================================
// SUGESTÃO DE THRESHOLDS
// ============================================================================

/**
 * Mostra painel de sugestão de thresholds
 */
function mostrarPainelSugestaoThresholds() {
    document.getElementById('painel-inicial').style.display = 'none';
    document.getElementById('painel-resultados').style.display = 'none';
    document.getElementById('painel-comparacao').style.display = 'none';
    document.getElementById('painel-erro').style.display = 'none';
    document.getElementById('painel-processamento-lote').style.display = 'none';
    document.getElementById('painel-sugestao-thresholds').style.display = 'block';
    
    // Mostrar container de processamento e esconder outros
    const containerProcessamento = document.getElementById('container-processamento');
    if (containerProcessamento) {
        containerProcessamento.style.display = 'grid';
    }
    
    // Esconder as outras rows
    const linhas = document.querySelectorAll('.container-fluid > .row');
    linhas.forEach((linha, index) => {
        if (index > 0) {
            linha.style.display = 'none';
        }
    });
    
    document.getElementById('painel-sugestao-thresholds').scrollIntoView({ behavior: 'smooth' });
}

/**
 * Carrega sugestões de threshold da API
 */
async function carregarSugestoesThreshold() {
    const loader = document.getElementById('threshold-loader');
    const conteudo = document.getElementById('threshold-conteudo');
    const btnCarregar = document.getElementById('btn-carregar-sugestoes');
    
    // Mostrar loader
    loader.style.display = 'block';
    conteudo.style.display = 'none';
    btnCarregar.disabled = true;
    
    try {
        const response = await fetch('/api/sugerir-thresholds');
        const resultado = await response.json();
        
        if (!resultado.sucesso) {
            mostrarNotificacao('❌ ' + resultado.mensagem, 'danger');
            loader.style.display = 'none';
            btnCarregar.disabled = false;
            return;
        }
        
        const dados = resultado.dados;
        
        // Preencher dados gerais
        const periodos = dados.periodos;
        document.getElementById('threshold-periodo').textContent = 
            `${periodos.primeiro_ano} - ${periodos.ultimo_ano} (${periodos.total_anos} anos)`;
        
        // Preencher crescimento
        const crescimento = dados.crescimento;
        document.getElementById('threshold-crescimento-abs').textContent = 
            `${crescimento.absoluto > 0 ? '+' : ''}${crescimento.absoluto}`;
        document.getElementById('threshold-crescimento-pct').textContent = 
            `${crescimento.percentual > 0 ? '+' : ''}${crescimento.percentual}%`;
        document.getElementById('threshold-tendencia').textContent = 
            formatarTendencia(crescimento.tendencia);
        
        // Preencher thresholds sugeridos
        const thresholds = dados.thresholds_sugeridos;
        document.getElementById('threshold-conservador').textContent = thresholds.conservador;
        document.getElementById('threshold-moderado').textContent = thresholds.moderado;
        document.getElementById('threshold-agressivo').textContent = thresholds.agressivo;
        document.getElementById('threshold-alto-crescimento').textContent = thresholds.alto_crescimento;
        
        // Preencher estatísticas gerais
        const stats = dados.estatisticas_gerais;
        document.getElementById('threshold-media-geral').textContent = stats.media_geral;
        document.getElementById('threshold-desvio-geral').textContent = stats.desvio_geral;
        document.getElementById('threshold-minimo-geral').textContent = stats.minimo_geral;
        document.getElementById('threshold-maximo-geral').textContent = stats.maximo_geral;
        
        // Preencher comparação de períodos se disponível
        if (dados.comparacao_periodos && Object.keys(dados.comparacao_periodos).length > 0) {
            const comp = dados.comparacao_periodos;
            document.getElementById('threshold-periodo-inicio').textContent = comp.periodo_inicio;
            document.getElementById('threshold-media-inicio').textContent = comp.media_inicio;
            document.getElementById('threshold-periodo-fim').textContent = comp.periodo_fim;
            document.getElementById('threshold-media-fim').textContent = comp.media_fim;
            document.getElementById('threshold-crescimento-periodo-abs').textContent = 
                `${comp.crescimento_absoluto > 0 ? '+' : ''}${comp.crescimento_absoluto}`;
            document.getElementById('threshold-crescimento-periodo-pct').textContent = 
                `${comp.crescimento_percentual > 0 ? '+' : ''}${comp.crescimento_percentual}%`;
            document.getElementById('threshold-comparacao-periodos').style.display = 'block';
        } else {
            document.getElementById('threshold-comparacao-periodos').style.display = 'none';
        }
        
        // Preencher tabela de dados por ano
        const tabelaAnos = document.getElementById('tbody-threshold-anos');
        tabelaAnos.innerHTML = '';
        
        for (const [ano, dados_ano] of Object.entries(dados.anos_com_dados)) {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong>${ano}</strong></td>
                <td>${dados_ano.media}</td>
                <td>${dados_ano.minimo}</td>
                <td>${dados_ano.maximo}</td>
                <td>${dados_ano.desvio}</td>
                <td>${dados_ano.registros}</td>
            `;
            tabelaAnos.appendChild(tr);
        }
        
        // Preencher recomendações
        const divRecomendacoes = document.getElementById('threshold-recomendacoes');
        divRecomendacoes.innerHTML = '';
        
        dados.recomendacoes.forEach(recom => {
            const p = document.createElement('p');
            p.className = 'mb-2';
            p.innerHTML = `<i class="bi bi-check-circle-fill text-success me-2"></i> ${recom}`;
            divRecomendacoes.appendChild(p);
        });
        
        // Preencher exemplos de imagens se disponível
        if (dados.exemplos_imagens && dados.exemplos_imagens.periodo_inicio) {
            const exemplos = dados.exemplos_imagens;
            
            // Exemplos do período inicial
            const divExemploInicio = document.getElementById('threshold-exemplo-inicio');
            divExemploInicio.innerHTML = '';
            
            exemplos.periodo_inicio.imagens.forEach(img => {
                const div = document.createElement('div');
                div.className = 'mb-3 p-3 bg-light rounded border-start border-4';
                div.style.borderLeftColor = '#667eea';
                div.innerHTML = `
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <strong>${img.titulo}</strong><br>
                            <small class="text-muted">📄 ${img.arquivo}</small><br>
                            <small class="text-muted">Mês: ${img.mes}</small><br>
                            <strong class="text-primary">Intensidade: ${img.intensidade}</strong>
                        </div>
                        ${img.tipo ? `<span class="badge bg-info">${img.tipo}</span>` : ''}
                    </div>
                `;
                divExemploInicio.appendChild(div);
            });
            
            // Exemplos do período final
            const divExemploFim = document.getElementById('threshold-exemplo-fim');
            divExemploFim.innerHTML = '';
            
            exemplos.periodo_fim.imagens.forEach(img => {
                const div = document.createElement('div');
                div.className = 'mb-3 p-3 bg-light rounded border-start border-4';
                div.style.borderLeftColor = '#28a745';
                div.innerHTML = `
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <strong>${img.titulo}</strong><br>
                            <small class="text-muted">📄 ${img.arquivo}</small><br>
                            <small class="text-muted">Mês: ${img.mes}</small><br>
                            <strong class="text-success">Intensidade: ${img.intensidade}</strong>
                        </div>
                        ${img.tipo ? `<span class="badge bg-success">${img.tipo}</span>` : ''}
                    </div>
                `;
                divExemploFim.appendChild(div);
            });
            
            document.getElementById('threshold-exemplos-section').style.display = 'block';
        } else {
            document.getElementById('threshold-exemplos-section').style.display = 'none';
        }
        
        // Mostrar conteúdo e esconder loader
        loader.style.display = 'none';
        conteudo.style.display = 'block';
        btnCarregar.disabled = false;
        
        mostrarNotificacao('✅ Sugestões de threshold geradas com sucesso!', 'success');
        
    } catch (error) {
        console.error('Erro ao carregar sugestões:', error);
        mostrarNotificacao('❌ Erro ao carregar sugestões de threshold', 'danger');
        loader.style.display = 'none';
        btnCarregar.disabled = false;
    }
}

/**
 * Formata a tendência para exibição
 */
function formatarTendencia(tendencia) {
    const formatacoes = {
        'crescimento': '📈 Crescimento',
        'estável': '➡️ Estável',
        'declínio': '📉 Declínio'
    };
    return formatacoes[tendencia] || tendencia;
}

/**
 * Exporta as sugestões de threshold
 */
function exportarSugestoes() {
    try {
        // Coletar dados da página
        const periodo = document.getElementById('threshold-periodo').textContent;
        const crescimento = document.getElementById('threshold-crescimento-pct').textContent;
        const conservador = document.getElementById('threshold-conservador').textContent;
        const moderado = document.getElementById('threshold-moderado').textContent;
        const agressivo = document.getElementById('threshold-agressivo').textContent;
        
        // Criar CSV
        let csv = 'Sugestão de Thresholds para Crescimento de Luz\n';
        csv += '==============================================\n\n';
        csv += `Período Analisado,${periodo}\n`;
        csv += `Crescimento Detectado,${crescimento}\n\n`;
        csv += 'THRESHOLDS SUGERIDOS\n';
        csv += `Conservador (detecta leves mudanças),${conservador}\n`;
        csv += `Moderado (padrão recomendado),${moderado}\n`;
        csv += `Agressivo (detecta mudanças fortes),${agressivo}\n\n`;
        csv += 'Nota: Use o threshold MODERADO para comparações entre anos diferentes.\n';
        
        // Download
        const element = document.createElement('a');
        element.setAttribute('href', 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv));
        element.setAttribute('download', 'sugestao_thresholds.csv');
        element.style.display = 'none';
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
        
        mostrarNotificacao('✅ Arquivo exportado com sucesso!', 'success');
    } catch (error) {
        console.error('Erro ao exportar:', error);
        mostrarNotificacao('❌ Erro ao exportar dados', 'danger');
    }
}

// ========== RESPONSIVIDADE E EVENTOS DO MAPA ==========

/**
 * Trata scroll da página - invalida tamanho do mapa
 * para garantir que redimensione corretamente
 */
let scrollTimeout = null;
function handlePageScroll() {
    if (scrollTimeout) clearTimeout(scrollTimeout);
    scrollTimeout = setTimeout(() => {
        if (mapa) {
            mapa.invalidateSize();
        }
    }, 200);
}

/**
 * Observa mudanças de visibilidade da página
 */
function handleVisibilityChange() {
    if (!document.hidden && mapa) {
        // Página ficou visível novamente
        setTimeout(() => {
            mapa.invalidateSize();
        }, 100);
    }
}

/**
 * Observa mudanças na visibilidade do container do mapa
 */
function setupMapContainerObserver() {
    const mapaContainer = document.getElementById('mapa-container');
    if (!mapaContainer) return;
    
    const observer = new MutationObserver(() => {
        if (mapa) {
            mapa.invalidateSize();
        }
    });
    
    observer.observe(mapaContainer, {
        attributes: true,
        style: true,
        attributeFilter: ['style', 'class']
    });
    
    return observer;
}

// ============================================================================
// HEATMAP DE CRESCIMENTO LUMINOSO
// ============================================================================

/**
 * Mostra o painel de heatmap
 */
function mostrarPainelHeatmap() {
    // Esconder outros painéis
    let el = document.getElementById('painel-inicial');
    if (el) el.style.display = 'none';
    
    el = document.getElementById('painel-processamento');
    if (el) el.style.display = 'none';
    
    el = document.getElementById('painel-resultados');
    if (el) el.style.display = 'none';
    
    el = document.getElementById('painel-sugestao-thresholds');
    if (el) el.style.display = 'none';
    
    // Mostrar painel de heatmap
    document.getElementById('painel-heatmap-crescimento').style.display = 'block';
    
    // Scroll para o topo
    el = document.querySelector('.container-analise');
    if (el) {
        el.scrollIntoView({ behavior: 'smooth' });
    }
}

/**
 * Gera o heatmap de crescimento luminoso
 */
async function gerarHeatmap() {
    try {
        // Mostrar painel
        mostrarPainelHeatmap();
        
        // Mostrar loader
        document.getElementById('heatmap-loader').style.display = 'block';
        document.getElementById('heatmap-conteudo').style.display = 'none';
        document.getElementById('btn-gerar-heatmap').disabled = true;
        
        // Chamar API
        const response = await fetch('/api/gerar-heatmap');
        const dados = await response.json();
        
        if (!dados.sucesso) {
            throw new Error(dados.mensagem || 'Erro ao gerar heatmap');
        }
        
        // Ocultar loader e mostrar conteúdo
        document.getElementById('heatmap-loader').style.display = 'none';
        document.getElementById('heatmap-conteudo').style.display = 'block';
        
        // Exibir relatório
        const relatorioDiv = document.getElementById('heatmap-relatorio');
        relatorioDiv.textContent = dados.relatorio || 'Relatório indisponível';
        
        // Exibir imagens com timestamp para evitar cache
        const timestamp = new Date().getTime();
        const baseUrl = '/heatmap/';
        
        if (dados.arquivos.crescimento) {
            document.getElementById('heatmap-crescimento-img').src = 
                `${baseUrl}${dados.arquivos.crescimento}?t=${timestamp}`;
        }
        
        if (dados.arquivos.intensidade) {
            document.getElementById('heatmap-intensidade-img').src = 
                `${baseUrl}${dados.arquivos.intensidade}?t=${timestamp}`;
        }
        
        if (dados.arquivos.comparativo) {
            document.getElementById('heatmap-comparativo-img').src = 
                `${baseUrl}${dados.arquivos.comparativo}?t=${timestamp}`;
        }
        
        mostrarNotificacao('✅ Heatmap gerado com sucesso!', 'success');
        document.getElementById('btn-gerar-heatmap').disabled = false;
        
    } catch (error) {
        console.error('Erro ao gerar heatmap:', error);
        document.getElementById('heatmap-loader').style.display = 'none';
        document.getElementById('btn-gerar-heatmap').disabled = false;
        mostrarNotificacao(`❌ Erro: ${error.message}`, 'danger');
    }
}

/**
 * Baixa as imagens do heatmap
 */
function baixarHeatmaps() {
    try {
        const imagens = [
            { id: 'heatmap-crescimento-img', nome: 'heatmap_crescimento.png' },
            { id: 'heatmap-intensidade-img', nome: 'heatmap_intensidade.png' },
            { id: 'heatmap-comparativo-img', nome: 'heatmap_comparativo.png' }
        ];
        
        imagens.forEach(img => {
            const imgElement = document.getElementById(img.id);
            if (imgElement && imgElement.src) {
                const link = document.createElement('a');
                link.href = imgElement.src;
                link.download = img.nome;
                link.click();
            }
        });
        
        mostrarNotificacao('✅ Imagens baixadas!', 'success');
    } catch (error) {
        console.error('Erro ao baixar:', error);
        mostrarNotificacao('❌ Erro ao baixar imagens', 'danger');
    }
}

/**
 * Mostra o painel de mapa de crescimento
 */
function mostrarPainelMapaCrescimento() {
    // Esconder todos os painéis
    let painelAnalise = document.getElementById('painel-analise-imagem');
    let painelProcessamento = document.getElementById('painel-processamento-lote');
    let painelThreshold = document.getElementById('painel-sugestao-thresholds');
    let painelHeatmap = document.getElementById('painel-heatmap-crescimento');
    
    if (painelAnalise) painelAnalise.style.display = 'none';
    if (painelProcessamento) painelProcessamento.style.display = 'none';
    if (painelThreshold) painelThreshold.style.display = 'none';
    if (painelHeatmap) painelHeatmap.style.display = 'none';
    
    // Mostrar painel de mapa
    let painelMapa = document.getElementById('painel-mapa-crescimento');
    if (painelMapa) {
        painelMapa.style.display = 'block';
        painelMapa.scrollIntoView({ behavior: 'smooth' });
    }
}

/**
 * Gera o mapa interativo de crescimento para a cidade selecionada
 */
async function gerarMapaCrescimento() {
    try {
        const btnGerar = document.getElementById('btn-gerar-mapa');
        const loader = document.getElementById('mapa-loader');
        const conteudo = document.getElementById('mapa-conteudo');
        
        // Mostrar loader
        if (btnGerar) btnGerar.disabled = true;
        if (loader) loader.style.display = 'block';
        if (conteudo) conteudo.style.display = 'none';
        
        // Chamar API
        const response = await fetch('/api/gerar-mapa-crescimento');
        const dados = await response.json();
        
        if (!dados.sucesso) {
            mostrarNotificacao(`❌ Erro: ${dados.erro || dados.mensagem}`, 'danger');
            if (loader) loader.style.display = 'none';
            if (btnGerar) btnGerar.disabled = false;
            return;
        }
        
        // Atualizar cabeçalho com informações da cidade
        let titulo = document.querySelector('#painel-mapa-crescimento .card-header h5');
        if (titulo) {
            titulo.textContent = `🗺️ Mapa de Crescimento Luminoso - ${dados.cidade}`;
        }
        
        // Determinar classe CSS de status
        let statusClass = 'text-info';
        if (dados.crescimento > 0) statusClass = 'text-danger';
        else if (dados.crescimento < 0) statusClass = 'text-primary';
        else statusClass = 'text-warning';
        
        // Mostrar estatísticas de uma única cidade
        const statsHtml = `
            <div class="row">
                <div class="col-md-12">
                    <div class="text-center">
                        <h3 class="${statusClass}">${dados.crescimento > 0 ? '+' : ''}${dados.crescimento}%</h3>
                        <small class="text-muted">Taxa de Crescimento</small>
                    </div>
                </div>
            </div>
        `;
        
        let statsContainer = document.querySelector('#painel-mapa-crescimento .card-body:first-of-type');
        if (statsContainer && statsContainer.innerHTML.includes('Resumo')) {
            let existingStats = statsContainer.querySelector('.row');
            if (existingStats) {
                existingStats.innerHTML = statsHtml;
            }
        }
        
        // Carregar mapa no iframe
        const baseUrl = window.location.origin;
        const timestamp = new Date().getTime();
        const iframeEl = document.getElementById('mapa-iframe');
        if (iframeEl) {
            iframeEl.src = `${baseUrl}${dados.url_mapa}&t=${timestamp}`;
        }
        
        // Esconder loader e mostrar conteúdo
        if (loader) loader.style.display = 'none';
        if (conteudo) conteudo.style.display = 'block';
        if (btnGerar) btnGerar.disabled = false;
        
        mostrarNotificacao(`✅ Mapa gerado para ${dados.cidade}!`, 'success');
    } catch (error) {
        console.error('Erro ao gerar mapa:', error);
        mostrarNotificacao('❌ Erro ao gerar mapa', 'danger');
        
        let btnGerar = document.getElementById('btn-gerar-mapa');
        let loader = document.getElementById('mapa-loader');
        if (btnGerar) btnGerar.disabled = false;
        if (loader) loader.style.display = 'none';
    }
}

/**
 * Gera timelapse das imagens da cidade com overlay de crescimento
 */
async function gerarTimelapse() {
    try {
        const loader = document.getElementById('mapa-loader');
        const conteudo = document.getElementById('mapa-conteudo');
        
        // Mostrar loader
        if (loader) loader.style.display = 'block';
        if (conteudo) conteudo.style.display = 'none';
        
        // Chamar API de timelapse
        const response = await fetch('/api/gerar-timelapse');
        const dados = await response.json();
        
        if (!dados.sucesso) {
            mostrarNotificacao(`❌ Erro: ${dados.erro || dados.mensagem}`, 'danger');
            if (loader) loader.style.display = 'none';
            return;
        }
        
        // Atualizar cabeçalho
        let titulo = document.querySelector('#painel-mapa-crescimento .card-header h5');
        if (titulo) {
            titulo.textContent = `⏱️ Timelapse - ${dados.cidade}`;
        }
        
        // Carregar timelapse no iframe
        const baseUrl = window.location.origin;
        const timestamp = new Date().getTime();
        const iframeEl = document.getElementById('mapa-iframe');
        if (iframeEl) {
            iframeEl.src = `${baseUrl}${dados.url_timelapse}&t=${timestamp}`;
        }
        
        // Esconder loader e mostrar conteúdo
        if (loader) loader.style.display = 'none';
        if (conteudo) conteudo.style.display = 'block';
        
        mostrarNotificacao(`✅ Timelapse gerado para ${dados.cidade}!`, 'success');
    } catch (error) {
        console.error('Erro ao gerar timelapse:', error);
        mostrarNotificacao('❌ Erro ao gerar timelapse', 'danger');
        
        let loader = document.getElementById('mapa-loader');
        if (loader) loader.style.display = 'none';
    }
}

/**
 * Baixa o arquivo HTML do mapa
 */
function baixarMapaHTML() {
    try {
        const link = document.createElement('a');
        link.href = '/mapa-crescimento';
        link.download = 'mapa_crescimento.html';
        link.click();
        mostrarNotificacao('✅ Mapa baixado!', 'success');
    } catch (error) {
        console.error('Erro ao baixar:', error);
        mostrarNotificacao('❌ Erro ao baixar mapa', 'danger');
    }
}

// Inicializar mapa quando página carrega
window.addEventListener('load', () => {
    setTimeout(inicializarMapa, 1000);
    
    // Adicionar listeners de responsividade
    window.addEventListener('scroll', handlePageScroll, { passive: true });
    window.addEventListener('resize', () => {
        if (mapa) mapa.invalidateSize();
    });
    document.addEventListener('visibilitychange', handleVisibilityChange);
    
    // Observer para mudanças no container
    setTimeout(setupMapContainerObserver, 1500);
    
    console.log('✅ Eventos de responsividade do mapa configurados');
});
