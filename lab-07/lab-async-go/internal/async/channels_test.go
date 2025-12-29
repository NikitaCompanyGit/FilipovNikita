package async

import (
	"context"
	"testing"
	"time"
)

// TestMergeChannels проверяет объединение данных из нескольких каналов
func TestMergeChannels(t *testing.T) {
	// Создаем контекст с таймаутом
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()

	// Создаем два входных канала
	ch1 := make(chan int)
	ch2 := make(chan int)

	// Горутина для отправки данных в первый канал
	go func() {
		defer close(ch1)
		for i := 0; i < 3; i++ {
			ch1 <- i
		}
	}()

	// Горутина для отправки данных во второй канал
	go func() {
		defer close(ch2)
		for i := 3; i < 6; i++ {
			ch2 <- i
		}
	}()

	// Объединяем каналы
	merged := MergeChannels(ctx, ch1, ch2)

	// Собираем результаты
	var results []int
	// Нужно закрыть выходной канал после завершения всех входных
	go func() {
		for val := range merged {
			results = append(results, val)
		}
	}()

	// Ждем завершения с таймаутом
	time.Sleep(1 * time.Second)

	// Проверяем, что получили все значения
	if len(results) != 6 {
		t.Errorf("Expected 6 values, got %d", len(results))
	}
}

// TestBufferedChannelProcessor проверяет обработку данных через буфер
func TestBufferedChannelProcessor(t *testing.T) {
	// Создаем входной канал и отправляем в него данные
	input := make(chan int, 5)

	for i := 1; i <= 5; i++ {
		input <- i
	}
	close(input)

	// Обрабатываем данные с размером буфера 3
	output := BufferedChannelProcessor(input, 3)

	// Ожидаемые результаты (входные значения умноженные на 2)
	expected := []int{2, 4, 6, 8, 10}
	var results []int

	// Читаем результаты из выходного канала
	for val := range output {
		results = append(results, val)
	}

	// Проверяем количество результатов
	if len(results) != len(expected) {
		t.Errorf("Expected %d results, got %d", len(expected), len(results))
	}

	// Проверяем каждое значение
	for i, val := range results {
		if val != expected[i] {
			t.Errorf("Expected %d at position %d, got %d", expected[i], i, val)
		}
	}
}

// TestChannelTimeout проверяет обработку таймаутов при работе с каналами
func TestChannelTimeout(t *testing.T) {
	// Создаем пустой канал
	ch := make(chan int)

	// Пытаемся читать с таймаутом
	select {
	case <-ch:
		// Не должны попасть сюда
		t.Error("Should not receive from channel")
	case <-time.After(100 * time.Millisecond):
		// Ожидаемое поведение - таймаут сработал
	}
}

// TestSelectExample проверяет использование select с несколькими каналами
func TestSelectExample(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()

	// Создаем два входных канала
	ch1 := make(chan int)
	ch2 := make(chan int)

	// Заполняем каналы данными в отдельных горутинах
	go func() {
		defer close(ch1)
		ch1 <- 10
		ch1 <- 20
	}()

	go func() {
		defer close(ch2)
		ch2 <- 30
		ch2 <- 40
	}()

	// Вызываем функцию с select
	result := SelectExample(ctx, ch1, ch2)

	// Собираем результаты
	var results []int
	for val := range result {
		results = append(results, val)
	}

	// Проверяем, что получили все значения
	if len(results) != 4 {
		t.Errorf("Expected 4 results, got %d", len(results))
	}
}

// TestRangeOverChannel проверяет итерацию по каналу
func TestRangeOverChannel(t *testing.T) {
	// Создаем канал и отправляем данные
	ch := make(chan int)

	go func() {
		defer close(ch)
		for i := 1; i <= 5; i++ {
			ch <- i
		}
	}()

	// Вычисляем сумму через функцию
	sum := RangeOverChannel(ch)

	// Проверяем результат (1+2+3+4+5 = 15)
	expected := 15
	if sum != expected {
		t.Errorf("Expected sum %d, got %d", expected, sum)
	}
}

// BenchmarkChannelCommunication тестирует производительность коммуникации через каналы
func BenchmarkChannelCommunication(b *testing.B) {
	ch := make(chan int, b.N)

	// Горутина для чтения из канала
	go func() {
		for range ch {
		}
	}()

	b.ResetTimer()
	// Отправляем много значений
	for i := 0; i < b.N; i++ {
		ch <- i
	}
	close(ch)
}
