from typing import Any


class g(list):
    def __init__(self):
        self.v = 1

    def __len__(self) -> int:
        return super().__len__()
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return super().__call__(*args, **kwds)

t = g()
t.append(1)
print(t.__len__())