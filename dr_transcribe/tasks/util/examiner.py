from io import StringIO


class BaseExaminor:
    def __init__(self) -> None:
        super()

    def examine(self, parsed_data: dict) -> float:
        raise NotImplementedError("Please Implement this method")

    def _chunk_text(self, text: str) -> list:
        raise NotImplementedError("Please Implement this method")

    def _score_text(self, chunk: str) -> float:
        raise NotImplementedError("Please Implement this method")

    def _normalize_score(self, score: float) -> float:
        raise NotImplementedError("Please Implement this method")

    def _get_transcript_with_speakers(self, parsed_data: dict) -> str:
        transcript = StringIO()
        segments = parsed_data["results"]["speaker_labels"]["segments"]
        for convo in segments:
            concatenated_content = StringIO()
            for item in convo["items"]:
                if item["content"] != "RESTRICTED":
                    concatenated_content.write(item["content"] + " ")
            if concatenated_content.tell() > 0:
                transcript.write(
                    f"{convo['speaker_label']}: {concatenated_content.getvalue()}",
                )
        return transcript.getvalue()

    def _get_transcript(self, parsed_data: dict):
        return parsed_data["results"]["transcripts"][0]["transcript"]
