# AI Chat Agent DreamSquad 🦄👾

API de Chat com Agente de IA capaz de realizar cálculos matemáticos utilizando FastAPI, Strands Agents SDK e Ollama.

## Descrição

Este projeto implementa uma API REST que se conecta a um Agente de IA configurado para:

-   Responder perguntas de conhecimento geral
-   Realizar cálculos matemáticos usando uma tool especializada, quando necessário
-   Identificar automaticamente quando usar ferramentas externas

## Estrutura do Projeto

```
ia-chat-agent-dreamsquad/
├── .env                    # Variáveis de ambiente
├── .gitignore             # Ignorados pelo Git
├── README.md              # Documentação
├── requirements.txt       # Dependências
├── main.py               # API principal com FastAPI
└── tools/
    └── calculator.py     # Tool de cálculo matemático
```

## Pré-requisitos

Antes de começar, lembre-se de ter instalado:

1. **Python 3.8+**

    ```bash
    python3 --version
    ```

2. **Ollama** (já instalado no seu MacBook)

    ```bash
    ollama --version
    ```

3. **Modelo Gemma2** (já baixado)
    ```bash
    ollama list
    ```
    Você deve ver `llama3.2:latest` na lista.

## ⚙️ Instalação

### 1. Clone ou crie o projeto

```bash
cd ai-chat-agent-dreamsquad
```

### 2. Crie e ative um ambiente virtual

```bash

python3 -m venv venv

# Ativar no macOS/Linux
source venv/bin/activate
```

Quando o ambiente virtual estiver ativado, você verá `(venv)` no início do prompt.

### 3. Instale as dependências

```bash
pip install --upgrade pip
pip install -r requirements.txt
# ou
pip install --upgrade -r requirements.txt
```

### 4. Configure as variáveis de ambiente

O arquivo `.env` deve estar configurado com valores padrão. Crie um arquivo `.env` e insira as informações abaixo:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:latest
API_HOST=0.0.0.0
API_PORT=8000
AGENT_MAX_TOKENS=2000
AGENT_TEMPERATURE=0.7
```

## Execução

### 1. Certifique-se de que o Ollama está rodando

Ao rodar o comando abaixo, é esperado um JSON tipo '{models: [{...}]}' como retorno

```bash
curl http://localhost:11434/api/tags
```

Se não tiver retornado o JSON, inicie o Ollama:

```bash
ollama serve
```

### 2. Inicie a API

Na primeira janela do terminal rode o comando:

```bash
python main.py
```

Se a API startar corretamente, aparecerá a mensagem:

```
🚀 Iniciando Chat Agent API
📍 URL: http://0.0.0.0:8000
📚 Documentação: http://0.0.0.0:8000/docs
🤖 Modelo: llama3.2:latest
🌐 Ollama Host: http://localhost:11434
💡 Cada requisição é independente
```

## Endpoints da API

### 1. `GET /` - Informações da API

```bash
curl http://localhost:8000/
```

### 2. `GET /health` - Health Check

```bash
curl http://localhost:8000/health
```

### 3. `POST /chat` - Testando o chat com o Agente

Quando a primeira janela de terminal estiver com a API startada corretamente, abra uma segunda janela de temrinal e cole o seguinte:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Olá"}'
```

**Importante:** Optei pela API é **stateless**, então cada requisição é independente e não mantém histórico de conversas anteriores.

### Teste de cálculo 1: Cálculo simples (usa a tool)

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Quanto é 2391 * 4295?"}'
```

**Resposta esperada:**

```json
{
    "response": "O resultado é: 10269345"
}
```

### Teste de cálculo 2: Raiz quadrada (usa a tool)

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Qual a raiz quadrada de 144?"}'
```

**Resposta esperada:**

```json
{
    "response": "A raiz quadrada de 144 é 12"
}
```

### Teste sem cálculo 3: Conhecimento geral (não usa a tool)

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Quem foi Albert Einstein?"}'
```

**Resposta esperada:**

```json
{
    "response": "Albert Einstein foi um físico teórico alemão..."
}
```

### Teste 4: Via Interface Swagger

Acesse: http://localhost:8000/docs

Na interface Swagger você pode:

1. Clicar em `POST /chat`
2. Clicar em "Try it out"
3. Inserir uma mensagem no campo `message`
4. Clicar em "Execute"

## Solução de Problemas

### Problema: "Agente não está disponível ou algo parecido"

**Solução:** Certifique-se de que o Ollama está rodando:

```bash
ollama serve
```

### Problema: "Model not found"

**Solução:** Baixe o modelo usado para o desenvolvimento desse projeto:

```bash
ollama pull llama3.2
```

### Problema: "Connection refused"

**Solução:** Verifique se a porta 11434 do Ollama está acessível:

```bash
curl http://localhost:11434/api/tags
```

### Problema: Importação de módulos

**Solução:** Certifique-se de que o ambiente virtual está ativado:

```bash
source venv/bin/activate
pip install --update -r requirements.txt
```

## Tecnologias Utilizadas

-   **[FastAPI](https://fastapi.tiangolo.com/)**: Framework web moderno e rápido para Python
-   **[Strands Agents](https://strandsagents.com/latest/documentation/docs/)**: Framework para criação de agentes de IA
-   **[Ollama](https://ollama.com/)**: Runtime local para modelos de linguagem
-   **[Gemma2]**: Modelo de linguagem do Google
-   **[Python-dotenv](https://pypi.org/project/python-dotenv/)**: Gerenciamento de variáveis de ambiente
-   **[Uvicorn]**: Servidor ASGI de alta performance

## Licença

Este projeto foi desenvolvido como parte de um processo seletivo.

---

Desenvolvido com dedicação para o time de #dreamers!
