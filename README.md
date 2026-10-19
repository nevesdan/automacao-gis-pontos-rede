# Automação GIS: Extração de Pontos Extremos de Rede

Automação de uma etapa de processamento geoespacial no **ArcGIS Pro**, utilizando **Python e ArcPy** para identificar os pontos extremos de trechos conectados de uma rede e consolidar informações úteis para análise e atualização de dados geográficos.

## 🎯 Objetivo

Reduzir o trabalho manual envolvido na identificação dos extremos de segmentos conectados, permitindo organizar os resultados de forma mais consistente e apoiar rotinas de análise GIS.

## 🧩 O problema

Em bases lineares, um mesmo trecho pode estar representado por vários segmentos conectados. Para determinados levantamentos, é necessário identificar apenas o início e o fim do conjunto conectado e considerar a extensão total formada pelos segmentos.

Realizar essa conferência manualmente pode consumir tempo e aumentar o risco de inconsistências.

## ⚙️ Abordagem

A proposta utiliza Python com ArcPy, dentro do ambiente do ArcGIS Pro, para automatizar etapas do processamento espacial e da organização dos resultados.

O fluxo de trabalho é direcionado a:

- trabalhar com feições lineares disponíveis em uma camada GIS;
- identificar segmentos que pertencem a um mesmo trecho conectado;
- obter os pontos extremos do trecho resultante;
- consolidar a extensão dos segmentos relacionados, quando aplicável;
- organizar os resultados para uso em análises e planilhas de apoio.

> A lógica deve ser executada e validada com os dados e as regras do projeto antes de ser utilizada em produção. Este repositório não inclui dados operacionais ou geometrias reais de redes.

## 🛠️ Tecnologias

- **Python**
- **ArcPy**
- **ArcGIS Pro**
- **Dados vetoriais e análise de conectividade**

## 🔒 Privacidade e dados

O projeto é apresentado com foco técnico e demonstrativo. Não são publicados caminhos internos, dados corporativos, geometrias operacionais, credenciais ou informações confidenciais.

## 📌 Status

Projeto de portfólio GIS. O código-fonte final será disponibilizado após revisão e validação para publicação, acompanhado de exemplos demonstrativos que não exponham dados confidenciais.

## 👤 Autor

**Daniel Neves**  
Engenheiro Ambiental | Geoprocessamento e Automação GIS

- GitHub: [@nevesdan](https://github.com/nevesdan)
