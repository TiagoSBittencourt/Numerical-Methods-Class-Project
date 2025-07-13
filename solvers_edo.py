import numpy as np
from typing import Callable, Tuple

class SolverEDO:
    """
    Uma classe que agrupa métodos estaticos para resolver sistemas de EDOs.
    """

    @staticmethod
    def rk1(f: Callable, a: float, b: float, h: float, x0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Resolve um sistema de EDOs usando o método de Euler.

        Argumentos:
        f (Callable): Função que calcula as derivadas (deve receber t e x)
        a (float): Início do intervalo
        b (float): Fim do intervalo
        h (float): Tamanho do passo
        x0 (np.ndarray): Condições iniciais (vetor)

        Retorna:
        (np.ndarray, np.ndarray): Tupla com o vetor T e a matriz solução X
        """
        # Força np.ndarray
        x0 = np.asarray(x0)

        # Cria o array com t0 ate tb com passo h
        T = np.arange(a, b + h, h)
        n = len(T)
        m = len(x0)

        # Cria um array com as aproximações no tempo (todas = 0)
        X = np.zeros((m, n))

        # Primeira coluna inicia com os valores inicias passados como parametro 
        X[:, 0] = x0

        # Itera aplicando Euler "n" vezes
        for i in range(n - 1):
            t_i = T[i]                          # Pega o valor atual do tempo (qual iteração)
            x_i = X[:, i]                       # Pega os valores da ultima interação
            X[:, i + 1] = x_i + h * f(t_i, x_i) # Aplica Euler para chutar proximos valores

        return T, X

    @staticmethod
    def rk2(f: Callable, a: float, b: float, h: float, x0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Resolve um sistema de EDOs usando o método de Runge-Kutta de 2ª ordem (Euler modificado)

        Argumentos:
        f (Callable): Função que calcula as derivadas (deve receber t e x)
        a (float): Início do intervalo
        b (float): Fim do intervalo
        h (float): Tamanho do passo
        x0 (np.ndarray): Condições iniciais (vetor)

        Retorna:
        (np.ndarray, np.ndarray): Tupla com o vetor T e a matriz solução X
        """
        # Força np.ndarray
        x0 = np.asarray(x0)

        # Cria o array com t0 até tb com passo h
        T = np.arange(a, b + h, h)
        n = len(T)
        m = len(x0)

        # Cria um array com as aproximações no tempo (todas = 0)
        X = np.zeros((m, n))

        # Primeira coluna inicia com os valores iniciais passados como parametro
        X[:, 0] = x0

        # Itera aplicando RK2 "n" vezes
        for i in range(n - 1):
            t_i = T[i]                     # Tempo atual
            x_i = X[:, i]                  # Estado atual (todas variáveis)

            k1 = f(t_i, x_i)               # Estima a derivada em t_i
            k2 = f(t_i + h, x_i + h * k1)  # Estima a derivada em t_i + h (usando k1)

            # Atualiza o próximo valor com a média ponderada das inclinações (formula de rk2)
            X[:, i + 1] = x_i + (h / 2) * (k1 + k2)

        return T, X

    @staticmethod
    def rk4(f: Callable, a: float, b: float, h: float, x0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Resolve um sistema de EDOs usando o método de Runge-Kutta de 4ª ordem

        Argumentos:
        f (Callable): Função que calcula as derivadas (deve receber t e x)
        a (float): Início do intervalo
        b (float): Fim do intervalo
        h (float): Tamanho do passo
        x0 (np.ndarray): Condições iniciais (vetor)

        Retorna:
        (np.ndarray, np.ndarray): Tupla com o vetor T e a matriz solução X
        """
        # Força np.ndarray
        x0 = np.asarray(x0)

        # Cria o array com t0 até tb com passo h
        T = np.arange(a, b + h, h)
        n = len(T)
        m = len(x0)

        # Cria um array com as aproximações no tempo (todas = 0)
        X = np.zeros((m, n))

        # Primeira coluna inicia com os valores iniciais passados como parametro
        X[:, 0] = x0

        # Itera aplicando RK4 "n" vezes
        for i in range(n - 1):
            t_i = T[i]                     # Tempo atual
            x_i = X[:, i]                  # Estado atual (todas variáveis)

            k1 = f(t_i, x_i)                              # Estima a derivada no ponto inicial (t_i)
            k2 = f(t_i + (h / 2), x_i + (h / 2) * k1)         # Estima a derivada no ponto "medio" (t_i + h/2)
            k3 = f(t_i + (h / 2), x_i + (h / 2) * k2)         # Estima a derivada no ponto "medio"
            k4 = f(t_i + h, x_i + h * k3)                 # Estima a derivada no final do intervalo (t_i + h)

            # Atualiza o próximo valor com a média ponderada das inclinações (fórmula de RK4)
            X[:, i + 1] = x_i + (h / 6) * (k1 + 2*k2 + 2*k3 + k4) # Equivalente: x_i + h*((k1/6) + (k2/3) + (k3/3) + (k4/6))

        return T, X

    @staticmethod
    def tiro(f: Callable, a: float, b: float, h: float, y0: float, yb: float, chute1: float, chute2: float, tol: float = 1e-5, max_iter: int = 100) -> Tuple[np.ndarray, np.ndarray]:
        """
        Resolve uma EDO de 2ª ordem como PVI usando o método do Tiro Simples com Runge-Kutta de 4ª ordem.

        Argumentos:
        f (Callable): Função que retorna o sistema reescrito como EDOs de 1ª ordem (recebe t e vetor x)
        a (float): Início do intervalo
        b (float): Fim do intervalo
        h (float): Tamanho do passo
        y0 (float): Condição inicial y(a)
        yb (float): Valor esperado para y(b)
        chute1 (float): Primeiro chute para y'(a)
        chute2 (float): Segundo chute para y'(a)
        tol (float): Tolerância para o critério de parada
        max_iter (int): Número máximo de iterações

        Retorna:
        (np.ndarray, np.ndarray): Vetor T e matriz solução X (com y e y')
        """
        
        x0_1 = np.array([y0, chute1])
        _, X1 = SolverEDO.rk4(f, a, b, h, x0_1)
        erro1 = X1[0, -1] - yb

        x0_2 = np.array([y0, chute2])
        T, X2 = SolverEDO.rk4(f, a, b, h, x0_2)
        erro2 = X2[0, -1] - yb

        for _ in range(max_iter):
            if abs(erro2) < tol:
                return T, X2

            # Secante 
            chute3 = chute2 - erro2 * (chute2 - chute1) / (erro2 - erro1)

            x0_3 = np.array([y0, chute3])
            T, X3 = SolverEDO.rk4(f, a, b, h, x0_3)
            erro3 = X3[0, -1] - yb 

            # Atualiza valores para a proxima iteração  
            chute1, erro1 = chute2, erro2
            chute2, erro2 = chute3, erro3 
            X2 = X3

        return T, X2



if __name__ == "__main__":
    def f_test(t, x):
        return (t / x) - (x / t)

    a = 1.0         # Inicio
    h = 0.1         # Passo
    num_passos = 3  
    b = a + num_passos * h  # Final
    x0 = [2.0]    # Condição inicial y(1) = 2


    print("\n==> Método de Euler (RK1):")
    T1, X1 = SolverEDO.rk1(f_test, a, b, h, x0)
    for i in range(len(T1)):
        print(f"y({T1[i]:.1f}) ≈ {X1[0, i]:.6f}")

    print("\n==> Método de Runge-Kutta de 2ª ordem (RK2):")
    T2, X2 = SolverEDO.rk2(f_test, a, b, h, x0)
    for i in range(len(T2)):
        print(f"y({T2[i]:.1f}) ≈ {X2[0, i]:.6f}")

    print("\n==> Método de Runge-Kutta de 4ª ordem (RK4):")
    T4, X4 = SolverEDO.rk4(f_test, a, b, h, x0)
    for i in range(len(T4)):
        print(f"y({T4[i]:.1f}) ≈ {X4[0, i]:.6f}")

    import matplotlib.pyplot as plt

    def f_tiro(x, y):
        return np.array([y[1], -y[0]])

    a = 0.0
    b = np.pi / 2
    h = 0.1
    y0 = 0.0           # y(0) = 0
    yb = 1.0           # y(pi/2) = 1
    chute1 = 0.0       # Chute inicial para y'(0)
    chute2 = 2.0       # Segundo chute

    print("\n==> Método do Tiro com RK4:")
    T, X = SolverEDO.tiro(f_tiro, a, b, h, y0, yb, chute1, chute2)

    for i in range(len(T)):
        print(f"y({T[i]:.2f}) ≈ {X[0, i]:.6f}")

    # Solução analítica para comparação
    def y_exata(x):
        return np.sin(x)

    # Plotando a solução numérica vs analítica
    plt.figure(figsize=(10, 5))
    plt.plot(T, X[0], 'o-', label='Solução Numérica (Método do Tiro + RK4)')
    plt.plot(T, y_exata(T), 'r--', label='Solução Analítica: y(x) = sin(x)')
    plt.xlabel('x')
    plt.ylabel('y(x)')
    plt.title('Comparação: Solução Numérica vs. Solução Exata')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()