package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"sync"
	"time"
)

func main() {
	fmt.Println("=== Лабораторная работа: Асинхронное программирование в Go ===")

	// Демонстрация всех паттернов из части 1
	var wg sync.WaitGroup

	// 1. Базовые горутины
	wg.Add(1)
	go func() {
		defer wg.Done()
		fmt.Println("\n1. Базовые горутины и WaitGroup:")
		demoBasicGoroutines()
	}()

	// 2. Каналы и select
	wg.Add(1)
	go func() {
		defer wg.Done()
		fmt.Println("\n2. Буферизованные каналы и select:")
		demoChannelsSelect()
	}()

	// 3. Worker Pool
	wg.Add(1)
	go func() {
		defer wg.Done()
		fmt.Println("\n3. Worker Pool паттерн:")
		demoWorkerPool()
	}()

	// 4. Fan-out/Fan-in
	wg.Add(1)
	go func() {
		defer wg.Done()
		fmt.Println("\n4. Fan-out/Fan-in паттерн:")
		demoFanOutFanIn()
	}()

	wg.Wait()

	// 5. HTTP сервер (можно запустить в отдельном окне для нагрузочного тестирования)
	fmt.Println("\n5. Многопоточный HTTP сервер:")
	fmt.Println("Для запуска сервера раскомментируйте строку ниже")
	// startHTTPServer()
}

// demoBasicGoroutines демонстрирует работу базовых горутин с WaitGroup
func demoBasicGoroutines() {
	// WaitGroup используется для синхронизации и ожидания завершения всех горутин
	var wg sync.WaitGroup

	// Запускаем 5 горутин
	for i := 1; i <= 5; i++ {
		// Add(1) увеличивает счетчик ожидаемых горутин
		wg.Add(1)
		go func(id int) {
			// Done() уменьшает счетчик после завершения горутины
			defer wg.Done()
			fmt.Printf("  Горутина %d: запущена\n", id)
			time.Sleep(time.Duration(id*100) * time.Millisecond)
			fmt.Printf("  Горутина %d: завершена\n", id)
		}(i)
	}

	// Wait() блокирует выполнение до тех пор, пока счетчик не станет нулевым
	wg.Wait()
	fmt.Println("  Все горутины завершили работу")
}

// demoChannelsSelect демонстрирует работу буферизованных каналов и select
func demoChannelsSelect() {
	// Буферизованный канал с размером буфера 3
	ch := make(chan int, 3)

	// Горутина-продюсер отправляет значения в канал
	go func() {
		for i := 0; i < 5; i++ {
			ch <- i
			fmt.Printf("  Продюсер отправил: %d\n", i)
			time.Sleep(100 * time.Millisecond)
		}
		close(ch)
		fmt.Println("  Продюсер завершил работу")
	}()

	// Горутина-консьюмер читает из канала с таймаутом
	go func() {
		for {
			select {
			case val, ok := <-ch:
				// Если канал закрыт, ok будет false
				if !ok {
					fmt.Println("  Консьюмер: канал закрыт")
					return
				}
				fmt.Printf("  Консьюмер получил: %d\n", val)
				time.Sleep(200 * time.Millisecond)

			case <-time.After(1 * time.Second):
				// Таймаут срабатывает если нет данных в течение 1 секунды
				fmt.Println("  Консьюмер: истек таймаут ожидания")
			}
		}
	}()

	// Даем время для завершения горутин
	time.Sleep(3 * time.Second)
}

// demoWorkerPool демонстрирует паттерн Worker Pool
func demoWorkerPool() {
	// Количество воркеров в пуле
	numWorkers := 3
	// Количество задач для обработки
	numTasks := 10

	// Каналы для задач и результатов
	tasks := make(chan int, numTasks)
	results := make(chan string, numTasks)

	// WaitGroup для отслеживания завершения всех воркеров
	var wg sync.WaitGroup

	// Запуск воркеров
	for i := 1; i <= numWorkers; i++ {
		wg.Add(1)
		go func(workerID int) {
			// Done вызывается при завершении работы воркера
			defer wg.Done()
			// Воркер читает задачи из канала до его закрытия
			for task := range tasks {
				fmt.Printf("  Воркер %d обрабатывает задачу %d\n", workerID, task)
				time.Sleep(200 * time.Millisecond)
				results <- fmt.Sprintf("Задача %d обработана воркером %d", task, workerID)
			}
			fmt.Printf("  Воркер %d завершил работу\n", workerID)
		}(i)
	}

	// Отправка задач в канал
	go func() {
		for i := 1; i <= numTasks; i++ {
			tasks <- i
		}
		// Закрытие канала задач сигнализирует воркерам об окончании работы
		close(tasks)
	}()

	// Горутина для закрытия канала результатов после завершения всех воркеров
	go func() {
		wg.Wait()
		close(results)
	}()

	// Обработка результатов
	for result := range results {
		fmt.Printf("  %s\n", result)
	}
	fmt.Println("  Все задачи обработаны")
}

// demoFanOutFanIn демонстрирует паттерн Fan-out/Fan-in
func demoFanOutFanIn() {
	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
	defer cancel()

	// Fan-out: несколько продюсеров
	ch1 := producer(ctx, 1)
	ch2 := producer(ctx, 2)

	// Fan-in: объединение результатов
	results := merge(ctx, ch1, ch2)

	// Обработка результатов
	resultCount := 0
	for result := range results {
		fmt.Printf("  Результат: %d\n", result)
		resultCount++
	}
	fmt.Printf("  Получено %d результатов\n", resultCount)
}

// producer создает горутину-продюсер, отправляющую данные в канал
func producer(ctx context.Context, id int) <-chan int {
	out := make(chan int)
	go func() {
		defer close(out)
		for i := 0; i < 3; i++ {
			select {
			case out <- i*10 + id:
				fmt.Printf("  Продюсер %d отправил значение\n", id)
			case <-ctx.Done():
				fmt.Printf("  Продюсер %d отменен\n", id)
				return
			}
			time.Sleep(300 * time.Millisecond)
		}
	}()
	return out
}

// merge объединяет данные из нескольких каналов в один
func merge(ctx context.Context, inputs ...<-chan int) <-chan int {
	var wg sync.WaitGroup
	out := make(chan int)

	// Функция для чтения из одного входного канала
	output := func(c <-chan int) {
		defer wg.Done()
		for {
			select {
			case n, ok := <-c:
				if !ok {
					return
				}
				select {
				case out <- n:
				case <-ctx.Done():
					return
				}
			case <-ctx.Done():
				return
			}
		}
	}

	// Запускаем горутины для чтения из каждого входного канала
	wg.Add(len(inputs))
	for _, input := range inputs {
		go output(input)
	}

	// Горутина для закрытия выходного канала после завершения всех входных
	go func() {
		wg.Wait()
		close(out)
	}()

	return out
}

// startHTTPServer запускает многопоточный HTTP сервер
func startHTTPServer() {
	mux := http.NewServeMux()

	// Обработчик для корневого пути
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "Hello! Текущее время: %s\n", time.Now().Format("15:04:05"))
	})

	// Обработчик для проверки здоровья сервера
	mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("OK"))
	})

	server := &http.Server{
		Addr:    ":8080",
		Handler: mux,
	}

	// Запуск сервера в отдельной горутине
	go func() {
		log.Println("Сервер запущен на http://localhost:8080")
		if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("Ошибка сервера: %v", err)
		}
	}()

	// Канал для graceful shutdown
	stop := make(chan struct{})
	<-stop

	// Graceful shutdown с таймаутом
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := server.Shutdown(ctx); err != nil {
		log.Printf("Ошибка при остановке сервера: %v", err)
	}

	log.Println("Сервер остановлен")
}
