from typing import override


class Rating:
    def __init__(self, id: int, value: int, comment: str, username: str) -> None:
        self.id: int = id
        self.value: int = value
        self.comment: str = comment
        self.username: str = username

    @override
    def __repr__(self):
        return (
            f"Rating(id={self.id}, value={self.value}, comment={self.comment}, "
            f"username={self.username})"
        )
