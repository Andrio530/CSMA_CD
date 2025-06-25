# Simulador CSMA/CD - IEEE 802.3

Este projeto é um simulador gráfico do protocolo CSMA/CD (Carrier Sense Multiple Access with Collision Detection), utilizado em redes Ethernet (IEEE 802.3). Ele simula múltiplos transmissores tentando acessar um canal de comunicação, gerenciando colisões e aplicando o algoritmo de backoff exponencial binário.

## 🎯 Objetivo

Demonstrar visualmente como funciona o protocolo CSMA/CD em ambientes com concorrência de transmissões.

## 💻 Tecnologias Usadas

- Python 3
- Tkinter (GUI)
- Matplotlib (gráficos de estatísticas)

## 🧪 Funcionalidades

- Simulação visual de transmissões em um canal compartilhado
- Detecção de colisões e aplicação de backoff exponencial
- Exibição de estatísticas:
  - Total de tentativas
  - Transmissões bem-sucedidas
  - Colisões detectadas
  - Eficiência da simulação
- Geração de gráfico ao final da simulação

## 🛠️ Como Executar

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/csma-cd-simulator.git
cd csma-cd-simulator

# Execute o simulador
python simulador_csma_cd.py
