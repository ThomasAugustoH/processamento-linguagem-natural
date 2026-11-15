# GameMatch — Unidade 4

Aplicação web de recomendação de jogos com busca semântica no catálogo Backloggd. Os textos e metadados do CSV são usados como estão, sem um mapa manual de tradução.

## Executar

Requer Python 3.11 ou 3.12.

```bash
python -m venv .venv
```

Ative o ambiente virtual e instale as dependências:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Na primeira execução, o modelo multilíngue de embeddings será baixado e o índice local será criado em `.cache/`.

## Explicações com Gemini (opcional)

Sem chave, a aplicação ainda busca jogos e os apresenta por similaridade. Para habilitar as explicações do agente, configure `GOOGLE_API_KEY` antes de iniciar o Streamlit.

PowerShell:

```powershell
$env:GOOGLE_API_KEY = "sua-chave"
streamlit run app.py
```

Linux ou macOS:

```bash
export GOOGLE_API_KEY="sua-chave"
streamlit run app.py
```

O agente recebe os jogos recuperados pelo RAG e a aplicação valida os IDs retornados antes de exibi-los. A chave deve ficar em variável de ambiente, nunca no código.

## Arquivos

- `app.py`: interface Streamlit, filtros e histórico da sessão.
- `rag_engine.py`: leitura do catálogo, embeddings e busca semântica.
- `recommendation_agent.py`: agente opcional com validação e fallback para a busca.
- `jogos_nlp_completo.csv`: catálogo usado pela aplicação.
- `requirements.txt`: dependências necessárias para esta aplicação.
