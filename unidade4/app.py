from __future__ import annotations

import streamlit as st

from rag_engine import GameCatalog
from recommendation_agent import GameRecommendationAgent


st.set_page_config(
    page_title="GameMatch — Recomendador de Jogos",
    page_icon="🎮",
    layout="wide",
)


@st.cache_resource(show_spinner=False)
def load_catalog() -> GameCatalog:
    return GameCatalog()


@st.cache_resource(show_spinner=False)
def load_agent() -> GameRecommendationAgent:
    return GameRecommendationAgent()


if "game_history" not in st.session_state:
    st.session_state.game_history = []
if "latest_result" not in st.session_state:
    st.session_state.latest_result = None


st.title("🎮 GameMatch — Recomendador de Jogos")
st.write(
    "Descreva o tipo de jogo que procura. A aplicação busca títulos compatíveis no catálogo existente do Backloggd."
)
st.caption(
    "A busca usa os textos originais do catálogo. O score de similaridade ordena resultados e não representa uma probabilidade."
)

try:
    with st.spinner("Carregando o catálogo e o modelo de linguagem…"):
        catalog = load_catalog()
        agent = load_agent()
except Exception as exc:
    st.error(f"Não foi possível carregar o catálogo de jogos: {exc}")
    st.stop()


with st.sidebar:
    st.header("Filtros do catálogo")
    platform = st.selectbox("Plataforma", ["Todas"] + catalog.platforms)
    genre = st.selectbox("Tag / gênero", ["Todas"] + catalog.genres)
    min_rating = st.slider("Nota média mínima", 0.0, 5.0, 0.0, 0.5)
    year_from, year_to = st.slider(
        "Ano de lançamento",
        min_value=min(catalog.min_year, catalog.max_year),
        max_value=max(catalog.min_year, catalog.max_year),
        value=(min(catalog.min_year, catalog.max_year), max(catalog.min_year, catalog.max_year)),
    )
    top_k = st.slider("Quantidade de recomendações", 1, 5, 3)
    st.caption(f"{len(catalog.data)} jogos no catálogo local")
    if st.button("Limpar histórico da sessão", use_container_width=True):
        st.session_state.game_history = []
        st.session_state.latest_result = None


with st.form("game_search", clear_on_submit=False):
    query = st.text_input(
        "O que você procura?",
        placeholder="A story-rich open-world RPG with exploration",
    )
    submitted = st.form_submit_button("Buscar jogos", type="primary")

if submitted:
    if not query.strip():
        st.warning("Digite uma descrição para iniciar a busca.")
    else:
        previous_turns = st.session_state.game_history[-3:]
        with st.spinner("Buscando no catálogo e preparando as recomendações…"):
            candidates = catalog.search(
                query=query,
                top_k=top_k,
                platform=None if platform == "Todas" else platform,
                genre=None if genre == "Todas" else genre,
                min_rating=min_rating,
                year_from=year_from,
                year_to=year_to,
            )
            result = agent.recommend(query, candidates, history=previous_turns)

        st.session_state.latest_result = {"query": query, **result}
        st.session_state.game_history.append(
            {
                "query": query,
                "games": [game["name"] for game in result["recommendations"]],
                "summary": result["summary"],
            }
        )


def render_result(result: dict) -> None:
    st.markdown(f"**Busca:** {result['query']}")
    st.write(result["summary"])
    if result.get("notice"):
        st.info(result["notice"])
    if result.get("mode") == "agent":
        st.caption(f"Explicação gerada por {agent.model_name}; as recomendações ficam restritas aos jogos recuperados.")
    else:
        st.caption("Resultados apresentados pela ordem da busca semântica.")

    if not result["recommendations"]:
        st.info("Tente descrever a busca de forma mais ampla ou remova alguns filtros do catálogo.")
        return

    for position, game in enumerate(result["recommendations"], start=1):
        with st.container(border=True):
            year = game.get("year") or "ano não informado"
            rating = game.get("rating", 0.0)
            st.subheader(f"{position}. {game['name']} ({year})")
            st.write(game.get("reason", ""))
            st.caption(
                f"Tags: {game.get('tags') or 'N/D'} · Nota: {rating:.1f}/5 · "
                f"Similaridade: {game.get('similarity', 0.0):.3f}"
            )
            with st.expander("Detalhes do catálogo"):
                st.write(f"**Plataformas:** {game.get('platforms') or 'N/D'}")
                st.write(f"**Desenvolvedora / publicadora:** {game.get('developer') or 'N/D'}")
                st.write(f"**Tempo estimado de jogo:** {game.get('playtime') or 'N/D'}")
                st.write(game.get("description") or "Sem descrição no catálogo.")


if st.session_state.latest_result:
    st.subheader("Recomendações")
    render_result(st.session_state.latest_result)

if st.session_state.game_history:
    with st.expander("Buscas recentes nesta sessão"):
        for turn in reversed(st.session_state.game_history[-5:]):
            st.markdown(f"**{turn['query']}**")
            if turn["games"]:
                st.caption(" · ".join(turn["games"]))
            else:
                st.caption("Nenhum jogo correspondente")
