"""Local semantic retrieval over the existing Backloggd game catalog."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer


ROOT = Path(__file__).resolve().parent
DEFAULT_DATA_PATH = ROOT / "jogos_nlp_completo.csv"
DEFAULT_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def _text(value: Any) -> str:
    if value is None or pd.isna(value):
        return ""
    return str(value).strip()


class GameCatalog:
    """Loads game metadata and retrieves matching records with cosine similarity."""

    def __init__(
        self,
        data_path: str | Path = DEFAULT_DATA_PATH,
        model_name: str = DEFAULT_MODEL_NAME,
    ) -> None:
        self.data_path = Path(data_path)
        self.model_name = model_name
        self.data = pd.read_csv(self.data_path)

        if "Nome" not in self.data.columns or "Descricao" not in self.data.columns:
            raise ValueError("O CSV precisa conter as colunas 'Nome' e 'Descricao'.")
        if self.data.empty:
            raise ValueError("O catálogo de jogos está vazio.")

        for column in (
            "Nome",
            "Descricao",
            "Tags",
            "Plataformas",
            "Desenvolvedora/Publisher",
            "Tempo de Jogo",
        ):
            if column not in self.data.columns:
                self.data[column] = ""
            self.data[column] = self.data[column].map(_text)

        if "Nota Média" in self.data.columns:
            self.data["Nota Média"] = pd.to_numeric(
                self.data["Nota Média"], errors="coerce"
            ).fillna(0.0)
        else:
            self.data["Nota Média"] = 0.0

        year_column = "Lançamento" if "Lançamento" in self.data.columns else "Lanamento"
        if year_column in self.data.columns:
            self.data["_year"] = pd.to_numeric(
                self.data[year_column].astype(str).str.extract(r"(\d{4})")[0],
                errors="coerce",
            )
        else:
            self.data["_year"] = np.nan

        self.model = SentenceTransformer(self.model_name)
        self.documents = [self._document_text(row) for _, row in self.data.iterrows()]
        self.embeddings = self._load_or_build_embeddings()
        self.platforms = self._unique_values("Plataformas")
        self.genres = self._unique_values("Tags")
        known_years = self.data["_year"].dropna()
        self.min_year = int(known_years.min()) if not known_years.empty else 1980
        self.max_year = int(known_years.max()) if not known_years.empty else 2030

    @staticmethod
    def _document_text(row: pd.Series) -> str:
        """Use the catalog's original text and metadata without manual translation."""
        fields = (
            ("Title", row.get("Nome", "")),
            ("Tags", row.get("Tags", "")),
            ("Description", row.get("Descricao", "")),
            ("Developer", row.get("Desenvolvedora/Publisher", "")),
            ("Platforms", row.get("Plataformas", "")),
        )
        return "\n".join(f"{label}: {_text(value)}" for label, value in fields if _text(value))

    def _cache_path(self) -> Path:
        digest = hashlib.sha256()
        digest.update(self.model_name.encode("utf-8"))
        digest.update(self.data_path.read_bytes())
        return ROOT / ".cache" / f"game_embeddings_{digest.hexdigest()[:20]}.npy"

    def _load_or_build_embeddings(self) -> np.ndarray:
        cache_path = self._cache_path()
        if cache_path.exists():
            cached = np.load(cache_path, allow_pickle=False)
            if cached.ndim == 2 and cached.shape[0] == len(self.documents):
                return cached.astype(np.float32, copy=False)

        vectors = self.model.encode(
            self.documents,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=True,
        ).astype(np.float32, copy=False)
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        np.save(cache_path, vectors)
        return vectors

    def _unique_values(self, column: str) -> list[str]:
        values: set[str] = set()
        for value in self.data[column]:
            values.update(part.strip() for part in _text(value).split(",") if part.strip())
        return sorted(values, key=str.casefold)

    def search(
        self,
        query: str,
        top_k: int = 5,
        platform: str | None = None,
        genre: str | None = None,
        min_rating: float = 0.0,
        year_from: int | None = None,
        year_to: int | None = None,
    ) -> list[dict[str, Any]]:
        query = query.strip()
        if not query:
            return []
        if top_k < 1:
            return []

        query_vector = self.model.encode(
            [query], normalize_embeddings=True, convert_to_numpy=True
        )[0]
        scores = self.embeddings @ query_vector
        matches: list[dict[str, Any]] = []

        for index, score in enumerate(scores):
            row = self.data.iloc[index]
            platforms = [part.strip() for part in _text(row["Plataformas"]).split(",")]
            genres = [part.strip() for part in _text(row["Tags"]).split(",")]
            rating = float(row["Nota Média"])
            year_value = row["_year"]
            year = int(year_value) if pd.notna(year_value) else None

            if platform and platform not in platforms:
                continue
            if genre and genre not in genres:
                continue
            if rating < min_rating:
                continue
            if year_from is not None and year is not None and year < year_from:
                continue
            if year_to is not None and year is not None and year > year_to:
                continue

            source_id = _text(row.get("Posicao", index + 1)) or str(index + 1)
            matches.append(
                {
                    "id": source_id,
                    "name": _text(row["Nome"]),
                    "year": year,
                    "tags": _text(row["Tags"]),
                    "platforms": _text(row["Plataformas"]),
                    "developer": _text(row["Desenvolvedora/Publisher"]),
                    "rating": rating,
                    "playtime": _text(row["Tempo de Jogo"]),
                    "description": _text(row["Descricao"]),
                    "similarity": float(score),
                }
            )

        matches.sort(key=lambda game: game["similarity"], reverse=True)
        return matches[:top_k]
