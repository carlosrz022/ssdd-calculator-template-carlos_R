"""RemoteCalculator implementation for SSDD lab."""
import Ice
import RemoteCalculator  # pylint: disable=import-error


class Calculator(RemoteCalculator.Calculator):
    """Implementation of the RemoteCalculator.Calculator interface."""

    def sum(self, a: float, b: float, current: Ice.Current = None) -> float:  # pylint: disable=no-member, unused-argument
        """Calculates the sum of two numbers."""
        print(f"Summing {a} + {b}")
        return a + b

    def sub(self, a: float, b: float, current: Ice.Current = None) -> float:  # pylint: disable=no-member, unused-argument
        """Calculates the subtraction of two numbers."""
        print(f"Subtracting {a} - {b}")
        return a - b

    def mult(self, a: float, b: float, current: Ice.Current = None) -> float:  # pylint: disable=no-member, unused-argument
        """Calculates the multiplication of two numbers."""
        print(f"Multiplying {a} * {b}")
        return a * b

    def div(self, a: float, b: float, current: Ice.Current = None) -> float:  # pylint: disable=no-member, unused-argument
        """Calculates the division of two numbers. Raises ZeroDivisionError if b is zero."""
        print(f"Dividing {a} / {b}")
        if b == 0:
            raise RemoteCalculator.ZeroDivisionError()
        return a / b