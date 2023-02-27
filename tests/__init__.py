import pytest
from typing import Callable, Dict


def parametrize_with_names(arguments: str, named_values: Dict, **kwargs) -> Callable:
    names, values = zip(*sorted(named_values.items()))
    return pytest.mark.parametrize(arguments, values, ids=names, **kwargs)
