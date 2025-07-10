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