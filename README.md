# Simulador CSMA/CD IEEE 802.3

Este projeto simula o funcionamento do protocolo de acesso ao meio **CSMA/CD (Carrier Sense Multiple Access with Collision Detection)**, conforme a especificação da IEEE 802.3 (Ethernet). 
A simulação é feita com interface gráfica usando `Tkinter` e gráficos com `Matplotlib`.

## 🎯 Objetivo
Demonstrar visualmente o funcionamento do algoritmo CSMA/CD, incluindo detecção de colisões, envio de pacotes, controle de acesso ao canal e estatísticas do processo.

## ⚙️ Funcionalidades
- Transmissão de dados por múltiplos transmissores.
- Verificação de ocupação do canal antes da transmissão.
- Detecção de colisões e aplicação de **backoff exponencial**.
- Exibição visual em tempo real do status do canal.
- Geração de gráfico com estatísticas de desempenho:
  - Pacotes enviados com sucesso
  - Colisões
  - Tentativas totais
  - Eficiência (%)

## 🛠️ Como executar

1. Certifique-se de ter o Python instalado (>= 3.7).
2. Instale o matplotlib se ainda não tiver:
```bash
pip install matplotlib
```
3. Execute o script:
```bash
python nome_do_arquivo.py
```

## ✏️ Personalização
Você pode ajustar o comportamento da simulação diretamente no código fonte:

- **Quantidade de transmissores:**
  Altere o valor da variável `self.num_transmitters` na classe `CSMACDSimulatorGUI` para simular mais ou menos estações simultâneas.

- **Velocidade da simulação:**
  Modifique o valor de `self.simulation_speed` para alterar a velocidade (em segundos) entre tentativas de transmissão. Valores maiores tornam a simulação mais lenta e visualmente mais clara.

- **Estatísticas:**
  O sistema mostra estatísticas detalhadas ao final da simulação, permitindo a análise do desempenho do protocolo sob diferentes cenários.

## 🖼️ Interface
A interface gráfica mostra em tempo real o status do canal (livre ou ocupado) e os eventos de cada transmissor. 

## 📊 Exemplo de gráfico de estatísticas gerado
- Sucessos x Tentativas
- Eficiência (%)

## 📁 Estrutura de pastas
```
📦csma-cd-simulator
 ┣ 📜csma_cd_simulator.py
 ┣ 📜README.md
 ┗ 📂screenshots
     ┗ 📜.gitkeep
```

## 👨‍💻 Autor
Ândrio Gabriel Epping

---
Este projeto é parte de uma simulação acadêmica para ilustrar o comportamento do protocolo Ethernet em ambientes concorrentes.
