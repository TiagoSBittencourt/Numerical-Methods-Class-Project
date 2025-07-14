from solvers_edo import SolverEDO
from numerical_dif import NumericalDifferentiator
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    
    def Obs1_Obs2():
        C = 0.041

        def f(t, y2):
            y, w = y2
            dydx = w
            dwdx = C * np.sqrt(1.0 + w**2)
            return np.array([dydx, dwdx])

        a = 0.0
        b = 20
        h = 0.01
        y0 = 15            # y(0) = 0
        yb = 10            # y(pi/2) = 1
        chute1 = -5        # Chute inicial para y'(0)
        chute2 = 10        # Segundo chute

        T, X = SolverEDO.tiro(f, a, b, h, y0, yb, chute1, chute2, max_iter=10)

        """ To print x - y values """
        # for i in range(len(T)):
        #     print(f"y({T[i]:.2f}) ≈ {X[0, i]:.6f}")

        differentiator = NumericalDifferentiator(list(X[0]), h)
        d1, d2 = differentiator.calculate_derivatives()

        # Converte as listas de derivadas para arrays NumPy para facilitar os cálculos
        d1_arr = np.array(d1)
        d2_arr = np.array(d2)

        # 1. Cria a figura e os eixos para 2 subplots empilhados
        # sharex=True faz com que ambos os gráficos usem o mesmo eixo x
        fig, axs = plt.subplots(2, 1, figsize=(14, 12), sharex=True)
        fig.suptitle('Análise Completa da Solução da EDO (RK4, Tiro, Diff. Num.)', fontsize=18, fontweight='bold')

        # --- Painel Superior: Solução e suas Derivadas ---
        ax1 = axs[0]
        ax1.plot(T, X[0], 'o-', markersize=3, label='y(x) - Posição do Fio')
        ax1.plot(T, d1_arr, '--', label="y'(x) - Inclinação (1ª Derivada)")
        ax1.plot(T, d2_arr, ':', label="y''(x) - Curvatura (2ª Derivada)")

        ax1.set_ylabel("y(x) / y'(x) / y\"(x)")
        ax1.set_title('Solução e suas Derivadas Numéricas', fontsize=14)
        ax1.legend()
        ax1.grid(True, linestyle='--', alpha=0.6)

        # --- Painel Inferior: Verificação da EDO ---
        ax2 = axs[1]

        # Calcula o lado direito da EDO usando a derivada numérica y'(x)
        lado_direito_edo = C * np.sqrt(1.0 + d1_arr**2)

        ax2.plot(T, d2_arr, 'b-', linewidth=3, label="Lado Esquerdo (y'' calculada)")
        ax2.plot(T, lado_direito_edo, 'r--', linewidth=2, label="Lado Direito (C * sqrt(1 + y'^2))")

        ax2.set_xlabel('x (Posição Horizontal)', fontsize=12)
        ax2.set_ylabel('Valor da Curvatura y\"')
        ax2.set_title('Verificação da Consistência da Solução com a EDO', fontsize=14)
        ax2.legend()
        ax2.grid(True, linestyle='--', alpha=0.6)

        # Ajusta o layout para evitar sobreposição e exibe o gráfico
        plt.tight_layout(rect=[0, 0, 1, 0.95]) # Ajusta o retângulo para caber o suptitle
        plt.show()

    Obs1_Obs2()
