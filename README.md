# Automação GIS: Extração de Pontos Extremos de Rede

Projeto de automação geoespacial com **Python, ArcPy e ArcGIS Pro** para extrair os extremos das feições lineares selecionadas, padronizar a orientação dos pontos e organizar atributos para análise e edição.

## 🎯 Objetivo

Reduzir etapas manuais na criação de pontos de início e fim de trechos lineares, mantendo atributos relevantes da camada de origem e disponibilizando coordenadas em formatos úteis para conferência.

## 🧩 O problema

Em rotinas de produção cartográfica e análise GIS, pode ser necessário criar pontos nos extremos de várias feições lineares selecionadas. Fazer isso manualmente e preencher os atributos individualmente aumenta o tempo de execução e pode introduzir inconsistências.

## ⚙️ Como funciona

O script em `src/extrair_pontos_extremos.py` automatiza o processo no ArcGIS Pro:

1. Localiza a camada configurada no mapa ativo e verifica se existem feições selecionadas.
2. Lê os extremos de cada feição linear selecionada.
3. Define **INICIO** no extremo de maior coordenada Y e **FIM** no extremo de menor coordenada Y.
4. Ordena as feições de Norte para Sul, usando X e o identificador da feição como critérios de desempate.
5. Cria uma feature class de pontos e registra coordenadas, identificadores e atributos selecionados da origem.
6. Gera as coordenadas geográficas em graus, minutos e segundos (DMS).

> **Escopo importante:** o script processa cada feição selecionada individualmente. Ele não agrupa segmentos conectados nem calcula a extensão total de uma rede.

## 🗂️ Campos de saída

| Campo | Finalidade |
|---|---|
| `PONTOS` | Identifica o ponto como INICIO ou FIM e o índice do trecho no processamento. |
| `X_COORD`, `Y_COORD` | Coordenadas do ponto no sistema de referência espacial da camada de entrada. |
| `ORIG_OID` | Identificador sequencial próprio, editável, atribuído aos pontos de saída. Não é o OID da feição de origem. |
| `LAT_DMS`, `LONG_DMS` | Latitude e longitude formatadas em graus, minutos e segundos. |
| Campos herdados | Copia os campos configurados em `INHERITED_FIELDS`, quando disponíveis na camada. |

## ▶️ Como usar

1. Abra o projeto no ArcGIS Pro.
2. Abra o script e ajuste `INPUT_LAYER_NAME`, `OUTPUT_GDB` e `OUTPUT_NAME`.
3. Confira os campos em `INHERITED_FIELDS` e ajuste-os conforme a sua camada.
4. No mapa ativo, selecione as feições que deseja processar na camada configurada.
5. Execute o script na janela Python do ArcGIS Pro.

Por segurança, `OVERWRITE_OUTPUT` está definido como `False`. Se a saída já existir, o script interrompe a execução sem apagá-la. Para substituir deliberadamente a saída, altere a opção para `True` após confirmar o nome e o destino.

**Atenção à orientação:** a regra Norte–Sul usa a coordenada Y do sistema de referência da camada. Antes de executar, confirme que essa regra corresponde ao sistema de coordenadas e ao resultado esperado para seus dados.

## 🛠️ Tecnologias

- Python
- ArcPy
- ArcGIS Pro
- Feature classes e atributos geográficos

## 🔒 Privacidade e dados

Este repositório contém código demonstrativo, sem dados operacionais, geometrias reais de redes, credenciais ou caminhos de diretórios corporativos. Os caminhos e o nome da camada devem ser configurados pelo usuário no próprio ambiente.

## 📌 Status

Versão inicial para portfólio. O script foi adaptado para publicação, mas deve ser testado no ambiente ArcGIS Pro do usuário antes de uso operacional. A biblioteca ArcPy depende da instalação/licença e do ambiente Python do ArcGIS Pro.

## 👤 Autor

**Daniel Neves**  
Engenheiro Ambiental | Analista GIS | Geoprocessamento

- GitHub: [@nevesdan](https://github.com/nevesdan)
