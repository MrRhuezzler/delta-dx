class Error:
    def __init__(self, typ, details) -> None:
        self.typ = typ
        self.details = details

    def __repr__(self) -> str:
        return f"{self.typ} : {self.details}"


class InvalidExpression(Error):
    def __init__(self, details) -> None:
        super().__init__("Invalid Expression", details)
