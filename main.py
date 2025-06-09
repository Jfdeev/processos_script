import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QComboBox, QPushButton, QProgressBar, QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import QTimer

# Lista de processos (nome e tempo de execução em segundos)
PROCESSOS = [
    {"name": "Flash", "time": 5},
    {"name": "Zoom", "time": 7},
    {"name": "Senna", "time": 4},
    {"name": "Sarvitar", "time": 8},
]

QUANTUM = 1  
INTERVALO = 100  

class SimuladorEscalonamento(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Simulador de Escalonamento de CPU')
        self.setFixedSize(520, 400)

        layout_principal = QVBoxLayout()

        # Combobox para selecionar o algoritmo
        layout_selecao = QHBoxLayout()
        layout_selecao.addWidget(QLabel('Algoritmo:'))
        self.algoritmo_combo = QComboBox()
        self.algoritmo_combo.addItems(['FIFO', 'Round Robin', 'SJF'])
        layout_selecao.addWidget(self.algoritmo_combo)
        layout_principal.addLayout(layout_selecao)

        # Botões de iniciar e resetar
        layout_botoes = QHBoxLayout()
        self.btn_iniciar = QPushButton('Iniciar')
        self.btn_iniciar.clicked.connect(self.iniciar_simulacao)
        layout_botoes.addWidget(self.btn_iniciar)

        self.btn_resetar = QPushButton('Resetar')
        self.btn_resetar.setEnabled(False)
        self.btn_resetar.clicked.connect(self.resetar_simulacao)
        layout_botoes.addWidget(self.btn_resetar)
        layout_principal.addLayout(layout_botoes)

        # Barras de progresso dos processos
        self.barras = []
        for proc in PROCESSOS:
            layout_principal.addWidget(QLabel(proc['name']))
            barra = QProgressBar()
            barra.setMaximum(proc['time'] * 1000)
            barra.setValue(0)
            self.barras.append(barra)
            layout_principal.addWidget(barra)

        # Label para exibir o "vencedor"
        self.label_vencedor = QLabel('')
        layout_principal.addWidget(self.label_vencedor)

        self.setLayout(layout_principal)

        self.timer = QTimer()
        self.timer.timeout.connect(self.executar_tick)

    def iniciar_simulacao(self):
        self.btn_iniciar.setEnabled(False)
        self.btn_resetar.setEnabled(True)

        self.tempos_originais = [p['time'] * 1000 for p in PROCESSOS]
        self.tempos_restantes = list(self.tempos_originais)
        self.vencedor_exibido = False
        self.idx_atual = 0

        algoritmo = self.algoritmo_combo.currentText()
        if algoritmo in ['FIFO', 'Round Robin']:
            self.ordem = list(range(len(self.tempos_restantes)))
        else:  # SJF
            self.ordem = sorted(range(len(self.tempos_restantes)), key=lambda i: self.tempos_restantes[i])

        # Resetar todas as barras
        for barra in self.barras:
            barra.setValue(0)
        self.label_vencedor.clear()

        self.timer.start(INTERVALO)

    def executar_tick(self):
        if not self.ordem:
            self.parar_simulacao()
            return

        algoritmo = self.algoritmo_combo.currentText()
        idx = self.ordem[self.idx_atual]

        # Round Robin usa fatias, os outros vão direto
        if algoritmo == 'Round Robin':
            slice_ms = min(QUANTUM * 1000, self.tempos_restantes[idx])
        else:
            slice_ms = self.tempos_restantes[idx]

        decorrido = min(INTERVALO, slice_ms)
        self.tempos_restantes[idx] -= decorrido

        progresso = self.tempos_originais[idx] - self.tempos_restantes[idx]
        self.barras[idx].setValue(int(progresso))

        if self.tempos_restantes[idx] <= 0:
            self.tempos_restantes[idx] = 0
            if not self.vencedor_exibido:
                nome = PROCESSOS[idx]['name']
                self.label_vencedor.setText(f'🏆 Vencedor: {nome} 🏆')
                QMessageBox.information(self, 'Resultado', f'O vencedor é: {nome}!')
                self.vencedor_exibido = True
            self.ordem.remove(idx)

            # Atualiza o índice dependendo do algoritmo
            if algoritmo == 'Round Robin' and self.ordem:
                self.idx_atual %= len(self.ordem)
            else:
                self.idx_atual = 0
            if not self.ordem:
                self.parar_simulacao()
        else:
            if algoritmo == 'Round Robin':
                self.idx_atual = (self.idx_atual + 1) % len(self.ordem)

    def parar_simulacao(self):
        self.timer.stop()
        self.btn_iniciar.setEnabled(True)

    def resetar_simulacao(self):
        self.timer.stop()
        self.btn_iniciar.setEnabled(True)
        self.btn_resetar.setEnabled(False)
        self.ordem = []
        self.label_vencedor.clear()
        for barra in self.barras:
            barra.setValue(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = SimuladorEscalonamento()
    janela.show()
    sys.exit(app.exec_())
