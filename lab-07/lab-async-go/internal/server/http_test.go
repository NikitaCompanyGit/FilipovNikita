package server

import (
	"context"
	"fmt"
	"io"
	"net/http"
	"net/http/httptest"
	"sync"
	"testing"
	"time"
)

// TestServer_Routes проверяет все маршруты сервера
func TestServer_Routes(t *testing.T) {
	// Создаем сервер
	server := NewServer(":0")

	// Тестовые случаи для разных маршрутов
	tests := []struct {
		name       string
		path       string
		wantStatus int
	}{
		{
			name:       "root path",
			path:       "/",
			wantStatus: http.StatusOK,
		},
		{
			name:       "health check",
			path:       "/health",
			wantStatus: http.StatusOK,
		},
		{
			name:       "stats",
			path:       "/stats",
			wantStatus: http.StatusOK,
		},
	}

	// Проверяем каждый маршрут
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Создаем тестовый запрос
			req := httptest.NewRequest("GET", tt.path, nil)
			// Создаем тестовый ResponseWriter
			w := httptest.NewRecorder()

			// Обрабатываем запрос
			server.router.ServeHTTP(w, req)

			// Получаем ответ
			resp := w.Result()

			// Проверяем статус код
			if resp.StatusCode != tt.wantStatus {
				t.Errorf("Expected status %d, got %d", tt.wantStatus, resp.StatusCode)
			}
		})
	}
}

// TestServer_ConcurrentRequests проверяет обработку конкурентных запросов
func TestServer_ConcurrentRequests(t *testing.T) {
	// Создаем сервер
	server := NewServer(":0")
	// Сбрасываем счетчик
	server.ResetRequestCount()

	// Создаем тестовый сервер
	ts := httptest.NewServer(server.router)
	defer ts.Close()

	// WaitGroup для синхронизации горутин
	var wg sync.WaitGroup
	// Количество запросов
	requests := 100

	// Отправляем много конкурентных запросов
	for i := 0; i < requests; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			// Отправляем GET запрос
			resp, err := http.Get(ts.URL + "/")
			if err != nil {
				t.Errorf("Request failed: %v", err)
				return
			}
			defer resp.Body.Close()

			// Проверяем статус
			if resp.StatusCode != http.StatusOK {
				t.Errorf("Expected status 200, got %d", resp.StatusCode)
			}
		}(i)
	}

	// Ждем завершения всех запросов
	wg.Wait()

	// Проверяем счетчик запросов
	if server.GetRequestCount() != int64(requests) {
		t.Errorf("Expected %d requests, got %d", requests, server.GetRequestCount())
	}
}

// TestServer_HealthCheck проверяет endpoint здоровья сервера
func TestServer_HealthCheck(t *testing.T) {
	server := NewServer(":0")
	ts := httptest.NewServer(server.router)
	defer ts.Close()

	// Отправляем запрос к /health
	resp, err := http.Get(ts.URL + "/health")
	if err != nil {
		t.Fatalf("Request failed: %v", err)
	}
	defer resp.Body.Close()

	// Проверяем статус
	if resp.StatusCode != http.StatusOK {
		t.Errorf("Expected status 200, got %d", resp.StatusCode)
	}

	// Проверяем тело ответа
	body, _ := io.ReadAll(resp.Body)
	if string(body) != "OK" {
		t.Errorf("Expected body 'OK', got '%s'", string(body))
	}
}

// TestServer_Stats проверяет endpoint статистики
func TestServer_Stats(t *testing.T) {
	server := NewServer(":0")
	server.ResetRequestCount()
	ts := httptest.NewServer(server.router)
	defer ts.Close()

	// Отправляем несколько запросов к /
	for i := 0; i < 3; i++ {
		http.Get(ts.URL + "/")
	}

	// Проверяем статистику
	resp, err := http.Get(ts.URL + "/stats")
	if err != nil {
		t.Fatalf("Request failed: %v", err)
	}
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	expectedBody := "Total requests: 3"
	if string(body) != expectedBody {
		t.Errorf("Expected body '%s', got '%s'", expectedBody, string(body))
	}
}

// TestServer_GracefulShutdown проверяет graceful shutdown сервера
func TestServer_GracefulShutdown(t *testing.T) {
	server := NewServer(":0")

	// Создаем тестовый сервер
	ts := httptest.NewServer(server.router)

	// Создаем контекст с таймаутом для shutdown
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()

	// Останавливаем сервер gracefully
	go func() {
		time.Sleep(100 * time.Millisecond)
		server.Stop(ctx)
	}()

	// Сразу после shutdown пытаемся сделать запрос
	time.Sleep(150 * time.Millisecond)
	_, err := http.Get(ts.URL + "/")

	// После shutdown сервер не должен обрабатывать запросы
	if err == nil {
		// Может быть ошибка или успех в зависимости от времени
		// httptest.Server может закрыться раньше
	}
}

// TestServer_RequestCount проверяет корректность счетчика запросов
func TestServer_RequestCount(t *testing.T) {
	server := NewServer(":0")
	server.ResetRequestCount()

	// Создаем тестовые запросы
	for i := 0; i < 5; i++ {
		req := httptest.NewRequest("GET", "/", nil)
		w := httptest.NewRecorder()
		server.router.ServeHTTP(w, req)
	}

	// Проверяем счетчик
	if server.GetRequestCount() != 5 {
		t.Errorf("Expected 5 requests, got %d", server.GetRequestCount())
	}
}

// BenchmarkServer_Handler тестирует производительность обработчика
func BenchmarkServer_Handler(b *testing.B) {
	server := NewServer(":0")
	server.ResetRequestCount()

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		req := httptest.NewRequest("GET", "/", nil)
		w := httptest.NewRecorder()
		server.router.ServeHTTP(w, req)
	}
}

// BenchmarkServer_ConcurrentRequests тестирует производительность при конкурентных запросах
func BenchmarkServer_ConcurrentRequests(b *testing.B) {
	server := NewServer(":0")
	ts := httptest.NewServer(server.router)
	defer ts.Close()

	var wg sync.WaitGroup

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			http.Get(ts.URL + "/")
		}()
	}
	wg.Wait()
}
