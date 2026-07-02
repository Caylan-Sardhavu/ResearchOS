class ResearchNotebook:
    """
    Very simple notebook for MVP.

    Later this will use embeddings and semantic search.
    """

    def __init__(self):
        self.previous_questions = [
            "What is CRISPR?",
            "Effects of climate change on agriculture",
            "Large language models in healthcare",
            "AMD GPU inference optimization with ROCm",
        ]

        self.stop_words = {
            "the", "a", "an", "and", "or", "in", "on", "for", "to",
            "of", "with", "using", "how", "what", "is", "are"
        }

    def search(self, question: str) -> list[str]:
        matches = []

        question_words = {
            word.strip(".,?!").lower()
            for word in question.split()
            if word.strip(".,?!").lower() not in self.stop_words
        }

        for previous in self.previous_questions:
            previous_words = {
                word.strip(".,?!").lower()
                for word in previous.split()
                if word.strip(".,?!").lower() not in self.stop_words
            }

            shared_words = question_words.intersection(previous_words)

            if len(shared_words) >= 2:
                matches.append(previous)

        return matches