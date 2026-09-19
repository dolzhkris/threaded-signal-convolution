import numpy as np
import threading
import time
import matplotlib.pyplot as plt

class ThreadedConvolution:
    def __init__(self, N=100, fc=0.1, num_threads=4):
        self.N = N
        self.fc = fc
        self.num_threads = num_threads
        
        # Импульсная характеристика
        n = np.arange(1, N + 1)
        self.h = np.sin(2 * np.pi * fc * n) / (np.pi * fc * n)
        self.h = self.h / np.sum(np.abs(self.h))  # нормализация
        
        self.threads = []
        self.y = None
        self.lock = threading.Lock()
        
    def worker_thread(self, x, start_k, end_k, thread_id):
        """Функция потока для обработки диапазона"""
        y_part = np.zeros(end_k - start_k)
        
        for i, k in enumerate(range(start_k, end_k)):
            sum_val = 0.0
            for n in range(1, self.N + 1):
                idx = k - n
                if idx >= 0:
                    sum_val += self.h[n-1] * x[idx]
            y_part[i] = sum_val
        
        # Безопасно сохраняем результат
        with self.lock:
            if self.y is None:
                self.y = np.zeros(len(x))
            self.y[start_k:end_k] = y_part
        
        print(f"Поток {thread_id} завершил диапазон [{start_k}, {end_k})")
    
    def parent_thread(self, x):
        """Родительский поток управляет дочерними"""
        print(f"Родительский поток запускает {self.num_threads} дочерних потоков")
        
        chunk_size = len(x) // self.num_threads
        
        # Запускаем потоки
        for i in range(self.num_threads):
            start_k = i * chunk_size
            end_k = (i + 1) * chunk_size if i < self.num_threads - 1 else len(x)
            
            t = threading.Thread(
                target=self.worker_thread,
                args=(x, start_k, end_k, i),
                name=f"Worker-{i}"
            )
            self.threads.append(t)
            t.start()
            print(f"Запущен поток {i} для k=[{start_k}, {end_k})")
        
        # Ожидаем завершения всех потоков
        print("\nОжидание завершения потоков...")
        for i, t in enumerate(self.threads):
            t.join()
            print(f"Поток {i} завершен")
        
        print("\nВсе потоки завершены")
        return self.y
    
    def run(self):
        """Запуск системы"""
        t, x = self.generate_signal(600)
        
        print("Последовательная обработка...")
        start = time.time()
        y_seq = self.convolve_seq(x)
        print(f"Время: {time.time() - start:.4f} сек")
        
        print("\nПараллельная обработка (потоки)...")
        start = time.time()
        y_par = self.parent_thread(x)
        print(f"Время: {time.time() - start:.4f} сек")
        
        # Визуализация
        self.plot(t, x, y_par)
        
        return y_seq, y_par
      
def generate_signal(self, length):
        t = np.linspace(0, 1, length)
        x = np.sin(2 * np.pi * 5 * t) + 0.5 * np.sin(2 * np.pi * 50 * t)
        return t, x
    
    def convolve_seq(self, x):
        y = np.zeros(len(x))
        for k in range(len(x)):
            for n in range(1, self.N + 1):
                idx = k - n
                if idx >= 0:
                    y[k] += self.h[n-1] * x[idx]
        return y
    
    def plot(self, t, x, y):
        plt.figure(figsize=(10, 6))
        
        plt.subplot(3, 1, 1)
        plt.plot(t, x, 'b-')
        plt.title('Исходный сигнал')
        plt.grid(True)
        
        plt.subplot(3, 1, 2)
        plt.plot(t, y, 'r-')
        plt.title('После НЧ-фильтра')
        plt.grid(True)
        
        plt.subplot(3, 1, 3)
        n = np.arange(1, self.N + 1)
        plt.stem(n, self.h, 'g-')
        plt.title('Импульсная характеристика h(n)')
        plt.grid(True)
        
        plt.tight_layout()
        plt.show()

# Запуск
if __name__ == "__main__":
    processor = ThreadedConvolution(num_threads=4)
    processor.run()
