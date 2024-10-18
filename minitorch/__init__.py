"""minitorch package.

This package provides foundational components for building neural networks and performing
automatic differentiation. It includes tensor operations, scalar functions, optimization algorithms,
data handling, and module definitions.

Modules:

- `tensor_data`: Core tensor data structures and indexing.
- `tensor`: Tensor class with automatic differentiation support.
- `tensor_ops`: Tensor operations using various backends.
- `tensor_functions`: Implementation of autodifferentiation functions for tensors.
- `scalar`: Scalar values and operations with autodifferentiation.
- `scalar_functions`: Autodifferentiation functions for scalar values.
- `autodiff`: Core automatic differentiation logic.
- `module`: Base class for neural network modules.
- `optim`: Optimization algorithms.
- `datasets`: Utilities for handling datasets.
- `testing`: Utilities for testing mathematical correctness.

"""
from .testing import MathTest, MathTestVariable  # noqa: F401,F403
from .tensor_data import *  # noqa: F401,F403
from .tensor import *  # noqa: F401,F403
from .tensor_ops import *  # noqa: F401,F403
from .tensor_functions import *  # noqa: F401,F403
from .datasets import *  # noqa: F401,F403
from .optim import *  # noqa: F401,F403
from .testing import *  # noqa: F401,F403
from .module import *  # noqa: F401,F403
from .autodiff import *  # noqa: F401,F403
from .scalar import *  # noqa: F401,F403
from .scalar_functions import *  # noqa: F401,F403
from .module import *  # noqa: F401,F403
