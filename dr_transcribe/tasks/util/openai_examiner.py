import json
from io import StringIO

from openai import Client

from dr_transcribe.tasks.util.examiner import BaseExaminor


class OpenAIExaminer(BaseExaminor):
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-3.5-turbo-1106",
        token_limit: int = 4096,
        seed: str = None,
        min_threshold: int = 500,
        timeout: int = 60,
    ):
        super().__init__()
        self.client = Client(api_key=api_key, timeout=timeout)
        self.model = model
        self.token_limit = token_limit
        self.seed = seed
        self.min_threshold = min_threshold

    def examine(self, parsed_data: dict) -> float:
        transcript = self._get_transcript_with_speakers(parsed_data)

        if len(transcript) < self.min_threshold:
            return 0

        chunks = self._chunk_text(transcript)
        score = self._score_text(chunks)
        return self._normalize_score(score)

    def _chunk_text(self, text: str, sentences_per_chunk: int = 50) -> list:
        sentences = text.split(".")
        total_sentences = len(sentences)

        if total_sentences <= min(sentences_per_chunk * 5, 100):
            return [text]

        chunk_count = 5
        chunk_size = total_sentences // chunk_count
        chunks = []
        for i in range(chunk_count):
            chunk = StringIO()
            start = i * chunk_size
            j = start
            end = min(start + sentences_per_chunk, len(sentences))
            while chunk.tell() < self.token_limit / 2 and j < end:
                chunk.write(sentences[j])
                j += 1
            chunks.append(chunk.getvalue())
        return chunks

    def _score_text(self, chunks: list[str]) -> float:
        score = 0

        for chunk in chunks:
            print(f"Sending a chunk to OpenAI, chunk size: {len(chunk)} tokens")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        # noqa: E501
                        "content": f"""
                Please read the following piece of text from a meeting transcript and rawte its coherence. Rating is on a scale from 1 to 100, where 1 indicates that the sentence is completely incoherent and makes no sense, and 100 indicates that the sentence is perfectly coherent and clearly understandable. When rating coherence, consider factors such as grammar, valid vocabulary, semantic meaning, logical and conversational flow. If context is necessary and not provided, use your general world knowledge to infer the most likely context where applicable.
                Each speaker is denoted by the unique identifier 'spk_*:', that prepends what they said at any given moment. Before you've given your rating, please provide a step-by-step justification for your assessment, explaining which aspects of the sentence contributed to its coherence or lack thereof. This is very important for my career. I know you can handle this challenge.

                Expected Output format is json with the following fields:
                - "justification": a string of text explaining your rating
                - "rating": a number from 1 to 100, inclusive, indicating your rating of the coherence of the text

                Text to Evaluate: "{chunk}"
                                    """,
                    },
                ],
                response_format={"type": "json_object"},
                top_p=1,
                seed=self.seed,
            )

            raw_json = response.choices[0].message.content

            try:
                json_data = json.loads(raw_json)
                score += json_data["rating"]
            except Exception as e:
                print("Failed to parse response from OpenAI as json" + e)

        return score / len(chunks)

    def _normalize_score(self, score: float) -> float:
        return round(score / 100, 3)
