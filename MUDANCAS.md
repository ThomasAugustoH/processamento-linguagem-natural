# Mudanças entre a versão original e a atual

**Referência "original":** commit `9d211e8` ("feat: up dos codigos do professor").
**Comparação:** código e texto de cada célula, ignorando saídas e quebras de linha. O `git diff` bruto mostra centenas de milhares de linhas só por causa das saídas gravadas e do CRLF.

## Resumo

| Notebook | Células antes → depois | Tamanho da mudança |
|---|---|---|
| `Aula_6.ipynb` | 35 → 35 | Pequena (2 células) |
| `Aula_7_Word2Vec_BERT.ipynb` | 27 → 27 | Pequena (4 células) |
| `Aula_8_Classificação_de_textos.ipynb` | 43 → 21 | Reescrito |
| `Aula_8_Teste_Jev.ipynb` | 51 → 27 | Reescrito |

Fora dos notebooks, foi criado o ambiente `.venv312/`, que não é versionado.

---

## Aula_6

1. **Escolha de `k` no K-Means (célula 15)**
   - Antes: `k = 3` fixo, com texto dizendo "k = 14" e "seis categorias".
   - Agora: testa `k` de 2 a 12 e escolhe o de maior **coeficiente de silhueta** (distância do cosseno). Imprime a silhueta por `k` e o `k` escolhido.
   - O texto em markdown foi ajustado para dizer isso.
2. **Célula 30 (distância entre centroides)**
   - Antes: tinha código de carregamento do CSV, repetido e fora de lugar.
   - Agora: calcula `distancia_centroides = cosine_distances(kmeans.cluster_centers_)`.
   - Isso corrigiu o `NameError: distancia_centroides is not defined` da célula seguinte.

## Aula_7 (Word2Vec e BERT)

1. **Célula 1:** acrescentou `import sys; print(sys.executable)`, para mostrar qual Python o kernel usa.
2. **Célula 3:** criou a coluna `descricao_original` (`df["Descricao"]`), com o texto sem processamento.
3. **Célula 11:** trocou o modelo.
   - Antes: `bert-base-uncased`.
   - Agora: `sentence-transformers/all-MiniLM-L6-v2`.
   - Motivo: com o BERT puro, os mesmos jogos apareciam para qualquer consulta.
4. **Célula 13:** os embeddings do BERT agora usam `descricao_original`, e não os tokens sem stopwords.
   - Antes: `df["descricao"]`.
   - Agora: `df["descricao_original"]`.
   - Motivo: modelos contextuais devem receber a frase completa. Isso já era o que o próprio texto do notebook dizia.

> O texto em markdown ainda diz "BERTimbau" e "português", mas o código usa um modelo em inglês.

## Aula_8 — Classificação de textos (reescrito)

| | Antes | Agora |
|---|---|---|
| Dados | Avaliações de produtos B2W-Reviews01, em português, baixadas da web | `jogos_nlp_completo.csv`, descrições de jogos em inglês |
| Tarefa | Binária (recomenda ou não) e multiclasse (1 a 5 estrelas) | **Multirrótulo**: prever os gêneros/tags de cada jogo |
| Texto | `review_text` bruto | Texto original e **lematizado** (coluna `lemas`) |
| Modelo | TF-IDF + Regressão Logística, com um único split treino/teste | Compara BoW, TF-IDF, LogReg e LinearSVC com `OneVsRestClassifier` e `class_weight="balanced"` |
| Avaliação | Acurácia, matriz de confusão | **Validação cruzada** repetida, F1 micro e macro, `GridSearchCV`, **limiar por gênero**, matriz de confusão por gênero |
| Extras | Coeficientes, erros, frases novas | Termos mais associados por gênero e teste com descrições novas (pré-processamento igual ao do corpus) |

Só ficam os gêneros com pelo menos 10 jogos.

## Aula_8 — Teste Jev (reescrito)

- Antes: avaliava o Jev no corpus B2W com duas perguntas, **Noul** para recomendar e **Score** para estrelas de 1 a 5, medindo acurácia, MAE e ROC AUC.
- Agora: usa o CSV de jogos. Faz **uma pergunta Noul por gênero**, todas numa única chamada por jogo.
- A amostra é de 25 jogos (`N_AMOSTRA`), com F1 micro e macro, ROC AUC, limiar fixo de 0,5 e depois limiar por gênero.
- Salva as probabilidades em `resultados_jev_jogos.csv`.
- Mantém a chave em `getpass`, sem gravar no notebook.

## Ambiente

- O `.venv` original usa **Python 3.15**, que não tem pacote do gensim e não consegue compilá-lo.
- Foi criado o **`.venv312`** (Python 3.12) com gensim, nltk, nbformat, ipykernel, pandas, numpy, scikit-learn, plotly, matplotlib, seaborn e tabulate.
- Os notebooks devem rodar com o kernel `.venv312`.
- Pacotes instalados com `pip install` fora do `.venv312` vão para o Python global e não aparecem no notebook.

## O que eu mesmo alterei

Nesta conversa eu editei **apenas** a linha `MODELO_BERT` da Aula_7, que é o item 3 da seção da Aula_7. Também instalei pacotes e criei o `.venv312`.

As demais mudanças já estavam nos arquivos quando comparei com o commit. Elas vieram de edições suas ou de outras ferramentas, e o diff não diz quem fez cada uma.

## Pendências sugeridas

- Atualizar os textos que ainda dizem "BERTimbau" na Aula_7.
- Adicionar um `requirements.txt` e documentar que o projeto precisa de Python 3.12.
- Fazer o commit das mudanças. Hoje elas estão só no diretório de trabalho.
