class SearchResult:
    def __init__(self):
        self.full_word_matches = []
        self.partial_matches = []
        self.character_matches = []

    def add_full_word_match(self, index):
        self.full_word_matches.append(index)

    def add_partial_match(self, index):
        self.partial_matches.append(index)

    def add_character_match(self, index):
        self.character_matches.append(index)

    def to_dict(self):
        return {
            "full_word_matches": self.full_word_matches,
            "partial_matches": self.partial_matches,
            "character_matches": self.character_matches,
        }