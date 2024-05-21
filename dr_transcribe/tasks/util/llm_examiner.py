import evaluate

from dr_transcribe.tasks.util.examiner import BaseExaminor


class LLMExaminer(BaseExaminor):
    def __init__(
        self,
        model: str = "facebook/xglm-564M",
        token_limit: int = 512,
        min_threshold: int = 500,
        device: str = "cpu",
        batch_size: int = 4,
    ):
        super().__init__()

        self.model = model
        self.token_limit = token_limit
        self.min_threshold = min_threshold
        self.device = device
        self.batch_size = batch_size

        self.perplexity = evaluate.load("perplexity", module_type="metric")

    def examine(self, parsed_data: dict) -> float:
        transcript = self._get_transcript(parsed_data)

        if len(transcript) < 500:
            return 0

        chunks = self._chunk_text(transcript, chunk_size=512)
        score = self._score_text(chunks)

        return self._normalize_score(score)

    def _chunk_text(self, text: str, chunk_size: int = 512) -> list:
        chunks = []
        for i in range(0, len(text), chunk_size):
            chunks.append(text[i : i + chunk_size])
        return chunks

    def _score_text(self, chunks: str) -> float:
        results = self.perplexity.compute(
            model_id=self.model,
            add_start_token=False,
            predictions=chunks,
            device=self.device,
            batch_size=self.batch_size,
        )
        return results["mean_perplexity"]

    def _normalize_score(self, score: float) -> float:
        score = min(score, 100)
        score_in_range = 1 - ((score - 30) / 70)
        return round(score_in_range, 3)
