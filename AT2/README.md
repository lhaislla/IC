# Dashboard Interativo: Análise de Trajetórias Acadêmicas (INEP 2010-2024)

Este projeto foi desenvolvido como parte da atividade de **Visualização de Dados Interativa**. O objetivo é explorar e comunicar insights sobre indicadores de fluxo do ensino superior brasileiro (Evasão, Retenção, Conclusão e Permanência) através de uma interface interativa e dinâmica.

## 🚀 Tecnologias Utilizadas
* **Linguagem:** Python 3.10+
* **Dashboard:** [Streamlit](https://streamlit.io/)
* **Visualização:** [Plotly Express](https://plotly.com/python/plotly-express/) (Mapas Coropléticos e Gráficos de Barras)
* **Manipulação de Dados:** Pandas e Openpyxl
* **Fonte de Dados:** Microdados e Indicadores de Fluxo do INEP (2010-2024)

```text



## 📂 Estrutura do Projeto

AT2/
├── data/
│   └── INDIC_BRASIL_2010_2024.xlsx   # Base de dados original (Excel)
├── pages/
│   └── dashboard.py               # Script principal da aplicação
└── requirements.txt               # Lista de dependências e versões


```
## ⚙️ Pré-requisitos

* Python 3.10 ou superior
* pip (gerenciador de pacotes)

---

## 🚀 Configuração do Ambiente

### 1. Criar o ambiente virtual

No diretório raiz do projeto:

```bash
python -m venv venv
```
---

### 2. Ativar o ambiente virtual

#### Windows (PowerShell):

```bash
venv\Scripts\activate
```

#### Linux / Mac:

```bash
source venv/bin/activate
```

---

### 3. Instalar dependências (IMPORTANTE)

Este projeto depende de bibliotecas especificadas no arquivo `requirements.txt`.

Execute:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## ▶️ Execução da Aplicação

Após instalar as dependências, execute:

```bash

streamlit run dashboard.py
```

---