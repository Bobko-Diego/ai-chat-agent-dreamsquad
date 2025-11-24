"""
Tool de Cálculo Matemático para o Agente de IA.
Permite realizar operações matemáticas básicas e avançadas.
"""

import math
from strands import tool


@tool
def calculator(expression: str) -> str:
    """
    Calcula expressões matemáticas e retorna o resultado.
    
    Use quando o usuário pedir cálculos como multiplicação, divisão, 
    raiz quadrada, potenciação ou outras operações matemáticas.
    
    Exemplos:
    - "1234 * 5678" → retorna 7006652
    - "sqrt(144)" → retorna 12
    - "2**10" → retorna 1024
    
    Args:
        expression: Expressão matemática (ex: "1234 * 5678" ou "sqrt(144)")
    
    Returns:
        Resultado numérico ou mensagem de erro
    """
    try:
        # Criar um namespace seguro com funções matemáticas
        safe_dict = {
            "__builtins__": {},
            "sqrt": math.sqrt,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log,
            "log10": math.log10,
            "exp": math.exp,
            "pow": math.pow,
            "abs": abs,
            "round": round,
            "pi": math.pi,
            "e": math.e,
        }
        
        # Avaliar a expressão de forma segura
        result = eval(expression, safe_dict)
        
        # Retornar apenas o resultado numérico (sem texto adicional)
        if isinstance(result, float):
            # Se for um número inteiro disfarçado de float, retornar como int
            if result.is_integer():
                return str(int(result))
            else:
                # Formatar com até 6 casas decimais, removendo zeros desnecessários
                return f"{result:.6f}".rstrip('0').rstrip('.')
        else:
            return str(result)
            
    except ZeroDivisionError:
        return "ERRO: Divisão por zero"
    except Exception as e:
        return f"ERRO: {str(e)}"