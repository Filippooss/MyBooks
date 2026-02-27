import base64
from typing import override


class Book:
    def __init__(
        self,
        id: int,
        title: str,
        author: str,
        publisher: str,
        release_year: int,
        description: str,
        image_raw: bytes,
    ) -> None:
        self.id: int = id
        self.title: str = title
        self.author: str = author
        self.publisher: str = publisher
        self.release_year: int = release_year
        self.description: str = description
        self.image_raw: bytes = image_raw

    # https://stackoverflow.com/questions/1436703/what-is-the-difference-between-str-and-repr
    @override
    def __repr__(self):
        return (
            f"Book(id={self.id}, title={self.title}, author={self.author}, "
            f"publisher={self.publisher}, release_year={self.release_year}, "
            f"description={self.description}, image={self.image_raw})"
        )

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "publisher": self.publisher,
            "release_year": self.release_year,
            "description": self.description,
            "image_raw": base64.b64encode(self.image_raw).decode("utf-8"),
        }


def from_json(json_data):
    image_raw = base64.b64decode(json_data["image_raw"])
    return Book(
        id=json_data["id"],
        title=json_data["title"],
        author=json_data["author"],
        publisher=json_data["publisher"],
        release_year=json_data["release_year"],
        description=json_data["description"],
        image_raw=image_raw,
    )
