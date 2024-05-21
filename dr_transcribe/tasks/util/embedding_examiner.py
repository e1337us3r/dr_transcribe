from sentence_transformers import SentenceTransformer, util

from dr_transcribe.tasks.util.examiner import BaseExaminor


class EmbeddingExaminer(BaseExaminor):
    def __init__(
        self,
        model: str = "distiluse-base-multilingual-cased-v2",
        token_limit: int = 512,
        chunk_size: int = 150,
        min_threshold: int = 500,
    ):
        super().__init__()
        self.model = model
        self.token_limit = token_limit
        self.chunk_size = chunk_size
        self.min_threshold = min_threshold
        self.model = SentenceTransformer(model, cache_folder=".models")

    def examine(self, parsed_data: dict) -> float:
        transcript = self._get_transcript(parsed_data)

        if len(transcript) < 500:
            return 0

        chunks = self._chunk_text(transcript, self.chunk_size)
        embeddings = self._get_embedding(chunks)
        similarities = self._score_text(embeddings)

        mean = float(sum(similarities) / len(similarities))

        return self._normalize_score(mean)

    def _get_embedding(self, text: str) -> list:
        return self.model.encode(text, normalize_embeddings=True)

    def _chunk_text(self, text: str, chunk_size=150) -> list:
        chunks = []
        for i in range(0, len(text), chunk_size):
            chunks.append(text[i : i + chunk_size])
        return chunks

    def _score_text(self, embedding: str) -> list[float]:
        return [
            util.cos_sim(embedding[i - 1], embedding[i])
            for i in range(1, len(embedding), 1)
        ]

    def _normalize_score(self, score: float) -> float:
        score = min(score, 0.5)
        return round(score * 2, 3)
