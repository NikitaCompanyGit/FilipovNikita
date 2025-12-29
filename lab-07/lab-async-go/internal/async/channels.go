package async

import (
	"context"
	"time"
)

// MergeChannels объединяет несколько входных каналов в один выходной канал
func MergeChannels(ctx context.Context, chs ...<-chan int) <-chan int {
	// Выходной канал для результатов
	out := make(chan int)

	// Для каждого входного канала запускаем отдельную горутину
	for _, ch := range chs {
		go func(c <-chan int) {
			// defer close(out) будет неправильным, так как нужно закрыть канал
			// только после всех горутин, используем sync.WaitGroup в callers
			for {
				select {
				// Читаем из входного канала
				case val, ok := <-c:
					// Если канал закрыт, выходим из горутины
					if !ok {
						return
					}
					// Отправляем значение в выходной канал
					select {
					case out <- val:
					case <-ctx.Done():
						return
					}
				// Если контекст отменен, выходим
				case <-ctx.Done():
					return
				}
			}
		}(ch)
	}

	return out
}

// BufferedChannelProcessor обрабатывает данные из входного канала и отправляет в выходной
func BufferedChannelProcessor(input <-chan int, bufferSize int) <-chan int {
	// Буферизованный выходной канал
	output := make(chan int, bufferSize)

	// Горутина для обработки данных
	go func() {
		// Закрываем выходной канал когда входной исчерпается
		defer close(output)
		// Читаем из входного канала
		for val := range input {
			// Простая обработка - умножаем на 2
			output <- val * 2
		}
	}()

	return output
}

// SelectExample демонстрирует использование select для работы с несколькими каналами
func SelectExample(ctx context.Context, ch1 <-chan int, ch2 <-chan int) <-chan int {
	out := make(chan int)

	go func() {
		defer close(out)
		for {
			select {
			// Готовы к получению из первого канала
			case val, ok := <-ch1:
				if !ok {
					return
				}
				select {
				case out <- val:
				case <-ctx.Done():
					return
				}
			// Готовы к получению из второго канала
			case val, ok := <-ch2:
				if !ok {
					return
				}
				select {
				case out <- val:
				case <-ctx.Done():
					return
				}
			// Таймаут - выполняется если долго нет данных
			case <-time.After(1 * time.Second):
				// Можно логировать таймауты
			// Отмена через контекст
			case <-ctx.Done():
				return
			}
		}
	}()

	return out
}

// RangeOverChannel демонстрирует итерацию по закрытому каналу
func RangeOverChannel(ch <-chan int) int {
	// Переменная для накопления результата
	sum := 0
	// for range читает из канала до его закрытия
	for val := range ch {
		sum += val
	}
	return sum
}
