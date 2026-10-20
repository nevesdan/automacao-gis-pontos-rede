# Automação GIS: Extração de Pontos Extremos de Rede

Projeto de automação geoespacial com **Python, ArcPy e ArcGIS Pro** para extrair os extremos das feições lineares selecionadas, padronizar a orientação dos pontos e organizar atributos para análise e edição.

## 🎯 Objetivo

Reduzir etapas manuais na criação de pontos de início e fim de trechos lineares, mantendo atributos relevantes da camada de origem e disponibilizando coordenadas em formatos úteis para conferência. O script foi testado e utilizado em uma rotina real para apoiar a produção do **Mapa de Avanço referente ao mês de setembro de 2026**, automatizando a extração dos pontos extremos dos trechos selecionados.

## 🧩 O problema

Em rotinas de produção cartográfica e análise GIS, pode ser necessário criar pontos nos extremos de várias feições lineares selecionadas. Fazer isso manualmente e preencher os atributos individualmente aumenta o tempo de execução e pode introduzir inconsistências.

## ⚙️ Como funciona

O script em [`src/extrair_pontos_extremos.py`](src/extrair_pontos_extremos.py) automatiza o processo no ArcGIS Pro:

1. Localiza no mapa ativo a camada cuja fonte corresponde ao caminho configurado em `INPUT_FC` e verifica se existem feições selecionadas.
2. Lê os extremos de cada feição linear selecionada.
3. Define **INICIO** no extremo de maior coordenada Y e **FIM** no extremo de menor coordenada Y.
4. Ordena as feições de Norte para Sul, usando X e o identificador da feição como critérios de desempate.
5. Cria uma feature class de pontos e registra coordenadas, identificadores e atributos selecionados da origem.
6. Gera as coordenadas geográficas em graus, minutos e segundos (DMS).

> **Escopo importante:** o script processa cada feição selecionada individualmente. Ele não agrupa segmentos conectados nem calcula a extensão total de uma rede.

## 🖼️ Demonstração visual

As imagens abaixo documentam o projeto e o fluxo de trabalho no ArcGIS Pro.

### Capturas do projeto

| Imagem | Visualização |
|---|---|
| **1. Captura inicial** | ![Captura inicial do projeto](Captura%20de%20tela%202026-10-19%20170904.png) |
| **2. Captura do fluxo de trabalho** | ![Captura do fluxo de trabalho](Captura%20de%20tela%202026-10-19%20171014.png) |
| **3. Captura do processamento** | ![Captura do processamento](Captura%20de%20tela%202026-10-19%20171041.png) |
| **4. Captura dos resultados** | ![Captura dos resultados](Captura%20de%20tela%202026-10-19%20171102.png) |
| **5. Captura dos atributos** | ![Captura dos atributos](Captura%20de%20tela%202026-10-19%20171125.png) |

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
2. O script foi configurado com os caminhos e nomes usados no projeto original: `INPUT_FC` aponta para `RedeGasCigas2.shp`, `OUTPUT_GDB` para `Setembro2026.gdb` e `OUTPUT_NAME` está definido como `CT059_Pontos`. Se for usar em outro computador ou projeto, ajuste esses caminhos para os locais existentes no seu ambiente.
3. Confira os campos em `INHERITED_FIELDS` e ajuste-os conforme a sua camada.
4. No mapa ativo, selecione as feições que deseja processar na camada configurada.
5. Execute o script na janela Python do ArcGIS Pro.

**Atenção: sobrescrita da saída.** Se a feature class definida em `OUTPUT_NAME` já existir dentro de `OUTPUT_GDB`, o script a apaga e cria uma nova. Confira o caminho e o nome de saída antes de executar, especialmente se houver dados que deseja preservar.

**Atenção à orientação:** a regra Norte–Sul usa a coordenada Y do sistema de referência da camada. Antes de executar, confirme que essa regra corresponde ao sistema de coordenadas e ao resultado esperado para seus dados.

## 🛠️ Tecnologias

- Python
- ArcPy
- ArcGIS Pro
- Feature classes e atributos geográficos

## 🔒 Privacidade e dados

Este repositório publica os caminhos de configuração utilizados no projeto original, inclusive o nome da geodatabase `Setembro2026.gdb`. Os caminhos são referências locais e não concedem acesso ao computador ou aos arquivos por si só. O repositório não inclui a geodatabase nem os dados operacionais; para executar em outro ambiente, ajuste `INPUT_FC` e `OUTPUT_GDB`.

## 📌 Status

Script baseado no código original, testado e utilizado para resolver uma necessidade prática: agilizar a criação dos pontos extremos necessários à elaboração do Mapa de Avanço de setembro de 2026. O processamento depende do ArcPy, do ArcGIS Pro e dos dados locais do projeto. Para reutilizá-lo em outro ambiente, ajuste os caminhos e valide os resultados. A biblioteca ArcPy depende da instalação/licença e do ambiente Python do ArcGIS Pro.

## 👤 Autor

**Daniel Neves**  
Engenheiro Ambiental | Analista GIS | Geoprocessamento

- GitHub: [@nevesdan](https://github.com/nevesdan)
