# Importações
import tkinter as tk
import threading
import time
import random
import matplotlib.pyplot as plt

class CSMACDSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador CSMA/CD - IEEE 802.3")
        self.status_var = tk.StringVar(value="Canal: Livre")
        self.running = False
        self.packet_global_id = 0  # Contador global de pacotes
        self.stats = {}
        self.velocidade_simulacao = tk.DoubleVar(value=1.0)
        self.transmitting_now = []
        self.transmitting_lock = threading.Lock()

        self.canvas = tk.Canvas(root, width=1200, height=300, bg='white')
        self.canvas.pack(pady=10)
        self.rects = []
        self.num_transmitters = 4

        for i in range(self.num_transmitters):
            x0 = 30 + i * 110
            rect = self.canvas.create_rectangle(x0, 30, x0 + 80, 100, fill="gray")
            self.canvas.create_text(x0 + 40, 110, text=f"T{i + 1}", font=("Arial", 10, "bold"))
            self.rects.append(rect)
            self.stats[f"T{i + 1}"] = {"sucesso": 0, "colisoes": 0, "tentativas": 0}

        self.status_label = tk.Label(root, textvariable=self.status_var, font=("Arial", 14))
        self.status_label.pack()

        self.log_text = tk.Text(root, height=10, width=100)
        self.log_text.pack(pady=10)

        self.start_btn = tk.Button(root, text="Iniciar Simulação", command=self.iniciar_simulacao)
        self.start_btn.pack(pady=5)

        self.stop_btn = tk.Button(root, text="Parar Simulação", command=self.parar_simulacao)
        self.stop_btn.pack(pady=5)

        self.stats_btn = tk.Button(root, text="Mostrar Estatísticas", command=self.mostrar_estatisticas)
        self.stats_btn.pack(pady=5)

        self.save_log_btn = tk.Button(root, text="Salvar Log", command=self.salvar_log)
        self.save_log_btn.pack(pady=5)

        tk.Label(root, text="Velocidade da Simulação (1.0 = normal):").pack()
        self.velocidade_slider = tk.Scale(root, from_=0.1, to=3.0, resolution=0.1,
                                          orient=tk.HORIZONTAL, variable=self.velocidade_simulacao)
        self.velocidade_slider.pack(pady=5)

    def log(self, msg):
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)

    def iniciar_simulacao(self):
        if not self.running:
            self.running = True
            for i in range(self.num_transmitters):
                threading.Thread(target=self.simular_transmissao, args=(f"T{i + 1}", self.rects[i]), daemon=True).start()

    def parar_simulacao(self):
        self.running = False
        self.status_var.set("Simulação parada.")
        self.log("==== Simulação Finalizada ====")

    def simular_transmissao(self, nome, rect_id):
        slot_time = 0.2
        max_tentativas = 10
        packet = None
        k = 0

        while self.running:
            v = self.velocidade_simulacao.get()

            if packet is None:
                self.packet_global_id += 1
                packet = f"P{self.packet_global_id}"
                k = 0  # Resetar tentativas

            if k == 0:
                tempo_ate_pacote_chegar = random.uniform(2, 3) * v
                time.sleep(tempo_ate_pacote_chegar)

            self.canvas.itemconfig(rect_id, fill="yellow")
            self.status_var.set(f"{nome} escutando o canal...")
            self.log(f"{nome}: escutando canal para {packet}...")

            with self.transmitting_lock:
                canal_ocupado = len(self.transmitting_now) > 0

            if canal_ocupado:
                backoff_ocupado = random.uniform(0.8, 1.5) * v
                self.log(f"{nome}: Canal ocupado, aguardando {backoff_ocupado:.2f}s antes de tentar {packet} novamente.")
                self.canvas.itemconfig(rect_id, fill="gray")
                time.sleep(backoff_ocupado)
                continue

            time.sleep(0.02 * v)

            with self.transmitting_lock:
                self.transmitting_now.append(nome)

            time.sleep(0.05 * v)

            with self.transmitting_lock:
                num_transmitindo = len(self.transmitting_now)

            self.stats[nome]["tentativas"] += 1

            if num_transmitindo > 1:
                self.stats[nome]["colisoes"] += 1
                self.status_var.set("COLISÃO DETECTADA!")
                self.canvas.itemconfig(rect_id, fill="red")
                self.log(f"{nome}: Colisão ao tentar transmitir {packet}.")

                k += 1
                if k >= max_tentativas:
                    self.log(f"{nome}: Desistiu de transmitir {packet} após {max_tentativas} tentativas.")
                    with self.transmitting_lock:
                        if nome in self.transmitting_now:
                            self.transmitting_now.remove(nome)
                    self.canvas.itemconfig(rect_id, fill="gray")
                    self.status_var.set("Canal: Livre")
                    packet = None
                    continue

                R = random.randint(0, 2 ** k - 1)
                backoff = R * slot_time

                with self.transmitting_lock:
                    if nome in self.transmitting_now:
                        self.transmitting_now.remove(nome)

                self.status_var.set(f"{nome} em backoff: {backoff:.2f}s")
                self.canvas.itemconfig(rect_id, fill="gray")
                self.log(f"{nome}: Backoff de {backoff:.2f}s (k={k}) para {packet}")
                time.sleep(backoff)
                continue

            # Sucesso na transmissão
            self.status_var.set(f"{nome} transmitindo {packet}...")
            self.canvas.itemconfig(rect_id, fill="green")
            self.log(f"{nome}: Transmitindo {packet}...")
            time.sleep(0.5 * v)

            self.status_var.set(f"{nome} transmitiu com sucesso.")
            self.canvas.itemconfig(rect_id, fill="blue")
            self.stats[nome]["sucesso"] += 1
            self.log(f"{nome}: {packet} transmitido com sucesso.")
            time.sleep(0.3 * v)

            with self.transmitting_lock:
                if nome in self.transmitting_now:
                    self.transmitting_now.remove(nome)

            self.canvas.itemconfig(rect_id, fill="gray")
            self.status_var.set("Canal: Livre")

            packet = None  # Próximo pacote
            k = 0  # Resetar backoff

    def mostrar_estatisticas(self):
        self.log("\n=== ESTATÍSTICAS FINAIS ===")
        transmissores = []
        sucessos = []
        colisoes = []
        tentativas = []
        total_sucessos = 0
        total_colisoes = 0
        total_tentativas = 0

        for nome, dados in self.stats.items():
            tentativa = dados['tentativas']
            colisao = dados['colisoes']
            sucesso_calculado = tentativa - colisao
            self.log(f"{nome} - Tentativas: {tentativa}, Colisões: {colisao}, Sucessos (calculado): {sucesso_calculado}")
            transmissores.append(nome)
            sucessos.append(sucesso_calculado)
            colisoes.append(colisao)
            tentativas.append(tentativa)
            total_sucessos += sucesso_calculado
            total_colisoes += colisao
            total_tentativas += tentativa

        eficiencia = (total_sucessos / total_tentativas * 100) if total_tentativas > 0 else 0
        self.log("\n--- Totais ---")
        self.log(f"Total de Pacotes Enviados (Tentativas): {total_tentativas}")
        self.log(f"Total de Pacotes com Colisão: {total_colisoes}")
        self.log(f"Total de Pacotes com Sucesso: {total_sucessos}")
        self.log(f"Eficiência do Canal: {eficiencia:.2f}%")

        # Gráficos
        plt.figure(figsize=(12, 5))
        plt.subplot(1, 3, 1)
        plt.bar(transmissores, sucessos, color='blue')
        plt.title('Sucessos')
        plt.subplot(1, 3, 2)
        plt.bar(transmissores, colisoes, color='red')
        plt.title('Colisões')
        plt.subplot(1, 3, 3)
        plt.bar(transmissores, tentativas, color='orange')
        plt.title('Tentativas')
        plt.tight_layout()
        plt.show()

    def salvar_log(self):
        conteudo = self.log_text.get("1.0", tk.END).strip()
        if conteudo:
            with open("simulacao_log.txt", "w", encoding="utf-8") as f:
                f.write(conteudo)
            self.log("Log salvo em 'simulacao_log.txt'.")
        else:
            self.log("Nenhum log para salvar.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CSMACDSimulatorGUI(root)
    root.mainloop()
