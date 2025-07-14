from typing import List, Tuple

class NumericalDifferentiator:
    """
    Calculates the first and second numerical derivatives of a given dataset.

    This class uses finite difference methods to approximate derivatives.
    It automatically selects the appropriate formula (forward, central, or backward)
    based on the data point's position to maintain accuracy across the entire set.
    """

    def __init__(self, y_values: List[float], step_size: float):
        """
        Initializes the differentiator with the dataset and step size.

        Args:
            y_values (List[float]): A list of y-values for the function f(x).
            step_size (float): The constant distance 'h' between x-values.
        """
        if len(y_values) < 4:
            raise ValueError("Input y_values must contain at least 4 points.")
        if step_size <= 0:
            raise ValueError("Step size 'h' must be positive.")
            
        self.y = y_values
        self.h = step_size
        self.n = len(y_values)

    # --- Public Method ---

    def calculate_derivatives(self) -> Tuple[List[float], List[float]]:
        """
        Computes the first and second derivatives for all points in the dataset.

        Returns:
            Tuple[List[float], List[float]]: A tuple containing two lists:
                                             - The first list holds the first derivatives.
                                             - The second list holds the second derivatives.
        """
        first_derivatives: List[float] = []
        second_derivatives: List[float] = []

        for i in range(self.n):
            if i == 0:
                # Use forward difference for the first point
                d1 = self._forward_first_derivative(self.y[0], self.y[1], self.y[2])
                d2 = self._forward_second_derivative(self.y[0], self.y[1], self.y[2], self.y[3])
            elif i == self.n - 1:
                # Use backward difference for the last point
                d1 = self._backward_first_derivative(self.y[i-2], self.y[i-1], self.y[i])
                d2 = self._backward_second_derivative(self.y[i-3], self.y[i-2], self.y[i-1], self.y[i])
            else:
                # Use central difference for all interior points
                d1 = self._central_first_derivative(self.y[i-1], self.y[i+1])
                d2 = self._central_second_derivative(self.y[i-1], self.y[i], self.y[i+1])
            
            first_derivatives.append(d1)
            second_derivatives.append(d2)
            
        return first_derivatives, second_derivatives

    # --- Private Methods  ---

    def _forward_first_derivative(self, y0: float, y1: float, y2: float) -> float:
        """Formula for 1st derivative at the start of the data. O(h^2)"""
        return (-3*y0 + 4*y1 - y2) / (2 * self.h)

    def _backward_first_derivative(self, y0: float, y1: float, y2: float) -> float:
        """Formula for 1st derivative at the end of the data. O(h^2)"""
        return (y0 - 4*y1 + 3*y2) / (2 * self.h)

    def _central_first_derivative(self, y_prev: float, y_next: float) -> float:
        """Formula for 1st derivative at interior points. O(h^2)"""
        return (y_next - y_prev) / (2 * self.h)

    def _forward_second_derivative(self, y0: float, y1: float, y2: float, y3: float) -> float:
        """Formula for 2nd derivative at the start of the data. O(h^2)"""
        return (2*y0 - 5*y1 + 4*y2 - y3) / (self.h ** 2)

    def _backward_second_derivative(self, y0: float, y1: float, y2: float, y3: float) -> float:
        """Formula for 2nd derivative at the end of the data. O(h^2)"""
        return (-y0 + 4*y1 - 5*y2 + 2*y3) / (self.h ** 2)

    def _central_second_derivative(self, y_prev: float, y_current: float, y_next: float) -> float:
        """Formula for 2nd derivative at interior points. O(h^2)"""
        return (y_next - 2*y_current + y_prev) / (self.h ** 2)



if __name__ == "__main__":
    y_data = [0.0, 1.0, 8.0, 27.0, 64.0]
    h_step = 1.0

    try:
        # 1. Create an instance of the class
        differentiator = NumericalDifferentiator(y_values=y_data, step_size=h_step)

        # 2. Calculate the derivatives
        first_derivative, second_derivative = differentiator.calculate_derivatives()

        # 3. Print the results
        print("Original Y Values: ", y_data)
        print("-" * 30)
        print("Calculated 1st Derivatives:", [round(val, 2) for val in first_derivative])
        print("Calculated 2nd Derivatives:", [round(val, 2) for val in second_derivative])

    except ValueError as e:
        print(f"Error: {e}")