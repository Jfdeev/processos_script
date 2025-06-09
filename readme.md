# 🧠 Simulador de Escalonamento de CPU

Este é um simulador gráfico de algoritmos de escalonamento de CPU feito com Python e PyQt5. O app permite visualizar de forma interativa como diferentes algoritmos tratam os processos e quem termina primeiro.

## ✨ Funcionalidades

* Interface gráfica simples e intuitiva
* Suporte a 3 algoritmos clássicos:

  * **FIFO (First-In, First-Out)**
  * **Round Robin** (com quantum de 1 segundo)
  * **SJF (Shortest Job First)**
* Barra de progresso para cada processo
* Alerta com o **vencedor** (primeiro processo finalizado)

## 🛠️ Requisitos

* Python 3.7+
* PyQt5

Para instalar o PyQt5, use:

```bash
pip install PyQt5
```

## ▶️ Como rodar

Clone o repositório e execute o script:

```bash
python simulador.py
```

## 🧪 Processos simulados

```python
PROCESSOS = [
    {"name": "Flash", "time": 5},
    {"name": "Zoom", "time": 7},
    {"name": "Senna", "time": 4},
    {"name": "Sarvitar", "time": 8},
]
```

Você pode personalizar os processos trocando os nomes e tempos no código.

## 🤖 Uso de Inteligência Artificial

Partes deste projeto foram organizadas e refatoradas com o auxílio de uma IA (ChatGPT), especialmente para:

* Criar este arquivo `README.md` com explicações claras e bem formatadas
* Usada para auxiliar na criacao dos algoritimos de escalonamento

O código original foi desenvolvido manualmente, e a IA atuou como assistente de escrita e organização.

