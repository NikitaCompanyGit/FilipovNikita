package async

import (
	"sync"
	"testing"
	"time"
)

// TestCounter проверяет потокобезопасность инкремента счетчика
func TestCounter(t *testing.T) {
	// Создаем новый счетчик
	counter := &Counter{}
	// WaitGroup для синхронизации горутин в тесте
	var wg sync.WaitGroup

	// Количество горутин для теста
	numGoroutines := 100
	// Каждая горутина будет делать несколько инкрементов
	incrementsPerGoroutine := 10

	// Запускаем множество горутин, которые конкурируют за доступ к счетчику
	for i := 0; i < numGoroutines; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for j := 0; j < incrementsPerGoroutine; j++ {
				counter.Increment()
			}
		}()
	}

	// Ждем завершения всех горутин
	wg.Wait()

	// Проверяем, что счетчик имеет правильное значение
	// Если не было гонок данных, число должно быть ровно numGoroutines * incrementsPerGoroutine
	expected := numGoroutines * incrementsPerGoroutine
	if counter.Value() != expected {
		t.Errorf("Expected counter value %d, got %d", expected, counter.Value())
	}
}

// TestProcessItems проверяет обработку элементов в отдельных горутинах
func TestProcessItems(t *testing.T) {
	// Массив элементов для обработки
	items := []int{1, 2, 3, 4, 5}
	// Слайс для сохранения обработанных элементов
	processed := make([]int, 0)
	// Мьютекс для защиты доступа к processed
	var mu sync.Mutex

	// Функция-обработчик
	processor := func(item int) {
		mu.Lock()
		defer mu.Unlock()
		processed = append(processed, item)
	}

	// Вызываем функцию обработки
	ProcessItems(items, processor)

	// Проверяем, что обработано правильное количество элементов
	if len(processed) != len(items) {
		t.Errorf("Expected %d processed items, got %d", len(items), len(processed))
	}

	// Проверяем, что все элементы были обработаны (независимо от порядка)
	itemMap := make(map[int]bool)
	for _, item := range processed {
		itemMap[item] = true
	}

	for _, item := range items {
		if !itemMap[item] {
			t.Errorf("Item %d was not processed", item)
		}
	}
}

// TestProcessItems_RaceCondition проверяет отсутствие гонок данных
// Запускается с флагом: go test -race
func TestProcessItems_RaceCondition(t *testing.T) {
	// Создаем большой массив элементов
	items := make([]int, 100)
	for i := 0; i < 100; i++ {
		items[i] = i
	}

	// Счетчик обработанных элементов
	var counter int
	// Мьютекс для защиты счетчика
	var mu sync.Mutex

	processor := func(item int) {
		mu.Lock()
		defer mu.Unlock()
		counter++
	}

	// Запускаем обработку
	ProcessItems(items, processor)

	// Проверяем результат
	if counter != 100 {
		t.Errorf("Expected 100 processed items, got %d", counter)
	}
}

// TestSimpleWorkerPool проверяет базовую функциональность пула воркеров
func TestSimpleWorkerPool(t *testing.T) {
	// Создаем пул с 3 воркерами
	pool := NewSimpleWorkerPool(3)
	// Запускаем воркеры
	pool.Start()

	// Количество задач
	numTasks := 10
	// Отправляем задачи
	go func() {
		for i := 1; i <= numTasks; i++ {
			pool.Submit(i)
		}
		pool.Stop()
	}()

	// Собираем результаты
	results := make(map[int]bool)
	for result := range pool.GetResults() {
		results[result] = true
	}

	// Проверяем, что получили все результаты
	if len(results) != numTasks {
		t.Errorf("Expected %d results, got %d", numTasks, len(results))
	}

	// Проверяем корректность вычислений (квадраты чисел)
	expectedSquares := []int{1, 4, 9, 16, 25, 36, 49, 64, 81, 100}
	for _, expected := range expectedSquares {
		if !results[expected] {
			t.Errorf("Expected result %d not found", expected)
		}
	}
}

// TestWorkerPool_Concurrent проверяет конкурентную работу пула
func TestWorkerPool_Concurrent(t *testing.T) {
	// Создаем пул с большим количеством воркеров
	pool := NewSimpleWorkerPool(10)
	pool.Start()

	numTasks := 1000

	// Отправляем много задач одновременно
	go func() {
		for i := 1; i <= numTasks; i++ {
			pool.Submit(i)
		}
		pool.Stop()
	}()

	// Собираем результаты
	resultCount := 0
	for range pool.GetResults() {
		resultCount++
	}

	// Проверяем, что получили все результаты
	if resultCount != numTasks {
		t.Errorf("Expected %d results, got %d", numTasks, resultCount)
	}
}

// BenchmarkCounter_Increment тестирует производительность инкремента
func BenchmarkCounter_Increment(b *testing.B) {
	counter := &Counter{}
	var wg sync.WaitGroup

	// Запускаем несколько горутин параллельно
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			counter.Increment()
		}()
	}
	wg.Wait()
}
