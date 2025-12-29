package server

import (
	"context"
	"fmt"
	"net/http"
	"sync/atomic"
	"time"
)

// Server представляет HTTP сервер с поддержкой горутин
type Server struct {
	// router - мультиплексер для маршрутизации запросов
	router *http.ServeMux
	// requestCount - атомарный счетчик для подсчета запросов
	requestCount int64
	// server - базовый HTTP сервер
	server *http.Server
}

// NewServer создает новый HTTP сервер на заданном адресе
func NewServer(addr string) *Server {
	s := &Server{
		// Создаем мультиплексер для обработки разных маршрутов
		router: http.NewServeMux(),
	}

	// Настраиваем маршруты
	s.setupRoutes()

	// Создаем HTTP сервер
	s.server = &http.Server{
		Addr:    addr,
		Handler: s.router,
	}

	return s
}

// setupRoutes настраивает все маршруты сервера
func (s *Server) setupRoutes() {
	// Главная страница - обрабатывается в отдельной горутине
	s.router.HandleFunc("/", s.handleRoot)
	// Проверка здоровья сервера
	s.router.HandleFunc("/health", s.handleHealth)
	// Статистика сервера
	s.router.HandleFunc("/stats", s.handleStats)
}

// handleRoot обрабатывает запросы к корневому пути
func (s *Server) handleRoot(w http.ResponseWriter, r *http.Request) {
	// Атомарно увеличиваем счетчик запросов (потокобезопасно)
	count := atomic.AddInt64(&s.requestCount, 1)
	// Имитация обработки запроса
	time.Sleep(50 * time.Millisecond)
	// Возвращаем ответ
	fmt.Fprintf(w, "Hello! Request count: %d\n", count)
}

// handleHealth обрабатывает запросы проверки здоровья
func (s *Server) handleHealth(w http.ResponseWriter, r *http.Request) {
	// Возвращаем OK статус
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("OK"))
}

// handleStats обрабатывает запросы получения статистики
func (s *Server) handleStats(w http.ResponseWriter, r *http.Request) {
	// Читаем текущее значение счетчика
	count := atomic.LoadInt64(&s.requestCount)
	// Возвращаем статистику
	fmt.Fprintf(w, "Total requests: %d", count)
}

// Start запускает HTTP сервер в режиме прослушивания
func (s *Server) Start() error {
	return s.server.ListenAndServe()
}

// Stop останавливает сервер с graceful shutdown
func (s *Server) Stop(ctx context.Context) error {
	// Shutdown ждет завершения всех текущих запросов перед остановкой
	return s.server.Shutdown(ctx)
}

// GetRequestCount возвращает текущее количество обработанных запросов
func (s *Server) GetRequestCount() int64 {
	// Используем atomic.LoadInt64 для безопасного чтения
	return atomic.LoadInt64(&s.requestCount)
}

// ResetRequestCount сбрасывает счетчик запросов
func (s *Server) ResetRequestCount() {
	// Используем atomic.StoreInt64 для безопасной записи
	atomic.StoreInt64(&s.requestCount, 0)
}
