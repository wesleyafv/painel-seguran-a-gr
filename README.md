# 🛡️ Central de Inteligência de Riscos GR - Telemetria Logística

Conexão entre Engenharia de Dados e Segurança Patrimonial para detecção automática de áreas de risco e potenciais sinistros de carga (*Jamming* / Roubo de Carga).

## 🚀 Link do Projeto no Ar
👉 [CLIQUE AQUI PARA ACESSAR O PAINEL INTERATIVO](https://painelsegurancagr.streamlit.app)
<img width="1358" height="845" alt="image" src="https://github.com/user-attachments/assets/be6957d8-abc2-40e1-9fef-019691aba1d0" />


---

## 📝 O Problema de Negócio
No setor de transporte de cargas, a perda de sinal de um rastreador pode ser apenas uma oscilação comum da operadora celular (zona de sombra). No entanto, se o motorista acionar o **Botão de Pânico** em uma janela de tempo próxima à perda de sinal, a probabilidade de uma abordagem criminosa com o uso de bloqueadores de sinal (*jammers*) é altíssima.

Este projeto resolve essa dor correlacionando esses dois eventos de telemetria no tempo e no espaço para gerar inteligência de rotas e identificação de pontos críticos para gerenciadoras de risco (GR).

## 🛠️ Tecnologias Utilizadas
* **Banco de Dados:** MySQL (Estruturação relacional e consultas de alta performance).
* **Linguagem:** Python 3.13 (Manipulação e higienização dos dados).
* **Análise de Dados:** Pandas (Filtros, limpeza e Self-Join temporal).
* **Geolocalização:** Folium & Leaflet (Renderização de mapas e camadas espaciais interativas).
* **Interface Web:** Streamlit & Streamlit-Folium (Construção do dashboard de monitoramento).
* **Infraestrutura:** GitHub & Streamlit Community Cloud (Deploy, controle de versão e hospedagem).

---

## 🧠 Arquitetura da Solução e Lógica de Dados

1. **Extração de Alta Performance:** Modelagem de query SQL com `INNER JOIN` ligando a tabela histórica de movimentação (`viagens_regras_gr`) com a tabela de cadastro de tecnologias (`regras_gr`).
2. **Correlação Temporal de 30 Minutos:** Filtro lógico avançado para isolar linhas da mesma viagem onde o intervalo entre a perda de sinal e o acionamento do pânico fosse menor ou igual a 30 minutos, otimizando o processamento direto na fonte.
3. **Camada Visual Dupla:** * **Mapa de Calor (Heatmap):** Identificação visual das manchas térmicas nas rodovias onde ocorrem as maiores quedas de sinal sob estresse.
   * **Cluster de Marcadores:** Agrupamento inteligente de botões de pânico disparados, permitindo auditoria individualizada por ID de Viagem.

---

## 📊 Como Rodar o Projeto Localmente

Se quiser clonar e rodar o projeto na sua máquina, siga os passos abaixo no terminal:

1. **Clone o repositório:**
```bash
git clone https://github.com/wesleyafv/painel-seguran-a-gr.git
```

2. **Instale as dependências necessárias:**
```bash
pip install -r requirements.txt
```

3. **Execute o servidor do Streamlit:**
```bash
streamlit run app_seguranca.py
```
