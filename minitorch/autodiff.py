from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Set, Tuple, Protocol


# ## Task 1.1
# Central Difference calculation


def central_difference(f: Any, *vals: Any, arg: int = 0, epsilon: float = 1e-6) -> Any:
    r"""Computes an approximation to the derivative of `f` with respect to one arg.

    See :doc:`derivative` or https://en.wikipedia.org/wiki/Finite_difference for more details.

    Args:
    ----
        f : arbitrary function from n-scalar args to one value
        *vals : n-float values $x_0 \ldots x_{n-1}$
        arg : the number $i$ of the arg to compute the derivative
        epsilon : a small constant

    Returns:
    -------
        An approximation of $f'_i(x_0, \ldots, x_{n-1})$

    """
    # TODO: Implement for Task 1.1.
    vals_pos: List[float] = list(vals)
    vals_neg: List[float] = list(vals)

    vals_pos[arg] += epsilon
    vals_neg[arg] -= epsilon

    return (f(*vals_pos) - f(*vals_neg)) / (2 * epsilon)


variable_count = 1


class Variable(Protocol):
    def accumulate_derivative(self, x: Any) -> None: ...  # noqa: D102

    @property
    def unique_id(self) -> int: ...  # noqa: D102

    def is_leaf(self) -> bool: ...  # noqa: D102

    def is_constant(self) -> bool: ...  # noqa: D102

    @property
    def parents(self) -> Iterable["Variable"]: ...  # noqa: D102

    def chain_rule(self, d_output: Any) -> Iterable[Tuple[Variable, Any]]: ...  # noqa: D102


def topological_sort(variable: Variable) -> Iterable[Variable]:
    """Computes the topological order of the computation graph.

    Args:
    ----
        variable: The right-most variable

    Returns:
    -------
        Non-constant Variables in topological order starting from the right.

    """
    # TODO: Implement for Task 1.4.

    visited: Set[int] = set()  # Tracks permanently visited nodes
    sorted_list: List[Variable] = []  # Stores the sorted nodes
    visit(variable, visited, sorted_list)
    sorted_list.reverse()  # Reverse the order because we append at the end of recursion
    return sorted_list


def visit(variable: Variable, visited: Set[int], sorted_list: List[Variable]) -> None:
    """Recursive DFS to visit each node in the computation graph.

    Args:
    ----
        variable: The current node to visit
        visited: Set of visited nodes (to avoid revisiting)
        sorted_list: The list where sorted nodes are collected

    """
    # If the variable has already been visited, return early
    if variable.unique_id in visited:
        return

    # Visit each parent (i.e., input to this variable) recursively
    for parent in variable.parents:
        if not parent.is_constant():  # Skip constants in the topological sort
            visit(parent, visited, sorted_list)

    # After visiting all parents, mark this variable as visited
    visited.add(variable.unique_id)
    # Append this variable to the sorted list (after visiting its dependencies)
    sorted_list.append(variable)


def backpropagate(variable: Variable, deriv: Any) -> None:
    """Runs backpropagation on the computation graph in order to
    compute derivatives for the leave nodes.

    Args:
    ----
        variable: The right-most variable
        deriv: Its derivative that we want to propagate backward to the leaves.

    Returns:
    -------
        No return. Should write to its results to the derivative values of each leaf through `accumulate_derivative`.

    """
    # TODO: Implement for Task 1.4.
    sorted_vars = topological_sort(variable)

    # Step 2: Initialize the dictionary to store derivatives
    derivs: Dict[int, Any] = {variable.unique_id: deriv}

    # Step 3: Process each variable in reverse topological order
    for var in sorted_vars:
        # If it's a leaf node, accumulate its derivative
        if var.is_leaf():
            var.accumulate_derivative(derivs.get(var.unique_id, 0.0))
        else:
            # Apply the chain rule to compute the derivatives with respect to its parents
            for parent, parent_deriv in var.chain_rule(derivs[var.unique_id]):
                if parent.unique_id in derivs:
                    derivs[parent.unique_id] += (
                        parent_deriv  # Accumulate the derivative
                    )
                else:
                    derivs[parent.unique_id] = parent_deriv  # Initialize the derivative


@dataclass
class Context:
    """Context class is used by `Function` to store information during the forward pass."""

    no_grad: bool = False
    saved_values: Tuple[Any, ...] = ()

    def save_for_backward(self, *values: Any) -> None:
        """Store the given `values` if they need to be used during backpropagation."""
        if self.no_grad:
            return
        self.saved_values = values

    @property
    def saved_tensors(self) -> Tuple[Any, ...]:  # noqa: D102
        return self.saved_values
