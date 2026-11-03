"""
Quantum Brain Engine (v9.0.0-OMEGA)
Математическое вероятностно-квантовое ядро гипотез и интерференции коммерческих стратегий.
"""

import numpy as np
from typing import List, Dict, Any, Tuple

class QuantumBrainEngine:
    def __init__(self, num_qubits: int = 4):
        """
        Инициализация квантового когнитивного регистра на num_qubits кубитах.
        Размерность пространства состояний: 2^num_qubits.
        """
        self.num_qubits = num_qubits
        self.dim = 2 ** num_qubits
        self.state_vector = np.zeros(self.dim, dtype=complex)
        self.state_vector[0] = 1.0  # Инициализация базисным вектором |0000...0>

    def apply_superposition(self) -> None:
        """
        Перевод гипотез и вариантов арбитража/контента в равновесную квантовую суперпозицию.
        Применяется оператор Адамара H^⊗n.
        """
        h = (1.0 / np.sqrt(2.0)) * np.array([[1.0, 1.0], [1.0, -1.0]], dtype=complex)
        operator = h
        for _ in range(self.num_qubits - 1):
            operator = np.kron(operator, h)
        self.state_vector = np.dot(operator, self.state_vector)

    def apply_interference(self, phase_shift_matrix: np.ndarray) -> None:
        """
        Интерференция смыслов: подавление рыночного шума, скама и конструктивная интерференция
        (усиление амплитуд) для прибыльных и валидированных связок.
        """
        if phase_shift_matrix.shape != (self.dim, self.dim):
            raise ValueError(f"Размерность матрицы интерференции должна быть ({self.dim}, {self.dim})")
        self.state_vector = np.dot(phase_shift_matrix, self.state_vector)
        norm = np.linalg.norm(self.state_vector)
        if norm > 0:
            self.state_vector /= norm

    def collapse_wave_function(self) -> str:
        """
        Коллапс волновой функции (измерение в базисе Z):
        Выбор оптимальной торговой стратегии с вероятностями P(i) = |psi_i|^2.
        """
        probabilities = np.abs(self.state_vector) ** 2
        # Нормализация на случай численной погрешности
        prob_sum = np.sum(probabilities)
        if prob_sum > 0:
            probabilities = probabilities / prob_sum
        collapsed_idx = np.random.choice(len(probabilities), p=probabilities)
        return format(collapsed_idx, f'0{self.num_qubits}b')

    def construct_interference_filter(self, hypothesis_scores: List[float], noise_flags: List[bool]) -> np.ndarray:
        """
        Формирует унитарную фазовую диагональную матрицу интерференции:
        - Подавление (деструктивная интерференция): амплитуды сомнительных/шумных гипотез гасятся e^(-i*pi/2) с демпфированием.
        - Усиление (конструктивная интерференция): амплитуды высокомаржинальных связок поворачиваются в фазу максимальной когерентности.
        """
        phases = np.zeros(self.dim, dtype=complex)
        for i in range(self.dim):
            score = hypothesis_scores[i] if i < len(hypothesis_scores) else 50.0
            is_noise = noise_flags[i] if i < len(noise_flags) else False
            
            if is_noise or score < 50.0:
                # Деструктивное ослабление
                phases[i] = np.exp(-1j * np.pi * 0.75) * 0.15
            else:
                # Конструктивное усиление пропорционально оценке FinOps
                boost = (score / 100.0) * 1.5
                theta = (score / 100.0) * (np.pi / 4.0)
                phases[i] = np.exp(1j * theta) * boost
                
        # Диагональный оператор интерференции
        diag_matrix = np.diag(phases)
        return diag_matrix

    def evaluate_hypotheses(self, hypotheses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Полный квантово-когнитивный цикл оценки набора рыночных гипотез:
        1. Инициализация |0>
        2. Суперпозиция (Адамар)
        3. Фазовая интерференция на основе FinOps скоринга и стоп-факторов
        4. Коллапс волновой функции к победившей стратегии
        """
        self.state_vector = np.zeros(self.dim, dtype=complex)
        self.state_vector[0] = 1.0
        
        self.apply_superposition()
        
        scores = [h.get("finops_score", 50.0) for h in hypotheses]
        noises = [h.get("is_stop_factor", False) for h in hypotheses]
        
        filter_matrix = self.construct_interference_filter(scores, noises)
        self.apply_interference(filter_matrix)
        
        probabilities = np.abs(self.state_vector) ** 2
        collapsed_binary = self.collapse_wave_function()
        winner_idx = int(collapsed_binary, 2)
        
        if winner_idx < len(hypotheses):
            winner = hypotheses[winner_idx]
        else:
            winner = hypotheses[0]
            
        return {
            "num_qubits": self.num_qubits,
            "collapsed_state": collapsed_binary,
            "winner_index": winner_idx,
            "winner_hypothesis": winner,
            "quantum_confidence": float(probabilities[winner_idx] if winner_idx < len(probabilities) else 0.0),
            "distribution": [float(p) for p in probabilities[:len(hypotheses)]]
        }
