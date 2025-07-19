from solvers_edo import SolverEDO
from numerical_dif import NumericalDifferentiator
from regressao import regressao_polinomial
from gerador_pdf import gerar_pdf_relatorio
import numpy as np
import matplotlib.pyplot as plt

def Obs1_Obs2():
    print("\n" + "="*80)
    print("RELATÓRIO DETALHADO - OBS.1 e OBS.2")
    print("="*80)
    
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

    print("\nPARAMETROS DO PROBLEMA:")
    print(f"   Constante C = {C}")
    print(f"   Intervalo: x ∈ [{a}, {b}]")
    print(f"   Passo h = {h}")
    print(f"   Condicoes de contorno: y({a}) = {y0}, y({b}) = {yb}")
    print(f"   Chutes iniciais para y'(0): {chute1}, {chute2}")

    print("\nOBS.1: METODO DO TIRO COM RUNGE-KUTTA 4ª ORDEM")
    print("-" * 60)
    
    T, X = SolverEDO.tiro(f, a, b, h, y0, yb, chute1, chute2, max_iter=10)
    
    # Estatísticas da solução
    n_pontos = len(T)
    y_solucao = X[0]
    dy_solucao = X[1]  # y'(x) obtido pelo método do tiro
    
    print(f"Solucao encontrada com {n_pontos} pontos")
    print(f"Valor inicial: y({T[0]:.2f}) = {y_solucao[0]:.6f}")
    print(f"Valor final: y({T[-1]:.2f}) = {y_solucao[-1]:.6f}")
    print(f"Erro na condicao de contorno: |y({b}) - {yb}| = {abs(y_solucao[-1] - yb):.2e}")
    print(f"Derivada inicial estimada: y'(0) = {dy_solucao[0]:.6f}")
    print(f"Derivada final: y'({b}) = {dy_solucao[-1]:.6f}")
    print(f"Estatisticas de y(x): min = {y_solucao.min():.4f}, max = {y_solucao.max():.4f}, media = {y_solucao.mean():.4f}")
    
    # Valores específicos
    print("\nVALORES DA SOLUCAO EM PONTOS ESPECIFICOS:")
    indices_especificos = [0, n_pontos//4, n_pontos//2, 3*n_pontos//4, -1]
    for i in indices_especificos:
        x_val = T[i]
        y_val = y_solucao[i]
        dy_val = dy_solucao[i]
        print(f"   y({x_val:2.0f}) = {y_val:8.4f}, y'({x_val:2.0f}) = {dy_val:8.4f}")
    
    print("\nOBS.2: DIFERENCIACAO NUMERICA (ERRO DE ORDEM h²)")
    print("-" * 60)
    
    # Aplicar diferenciação numérica
    diff = NumericalDifferentiator(y_solucao, h)
    d1_arr, d2_arr = diff.calculate_derivatives()
    d1_arr = np.array(d1_arr)
    d2_arr = np.array(d2_arr)
    
    print(f"Diferenciacao numerica aplicada a {len(y_solucao)} pontos")
    print("Metodos utilizados:")
    print("   - Forward difference: pontos extremos (erro O(h²))")
    print("   - Central difference: pontos internos (erro O(h²))")
    print("   - Backward difference: pontos extremos (erro O(h²))")
    
    # Comparação das derivadas
    erro_derivada = np.abs(dy_solucao - d1_arr)
    erro_medio_deriv = np.mean(erro_derivada)
    erro_max_deriv = np.max(erro_derivada)
    
    print(f"\nCOMPARACAO DE DERIVADAS:")
    print(f"   Erro na 1ª derivada |y'_RK4 - y'_numerica|:")
    print(f"   Erro medio: {erro_medio_deriv:.2e}")
    print(f"   Erro maximo: {erro_max_deriv:.2e}")
    
    # Verificação da EDO
    print(f"\nVERIFICACAO DA EQUACAO DIFERENCIAL:")
    print(f"   EDO: d²y/dx² = C√(1 + (dy/dx)²) onde C = {C}")
    
    # Calcula o lado direito da EDO usando a derivada numérica y'(x)
    lado_direito_edo = C * np.sqrt(1.0 + d1_arr**2)
    
    # Erro na satisfação da EDO
    erro_edo = np.abs(d2_arr - lado_direito_edo)
    erro_edo_medio = np.mean(erro_edo)
    erro_edo_maximo = np.max(erro_edo)
    erro_edo_rms = np.sqrt(np.mean(erro_edo**2))
    
    print(f"   Erro medio |y''_num - C√(1 + y'²)|: {erro_edo_medio:.2e}")
    print(f"   Erro maximo: {erro_edo_maximo:.2e}")
    print(f"   Erro RMS: {erro_edo_rms:.2e}")
    
    # Tabela de verificação em pontos específicos
    print(f"\nDERIVADAS EM PONTOS ESPECIFICOS:")
    print("   x       y(x)      y'(x)     y''(x)    C√(1+y'²)   Erro EDO")
    print("-" * 66)
    
    for i in indices_especificos:
        x_val = T[i]
        y_val = y_solucao[i]
        dy_val = d1_arr[i]
        d2y_val = d2_arr[i]
        lado_dir = C * np.sqrt(1.0 + dy_val**2)
        erro_local = abs(d2y_val - lado_dir)
        print(f"  {x_val:2.0f}    {y_val:7.4f}    {dy_val:7.4f}     {d2y_val:7.4f}       {lado_dir:7.4f}   {erro_local:.2e}")
    
    # Avaliação da qualidade
    print(f"\nQUALIDADE DA SOLUCAO:")
    if erro_edo_medio < 1e-3:
        print("   EXCELENTE: Solucao satisfaz bem a EDO (erro < 1e-03)")
    elif erro_edo_medio < 1e-2:
        print("   BOA: Solucao satisfaz razoavelmente a EDO (erro < 1e-02)")
    else:
        print("   REGULAR: Erro na EDO pode ser melhorado")
    
    if erro_medio_deriv < 1e-6:
        print("   EXCELENTE: Derivadas numericas muito precisas")
    elif erro_medio_deriv < 1e-4:
        print("   BOA: Derivadas numericas precisas")
    else:
        print("   REGULAR: Precisao das derivadas pode ser melhorada")
    
    print(f"\nDADOS GERADOS:")
    print(f"   {n_pontos} pontos da solucao y(x)")
    print(f"   {len(d1_arr)} valores da 1ª derivada y'(x)")
    print(f"   {len(d2_arr)} valores da 2ª derivada y''(x)")
    print(f"   Verificacao da EDO em todos os pontos")
    print("="*80)

    # Plotagem de resultados
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Gráfico 1: Solução y(x) e sua derivada primeira y'(x)
    ax1.plot(T, y_solucao, 'b-', linewidth=2, label='y(x) - Solução')
    ax1.plot(T, dy_solucao, 'r--', linewidth=2, label="y'(x) - 1ª Derivada")
    ax1.plot(T, d1_arr, 'g:', linewidth=1, alpha=0.7, label="y'(x) - Numérica")
    ax1.set_xlabel('x')
    ax1.set_ylabel('y(x), y\'(x)')
    ax1.set_title('Obs.1 e Obs.2: Solução e 1ª Derivada')
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.6)

    # Gráfico 2: Segunda derivada e verificação da EDO
    ax2.plot(T, d2_arr, 'b-', linewidth=2, label="y''(x) - 2ª Derivada Numérica")
    ax2.plot(T, lado_direito_edo, 'r--', linewidth=2, label=f"C√(1+y'²) - Lado Direito EDO")
    ax2.set_xlabel('x')
    ax2.set_ylabel("y''(x)")
    ax2.set_title('Obs.2: Verificação da EDO')
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.6)

    # Ajusta o layout para evitar sobreposição e exibe o gráfico
    plt.tight_layout(rect=[0, 0, 1, 0.95]) # Ajusta o retângulo para caber o suptitle
    plt.show()
    
    print("="*80)

def main():
    """Função principal que executa todas as análises"""
    print("=" * 80)
    print("PROJETO DE MÉTODOS NUMÉRICOS - ANÁLISE DE CABO SUSPENSO")
    print("=" * 80)
    
    # Executar todas as observações
    Obs1_Obs2()
    
    # Executa Obs.3
    print("\n" + "="*60)
    print("EXECUTANDO OBS.3 - REGRESSÃO POLINOMIAL")
    print("="*60)
    regressao_polinomial()
    
    # Opção para gerar PDF
    print("\n" + "=" * 60)
    print("GERAR RELATÓRIO PDF DETALHADO")
    print("=" * 60)
    
    resposta = input("Deseja gerar um relatório PDF detalhado? (s/n): ").lower().strip()
    
    if resposta in ['s', 'sim', 'y', 'yes']:
        try:
            print("\nGerando relatório PDF...")
            print("(Os cálculos serão executados novamente para o PDF, mas sem exibir gráficos)")
            
            nome_pdf = gerar_pdf_relatorio("relatorio_metodos_numericos.pdf")
            
            print(f"\nSUCESSO: Relatório PDF gerado com sucesso!")
            print(f"Arquivo: {nome_pdf}")
            print("O arquivo contém:")
            print("• Análise detalhada de todos os métodos")
            print("• Tabelas com resultados numéricos")
            print("• Verificação de erros e precisão")
            print("• Conclusões técnicas")
            print("• Metodologia implementada")
        except Exception as e:
            print(f"ERRO ao gerar PDF: {e}")
            print("Verifique se a biblioteca reportlab está instalada.")
    else:
        print("Relatório PDF não será gerado.")

if __name__ == "__main__":
    main()
