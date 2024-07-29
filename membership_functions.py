from abc import ABC, abstractmethod


class MembershipFunction(ABC):
    @abstractmethod
    def fuzzify(self, crisp_value):
        pass


class RectangularMembershipFunction(MembershipFunction):

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def fuzzify(self, crisp_value: float) -> float:
        return 1.0 if self.start <= crisp_value <= self.start else 0.0


class TriangularMembershipFunction(MembershipFunction):

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def fuzzify(self, x: float) -> float:
        if x == self.b:
            return 1.0
        elif self.a <= x <= self.b:
            return (x - self.a) / (self.b - self.a)
        elif self.b <= x <= self.c:
            return (self.c - x) / (self.c - self.b)
        else:
            return 0


class TrapezoidalMembershipFunction(MembershipFunction):

    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def fuzzify(self, x: float) -> float:
        if self.b <= x <= self.c:
            return 1.0
        elif self.a <= x < self.b:
            return (x - self.a) / (self.b - self.a)
        elif self.c < x < self.d:
            return (self.d - x) / (self.d - self.c)
        elif x <= self.a:
            return 0
        elif x > self.d:
            return 0.0
