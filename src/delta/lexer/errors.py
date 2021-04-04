class Error(Exception):
    def __init__(self, typ, start_pos, end_pos, details) -> None:
        self.typ = typ
        self.details = details
        self.start_pos = start_pos
        self.end_pos = end_pos
    
    def __repr__(self) -> str:
        return f"{self.typ} : {self.details} ({self.start_pos.idx}, {self.end_pos.idx})"


class InvalidIdentifier(Error):
    def __init__(self, start_pos, end_pos, details) -> None:
        super().__init__("Invalid Identifier", start_pos, end_pos, details)
