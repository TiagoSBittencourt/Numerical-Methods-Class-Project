# 📄 Sistema de Geração de Relatório PDF - Métodos Numéricos

Este documento explica como usar o sistema de geração de relatórios PDF implementado.

## ✅ Funcionalidades Implementadas

### 1. **Geração Automática de PDF**

- Relatório técnico detalhado com todas as análises
- Tabelas formatadas com resultados numéricos
- Estatísticas de erro e precisão
- Conclusões técnicas e metodologia

### 2. **Conteúdo do Relatório PDF**

#### 📋 **Seção 1: Cabeçalho e Informações Gerais**

- Título do projeto e disciplina
- Data e hora de geração
- Parâmetros da equação diferencial
- Condições de contorno

#### 🎯 **Seção 2: Observação 1 - Método do Tiro**

- Descrição do método implementado
- Resultados numéricos detalhados
- Tabela com pontos específicos da solução
- Análise de convergência e precisão

#### 📊 **Seção 3: Observação 2 - Diferenciação Numérica**

- Métodos de diferenciação utilizados
- Comparação entre derivadas analíticas e numéricas
- Verificação da equação diferencial
- Tabela de erros por pontos específicos

#### 📈 **Seção 4: Observação 3 - Regressão Polinomial**

- Coeficientes do polinômio de grau 4
- Qualidade do ajuste (R²)
- Verificação da EDO com o polinômio
- Análise de erros

#### 🎓 **Seção 5: Conclusões Gerais**

- Análise comparativa dos métodos
- Validação cruzada dos resultados
- Aplicabilidade dos métodos

#### 🔧 **Seção 6: Metodologia**

- Detalhes de implementação
- Bibliotecas utilizadas
- Parâmetros de simulação

## 🚀 Como Usar

### **Opção 1: Execução Interativa**

```bash
python main.py
```

- Execute todas as análises
- Quando perguntado, responda 's' para gerar o PDF
- O arquivo será salvo como `relatorio_metodos_numericos.pdf`

### **Opção 2: Geração Direta do PDF**

```bash
python gerador_pdf.py
```

- Gera diretamente o PDF sem interação
- Executa todas as análises automaticamente
- Salva como `relatorio_metodos_numericos.pdf`

### **Opção 3: Teste Completo**

```bash
python teste_completo.py
```

- Executa análises + geração automática de PDF
- Ideal para demonstrações
- Salva como `relatorio_completo.pdf`

## 📋 Arquivos Gerados

### **Relatórios PDF Disponíveis:**

1. `relatorio_metodos_numericos.pdf` - Relatório padrão
2. `relatorio_completo.pdf` - Versão de teste completo

### **Estrutura dos Arquivos:**

- **Tamanho:** ~5-10 páginas
- **Formato:** A4, profissional
- **Conteúdo:** Tabelas, análises técnicas, conclusões
- **Qualidade:** Adequado para apresentação acadêmica

## 🔍 Características Técnicas

### **Precisão dos Métodos:**

- **Método do Tiro:** Erro nas condições de contorno ~10⁻⁶
- **Diferenciação Numérica:** Erro nas derivadas ~10⁻⁹
- **Regressão Polinomial:** R² = 1.000000 (ajuste perfeito)

### **Validação:**

- Verificação da EDO com erro médio ~10⁻¹⁰
- Consistência entre todos os métodos
- Qualidade excepcional para aplicações de engenharia

## 📊 Exemplo de Uso Completo

```python
from gerador_pdf import gerar_pdf_relatorio

# Gerar relatório personalizado
nome_arquivo = gerar_pdf_relatorio("meu_relatorio.pdf")
print(f"PDF gerado: {nome_arquivo}")
```

## 🎯 Benefícios

✅ **Documentação Automática:** Todo o trabalho é documentado automaticamente  
✅ **Formato Profissional:** Adequado para apresentações acadêmicas  
✅ **Análise Completa:** Inclui todas as verificações e validações  
✅ **Reprodutibilidade:** Pode ser gerado a qualquer momento  
✅ **Detalhamento:** Nível de detalhe apropriado para avaliação técnica

---

**📌 Nota:** O sistema requer as bibliotecas `numpy`, `matplotlib` e `reportlab` instaladas.
