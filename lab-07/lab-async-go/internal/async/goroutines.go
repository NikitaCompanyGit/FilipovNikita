package async

import (
	"sync"
	"time"
)

// Counter - структура для безопасного инкремента счетчика из нескольких горутин
type Counter struct {
	// mu - мьютекс для синхронизации доступа к value
	mu sync.Mutex
	// value - само значение счетчика
	value int
}

// Increment увеличивает значение счетчика на 1 в потокобезопасном режиме
func (c *Counter) Increment() {
	// Блокируем доступ к критической секции
	c.mu.Lock()
	defer c.mu.Unlock()
	c.value++
}

// Value возвращает текущее значение счетчика
func (c *Counter) Value() int {
	// Читаем значение с защитой мьютекса
	c.mu.Lock()
	defer c.mu.Unlock()
	return c.value
}

// ProcessItems запускает несколько горутин для обработки массива элементов
func ProcessItems(items []int, processor func(int)) {
	// WaitGroup позволяет дождаться завершения всех горутин
	var wg sync.WaitGroup

	// Для каждого элемента запускаем отдельную горутину
	for _, item := range items {
		// Add(1) добавляет одну горутину к отслеживанию
		wg.Add(1)
		go func(i int) {
			// Done вызывается в конце горутины для уменьшения счетчика
			defer wg.Done()
			// Вызываем функцию-обработчик для элемента
			processor(i)
			// Имитация работы
			time.Sleep(10 * time.Millisecond)
		}(item)
	}

	// Wait блокирует текущую горутину до завершения всех отслеживаемых
	wg.Wait()
}

// SimpleWorkerPool - простая реализация пула воркеров
type SimpleWorkerPool struct {
	// workers - количество воркеров в пуле
	workers int
	// tasks - канал входящих задач
	tasks chan int
	// results - канал результатов
	results chan int
	// wg - для синхронизации завершения воркеров
	wg sync.WaitGroup
}

// NewSimpleWorkerPool создает новый пул воркеров
func NewSimpleWorkerPool(workers int) *SimpleWorkerPool {
	return &SimpleWorkerPool{
		workers: workers,
		// Буферизованные каналы для асинхронной обработки
		tasks:   make(chan int, workers*2),
		results: make(chan int, workers*2),
	}
}

// Start запускает воркеры пула
func (wp *SimpleWorkerPool) Start() {
	// Запускаем нужное количество воркеров
	for i := 0; i < wp.workers; i++ {
		wp.wg.Add(1)
		go func() {
			// Done вызывается когда воркер завершает работу
			defer wp.wg.Done()
			// Воркер читает задачи из канала до его закрытия
			for task := range wp.tasks {
				// Простая обработка - возвращаем квадрат числа
				wp.results <- task * task
			}
		}()
	}
}

// Submit добавляет задачу в очередь
func (wp *SimpleWorkerPool) Submit(task int) {
	wp.tasks <- task
}

// GetResults возвращает канал результатов
func (wp *SimpleWorkerPool) GetResults() <-chan int {
	return wp.results
}

// Stop останавливает пул и закрывает каналы
func (wp *SimpleWorkerPool) Stop() {
	// Закрываем канал задач, сигнализируя воркерам об окончании
	close(wp.tasks)
	// Ждем завершения всех воркеров
	wp.wg.Wait()
	// Закрываем канал результатов
	close(wp.results)
}
