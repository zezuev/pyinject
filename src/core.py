import inspect
from enum import Enum
from typing import Any


class Strategy(Enum):
    SINGLETON = 1
    FACTORY = 2


type Dependecy = tuple[str, type]


_DEPENDENCIES: dict[type, set[Dependecy]] = {}
_STRATEGIES: dict[type, Strategy] = {}
_COMPONENTS: dict[type, Any] = {}


def _get_component[T](t: type[T]) -> T:
    if component := _COMPONENTS.get(t):
        return component

    inject = {
        name: _get_component(dependency)
        for name, dependency in _DEPENDENCIES[t]
    }
    component = t(**inject)

    if _STRATEGIES.get(t, Strategy.SINGLETON) == Strategy.SINGLETON:
        _COMPONENTS[t] = component
    return component


def _get_topological_sorting() -> list[type]:
    sorting: list[type] = []

    def dfs(t: type):
        if t in sorting:
            return
        for (_, dependency) in _DEPENDENCIES.get(t, set()):
            dfs(dependency)
        sorting.append(t)

    for x in _DEPENDENCIES:
        dfs(x)

    return sorting


def Component[T](t: type[T]) -> type[T]:
    dependencies = inspect.get_annotations(t.__init__)
    _DEPENDENCIES[t] = set(dependencies.items())
    return t


def Singleton[T](t: type[T]) -> type[T]:
    if t in _STRATEGIES:
        raise TypeError("Cannot use multiple strategies for a single component.")

    _STRATEGIES[t] = Strategy.SINGLETON
    return t


def Factory[T](t: type[T]) -> type[T]:
    if t in _STRATEGIES:
        raise TypeError("Cannot use multiple strategies for a single component.")

    _STRATEGIES[t] = Strategy.FACTORY
    return t


def create_components() -> dict[type, Any]:
    sorting = _get_topological_sorting()
    return {t: _get_component(t) for t in sorting}