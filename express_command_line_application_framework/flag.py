from typing import List, Optional

class Flag:

    def __init__(
        self,
        keys: List[str],
        description: str,
        required: bool = False,
    ):
        self.keys: List[str] = keys
        self.description: str = description
        self.required: bool = required