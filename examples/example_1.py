from src.core import Component, Factory, create_components


@Component
class A: ...


@Factory
@Component
class B:

    def __init__(self, a: A):
        self.a = a

@Component
class C:

    def __init__(self, a: A, b: B):
        self.a = a
        self.b = b

@Component
class D:

    def __init__(self, a: A, b: B, c: C):
        self.a = a
        self.b = b
        self.c = c


@Component
class E:

    def __init__(self, a: A, c: C):
        self.a = a
        self.c = c


components = create_components()