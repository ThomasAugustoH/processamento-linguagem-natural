# Processamento de Linguagem Natural (PLN)

Repositório com implementações, análises e atividades práticas de Processamento de Linguagem Natural.

---

## 📌 Pré-requisitos

- **Python 3.11 ou 3.12** (Recomendado: **Python 3.12**)
  > ⚠️ **Importante:** Versões muito recentes do Python (como Python 3.13+) podem apresentar problemas ao compilar bibliotecas C/C++ como `gensim`.

---

## 🚀 Guia de Instalação e Configuração

### 1. Clonar o repositório
```bash
git clone https://github.com/ThomasAugustoH/processamento-linguagem-natural.git
cd processamento-linguagem-natural
```

### 2. Criar o Ambiente Virtual (`.venv`)

- **Windows (PowerShell ou Prompt de Comando):**
  ```powershell
  python -m venv .venv
  ```

- **Linux / macOS:**
  ```bash
  python3 -m venv .venv
  ```

---

### 3. Ativar o Ambiente Virtual

- **Windows (PowerShell):**
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
  *(Se encontrar erro de política de execução no PowerShell, rode antes: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)*

- **Windows (CMD):**
  ```cmd
  .\.venv\Scripts\activate.bat
  ```

- **Linux / macOS:**
  ```bash
  source .venv/bin/activate
  ```

---

### 4. Atualizar o `pip` e Instalar as Dependências

Com o ambiente ativado, execute:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

### 5. Recursos Adicionais do NLTK

Alguns notebooks utilizam tokenizadores, stopwords e lematizadores do NLTK. Baixe os recursos necessários executando o comando abaixo:

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords'); nltk.download('wordnet')"
```

---

### 6. Configurar o Kernel no Jupyter Notebook / VS Code

Para garantir que o Jupyter reconheça o kernel do seu ambiente virtual `.venv`:

```bash
python -m ipykernel install --user --name=pln-venv --display-name "Python 3.12 (PLN)"
```

Ao abrir os notebooks (`.ipynb`) no VS Code ou Jupyter Lab, selecione o kernel **Python 3.12 (PLN)** ou aponte diretamente para o executável em `.venv/Scripts/python.exe`.

---

## 📂 Conteúdo do Repositório

- **`Aula_6.ipynb`**: Clusterização de textos (K-Means, TF-IDF, Silhueta, Distância de Cosseno).
- **`Aula_7_Word2Vec_BERT.ipynb`**: Embeddings com Word2Vec e modelos pré-treinados Transformer (BERT / MiniLM).
- **`Aula_8_Classificação_de_textos.ipynb`**: Classificação de textos multirrótulo com TF-IDF, Bag-of-Words, Regressão Logística e LinearSVC.
- **`Aula_8_Teste_Jev.ipynb`**: Avaliação de LLM / inferência via API TypeSafe (Noul).
- **`scraper.ipynb`**: Extração de dados da plataforma Backloggd.
- **`jogos_nlp_completo.csv`** e **`top_jogos_backloggd.csv`**: Datasets utilizados nos experimentos.