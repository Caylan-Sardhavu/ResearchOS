import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


class ResearchNotebook:
    """
    Stores and searches completed ResearchOS investigations.

    The MVP uses a local JSON file so research history survives
    backend restarts. A vector database can replace this later.
    """

    def __init__(self) -> None:
        # Store notebook data beside this Python file.
        self.storage_path = Path(__file__).with_name("notebook_data.json")

        # Existing examples remain available to the Director's similarity search.
        self.seed_questions = [
            "What is CRISPR?",
            "Effects of climate change on agriculture",
            "Large language models in healthcare",
            "AMD GPU inference optimization with ROCm",
        ]

        self.stop_words = {
            "the",
            "a",
            "an",
            "and",
            "or",
            "in",
            "on",
            "for",
            "to",
            "of",
            "with",
            "using",
            "how",
            "what",
            "is",
            "are",
        }

        self._ensure_storage_exists()

    def _ensure_storage_exists(self) -> None:
        """
        Creates the notebook JSON file when it does not exist.
        """

        if not self.storage_path.exists():
            self.storage_path.write_text(
                json.dumps([], indent=2),
                encoding="utf-8",
            )

    def _load_entries(self) -> list[dict]:
        """
        Reads all saved notebook entries.
        """

        try:
            content = self.storage_path.read_text(encoding="utf-8")
            data = json.loads(content)

            if isinstance(data, list):
                return data

        except (OSError, json.JSONDecodeError):
            pass

        return []

    def _save_entries(self, entries: list[dict]) -> None:
        """
        Writes all notebook entries to local storage.
        """

        self.storage_path.write_text(
            json.dumps(entries, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def save_investigation(
        self,
        question: str,
        summary: str,
        research_gaps: list[str],
        selected_agents: list[str],
        paper_titles: list[str],
        report: str,
    ) -> dict:
        """
        Saves one completed research investigation.
        """

        entries = self._load_entries()

        entry = {
            "id": str(uuid4()),
            "question": question,
            "summary": summary,
            "research_gaps": research_gaps,
            "selected_agents": selected_agents,
            "paper_titles": paper_titles,
            "report": report,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        # Add the newest investigation first.
        entries.insert(0, entry)
        self._save_entries(entries)

        return entry

    def list_entries(self) -> list[dict]:
        """
        Returns all investigations, newest first.
        """

        return self._load_entries()

    def get_entry(self, entry_id: str) -> dict | None:
        """
        Returns one notebook entry by its unique ID.
        """

        for entry in self._load_entries():
            if entry.get("id") == entry_id:
                return entry

        return None

    def search(self, question: str) -> list[str]:
        """
        Finds previous questions with overlapping meaningful words.

        This preserves the interface already used by ResearchDirector.
        """

        matches: list[str] = []

        question_words = self._important_words(question)

        saved_questions = [
            entry.get("question", "")
            for entry in self._load_entries()
            if entry.get("question")
        ]

        all_questions = self.seed_questions + saved_questions

        for previous_question in all_questions:
            previous_words = self._important_words(previous_question)

            # A match requires at least two shared meaningful words.
            if len(question_words & previous_words) >= 2:
                if previous_question not in matches:
                    matches.append(previous_question)

        return matches[:5]

    def _important_words(self, text: str) -> set[str]:
        """
        Converts text into normalized keywords for basic similarity matching.
        """

        cleaned_text = (
            text.lower()
            .replace("?", "")
            .replace(".", "")
            .replace(",", "")
            .replace(":", "")
            .replace(";", "")
        )

        return {
            word
            for word in cleaned_text.split()
            if word not in self.stop_words and len(word) > 2
        }