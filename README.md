# 📊 Medical Insurance Cost Dashboard

🇧🇷 Português · [🇺🇸 English](./README.en.md)

Interactive data analysis and visualization project built with **Python, Pandas, Matplotlib, Seaborn and Streamlit** to explore the factors associated with medical insurance costs.

## 🎯 Sobre o projeto

Este projeto analisa um conjunto de dados de seguros de saúde para investigar como características demográficas e comportamentais estão relacionadas aos custos médicos.

A análise explora principalmente:

* idade;
* índice de massa corporal (BMI);
* tabagismo;
* região;
* número de dependentes;
* custos do seguro.

O objetivo é transformar os dados em **visualizações e insights que facilitem a compreensão dos principais fatores associados aos custos de saúde**.

## 📊 Principais análises

* Comparação dos custos entre fumantes e não fumantes;
* Relação entre BMI e custos do seguro;
* Impacto da idade nos custos;
* Comparação de custos entre regiões;
* Análise de indicadores e distribuições dos dados;
* Exploração interativa utilizando filtros e visualizações.

## 🛠️ Tecnologias

* **Python**
* **Pandas**
* **Streamlit**
* **Matplotlib**
* **Seaborn**

## 📁 Estrutura do projeto

```text
medicalcost_dashboard/
│
├── app.py
├── requirements.txt
├── .gitignore
├── .devcontainer/
└── README.md
```

## ▶️ Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/warleyroma/medicalcost_dashboard.git
cd medicalcost_dashboard
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Execute o dashboard

```bash
streamlit run app.py
```

O Streamlit disponibilizará o dashboard localmente no navegador.

## 📂 Dataset

O projeto utiliza o dataset público **Medical Cost Personal Datasets**, disponibilizado no Kaggle.

Fonte:

[Medical Cost Personal Datasets — Kaggle](https://www.kaggle.com/datasets/mirichoi0218/insurance)

## 🔎 Principais perguntas exploradas

* Fumantes apresentam custos médicos significativamente maiores?
* Como os custos variam conforme a idade?
* Existe relação entre BMI e despesas médicas?
* Existem diferenças relevantes entre regiões?
* Quais características estão mais associadas aos maiores custos?

## ⚠️ Observação

Este projeto tem finalidade **educacional e analítica**. As relações observadas nos dados não devem ser interpretadas automaticamente como relações causais.

## 🚀 Próximos passos

* [ ] Adicionar demonstração online do dashboard
* [ ] Melhorar a experiência visual e interativa
* [ ] Adicionar análise estatística mais aprofundada
* [ ] Explorar correlações entre as variáveis
* [ ] Implementar um modelo preditivo de custos
* [ ] Adicionar testes automatizados
* [ ] Criar pipeline de deploy

---

### 👤 Autor

**Warley Roma**

Data Analyst | Data Scientist | AI

[GitHub](https://github.com/warleyroma)
