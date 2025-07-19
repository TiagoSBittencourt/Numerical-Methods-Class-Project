from solvers_edo import SolverEDO
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial

def regressao_polinomial(mostrar_graficos=True):
    """
    Obs.3: Regressão polinomial de quarto grau e verificação da EDO
    
    Args:
        mostrar_graficos (bool): Se True, exibe os gráficos. Se False, apenas calcula.
    
    Passos:
    1. Resolver a EDO usando RK4 + Tiro (mesmo da Obs.1)
    2. Obter conjunto de pares ordenados (x, y)
    3. Fazer regressão polinomial de grau 4
    4. Calcular derivadas analíticas do polinômio
    5. Verificar se satisfaz a EDO: d²y/dx² = C * sqrt(1 + (dy/dx)²)
    """
    
    # --- Passo 1: Resolver a EDO (mesmo da Obs.1) ---
    C = 0.041

    def f(t, y2):
        y, w = y2
        dydx = w
        dwdx = C * np.sqrt(1.0 + w**2)
        return np.array([dydx, dwdx])

    a = 0.0
    b = 20
    h = 0.01
    y0 = 15            # y(0) = 15
    yb = 10            # y(20) = 10
    chute1 = -5        # Chute inicial para y'(0)
    chute2 = 10        # Segundo chute

    print("==> Resolvendo EDO usando RK4 + Tiro...")
    T, X = SolverEDO.tiro(f, a, b, h, y0, yb, chute1, chute2, max_iter=10)
    
    # --- Passo 2: Obter pares ordenados (x, y) ---
    x_data = T           # Pontos x (domínio)
    y_data = X[0]        # Pontos y (solução da EDO)
    
    print(f"Obtidos {len(x_data)} pares ordenados (x, y)")
    print(f"Intervalo: x ∈ [{x_data[0]:.2f}, {x_data[-1]:.2f}]")
    print(f"Valores y: y ∈ [{y_data.min():.2f}, {y_data.max():.2f}]")
    
    # --- Passo 3: Regressão polinomial de grau 4 ---
    print("\n==> Realizando regressao polinomial de grau 4...")
    
    # Usando numpy.polyfit para ajustar polinômio de grau 4
    coeficientes = np.polyfit(x_data, y_data, 4)
    polinomio = Polynomial(coeficientes[::-1])  # Inverte para ordem crescente de potências
    
    print("Coeficientes do polinomio P(x) = a₀ + a₁x + a₂x² + a₃x³ + a₄x⁴:")
    for i, coef in enumerate(coeficientes[::-1]):
        print(f"  a_{i} = {coef:.6e}")
    
    # --- Passo 4: Calcular derivadas analíticas do polinômio ---
    print("\n==> Calculando derivadas analiticas do polinomio...")
    
    # Primeira derivada: P'(x)
    polinomio_d1 = polinomio.deriv(1)
    
    # Segunda derivada: P''(x)
    polinomio_d2 = polinomio.deriv(2)
    
    print("Primeira derivada P'(x):")
    print(f"  P'(x) = {polinomio_d1}")
    print("Segunda derivada P''(x):")
    print(f"  P''(x) = {polinomio_d2}")
    
    # --- Passo 5: Verificar se satisfaz a EDO ---
    print("\n==> Verificando se o polinomio satisfaz a EDO...")
    
    # Avaliar polinômio e suas derivadas nos pontos x
    y_poly = polinomio(x_data)                 # P(x)
    dy_poly = polinomio_d1(x_data)            # P'(x)
    d2y_poly = polinomio_d2(x_data)           # P''(x)
    
    # Lado direito da EDO: C * sqrt(1 + (dy/dx)²)
    lado_direito_edo = C * np.sqrt(1.0 + dy_poly**2)
    
    # Erro absoluto entre lado esquerdo e direito
    erro_edo = np.abs(d2y_poly - lado_direito_edo)
    erro_medio = np.mean(erro_edo)
    erro_maximo = np.max(erro_edo)
    
    print(f"Erro medio |P''(x) - C√(1 + P'(x)²)|: {erro_medio:.6e}")
    print(f"Erro maximo: {erro_maximo:.6e}")
    
    # Coeficiente de determinação R² para qualidade do ajuste
    ss_res = np.sum((y_data - y_poly) ** 2)    # Soma dos quadrados dos resíduos
    ss_tot = np.sum((y_data - np.mean(y_data)) ** 2)  # Soma total dos quadrados
    r_squared = 1 - (ss_res / ss_tot)
    
    print(f"Coeficiente de determinacao R²: {r_squared:.6f}")
    
    # --- Visualização ---
    if mostrar_graficos:
        print("\n==> Gerando graficos de verificacao...")
        
        fig, axs = plt.subplots(3, 1, figsize=(15, 16))
        fig.suptitle('Obs.3: Regressão Polinomial de Grau 4 e Verificação da EDO', fontsize=16, fontweight='bold')
        
        # --- Gráfico 1: Comparação solução original vs polinômio ---
        ax1 = axs[0]
        ax1.plot(x_data, y_data, 'b-', linewidth=2, label='Solução Original (RK4+Tiro)')
        ax1.plot(x_data, y_poly, 'r--', linewidth=2, label='Polinômio de Grau 4')
        ax1.set_ylabel('y(x)')
        ax1.set_title(f'Comparação: Solução Original vs Regressão Polinomial (R² = {r_squared:.4f})')
        ax1.legend()
        ax1.grid(True, alpha=0.6)
        
        # --- Gráfico 2: Derivadas do polinômio ---
        ax2 = axs[1]
        ax2.plot(x_data, y_poly, 'k-', linewidth=2, label='P(x) - Polinômio')
        ax2.plot(x_data, dy_poly, 'g--', linewidth=2, label="P'(x) - 1ª Derivada")
        ax2.plot(x_data, d2y_poly, 'r:', linewidth=2, label="P''(x) - 2ª Derivada")
        ax2.set_ylabel('Valor')
        ax2.set_title('Polinômio e suas Derivadas Analíticas')
        ax2.legend()
        ax2.grid(True, alpha=0.6)
        
        # --- Gráfico 3: Verificação da EDO ---
        ax3 = axs[2]
        ax3.plot(x_data, d2y_poly, 'b-', linewidth=3, label="Lado Esquerdo: P''(x)")
        ax3.plot(x_data, lado_direito_edo, 'r--', linewidth=2, label="Lado Direito: C√(1 + P'(x)²)")
        ax3.set_xlabel('x (Posição Horizontal)')
        ax3.set_ylabel('Valor da Curvatura')
        ax3.set_title(f'Verificação da EDO (Erro Médio: {erro_medio:.2e})')
        ax3.legend()
        ax3.grid(True, alpha=0.6)
        
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.show()
        
        # --- Gráfico adicional: Erro absoluto ---
        plt.figure(figsize=(12, 6))
        plt.plot(x_data, erro_edo, 'r-', linewidth=2)
        plt.xlabel('x (Posição Horizontal)')
        plt.ylabel('Erro Absoluto |P\'\'(x) - C√(1 + P\'(x)²)|')
        plt.title(f'Erro na Satisfação da EDO pelo Polinômio de Grau 4\n(Erro Médio: {erro_medio:.2e}, Erro Máximo: {erro_maximo:.2e})')
        plt.grid(True, alpha=0.6)
        plt.yscale('log')  # Escala logarítmica para melhor visualização
        plt.tight_layout()
        plt.show()
    else:
        print("\n==> Graficos suprimidos para geracao de PDF...")
    
    # --- Relatório final ---
    print("\n" + "="*80)
    print("RELATORIO FINAL - Obs.3")
    print("="*80)
    print(f"Regressao polinomial de grau 4 realizada com sucesso")
    print(f"Qualidade do ajuste: R² = {r_squared:.6f}")
    print(f"Erro medio na EDO: {erro_medio:.6e}")
    print(f"Erro maximo na EDO: {erro_maximo:.6e}")
    
    if r_squared > 0.99:
        print("EXCELENTE: Polinomio representa muito bem a solucao original")
    elif r_squared > 0.95:
        print("BOM: Polinomio representa bem a solucao original")
    else:
        print("ATENCAO: Qualidade do ajuste pode ser melhorada")
    
    if erro_medio < 1e-3:
        print("EXCELENTE: Polinomio satisfaz bem a EDO")
    elif erro_medio < 1e-2:
        print("BOM: Polinomio satisfaz razoavelmente a EDO")
    else:
        print("ATENCAO: Polinomio nao satisfaz bem a EDO")
    
    print("="*80)
    
    return {
        'x_data': x_data,
        'y_data': y_data,
        'polinomio': polinomio,
        'coeficientes': coeficientes,
        'r_squared': r_squared,
        'erro_medio': erro_medio,
        'erro_maximo': erro_maximo
    }

if __name__ == "__main__":
    resultados = regressao_polinomial()
