from abc import ABC, abstractmethod
from membership_functions import MembershipFunction

class Node(ABC):

    @abstractmethod
    def evaluate(self, inputs):
        pass

    def __and__(self, other):
        return AndNode(self, other)

    def __or__(self, other):
        return OrNode(self, other)


class OrNode(Node):

    def __init__(self, left, right):
        self._left = left
        self._right = right

    def evaluate(self, inputs):
        left_result = self._left.evaluate(inputs)
        right_result = self._right.evaluate(inputs)
        return max(left_result, right_result)


class AndNode(Node):

    def __init__(self, left, right):
        self._left = left
        self._right = right

    def evaluate(self, inputs) -> float:
        left_result = self._left.evaluate(inputs)
        right_result = self._right.evaluate(inputs)
        return min(left_result, right_result)


class VariableNode(Node):

    def __init__(self, var, mf: MembershipFunction):
        self._var = var
        self._mf = mf

    def _get_crisp_value(self, inputs) -> float:
        if self._var.name not in inputs.keys():
            print('Input Variable Not Passed')
            return -1

        crisp_value = inputs[self._var.name]

        if not self._var.is_within_range(crisp_value):
            print('Input Variable Out Of Range')
            return -1

        return crisp_value

    def evaluate(self, inputs: dict) -> float:
        crisp_value = self._get_crisp_value(inputs)
        fuzzy_value = self._mf.fuzzify(crisp_value)
        return fuzzy_value

class InputVariable:
    def __init__(self, name: str, input_range: list[int]):
        self.name = name
        self.input_range = input_range
        self._mfs = {}

    def __getitem__(self, item):
        mf = self._mfs[item]
        return VariableNode(self, mf)

    def __setitem__(self, key, value):
        self._mfs[key] = value

    def is_within_range(self, crisp_value: float) -> bool:
        return self.input_range[0] <= crisp_value <= self.input_range[1]


class Rule:
    def __init__(self, premise: VariableNode, output: int):
        self.premise = premise
        self.output = output

    def evaluate(self, inputs) -> float:
        return self.premise.evaluate(inputs)


class FuzzySystem:
    def __init__(self, rules: list[Rule]):
        self.rules = rules

    def compute(self, **inputs):
        numerator = 0
        denominator = 0

        for rule in self.rules:
            weight = rule.evaluate(inputs)
            numerator += weight * rule.output
            denominator += weight

        return numerator / denominator
