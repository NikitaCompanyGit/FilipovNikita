export default function HomePage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[65vh] text-center space-y-12 py-10">
      <section className="space-y-6 max-w-3xl">
        <h1 className="text-5xl font-black text-slate-100 tracking-tight leading-none">
          Проектирование и разработка архитектуры ПО
        </h1>
        <p className="text-lg text-slate-400 leading-relaxed max-w-2xl mx-auto">
          Привет! Меня зовут Никита. Я специализируюсь на создании бэкенд-сервисов, интеграции систем и выстраивании CI/CD процессов.
        </p>
        <div className="pt-4">
          <a 
            href="/projects" 
            className="inline-block px-8 py-3.5 bg-violet-600 text-white font-bold rounded-2xl shadow-lg shadow-violet-500/20 hover:bg-violet-700 transition-all hover:-translate-y-0.5 active:translate-y-0"
          >
            Мои Проекты
          </a>
        </div>
      </section>
      
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-5xl mt-12">
        <div className="bg-slate-950 p-8 rounded-3xl border border-slate-800 hover:border-slate-700 transition-all text-left">
          <div className="w-12 h-12 bg-violet-950/50 text-violet-400 rounded-xl flex items-center justify-center mb-6">
            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
            </svg>
          </div>
          <h2 className="text-xl font-bold mb-2 text-slate-100">Backend инженерия</h2>
          <p className="text-slate-400 text-sm leading-relaxed">Разработка серверных приложений на FastAPI (Python) и Express (Node.js) с высокой отказоустойчивостью.</p>
        </div>

        <div className="bg-slate-950 p-8 rounded-3xl border border-slate-800 hover:border-slate-700 transition-all text-left">
          <div className="w-12 h-12 bg-violet-950/50 text-violet-400 rounded-xl flex items-center justify-center mb-6">
            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" />
            </svg>
          </div>
          <h2 className="text-xl font-bold mb-2 text-slate-100">Базы данных и кэш</h2>
          <p className="text-slate-400 text-sm leading-relaxed">Проектирование схем и индексов в PostgreSQL и MongoDB. Оптимизация тяжелых запросов.</p>
        </div>

        <div className="bg-slate-950 p-8 rounded-3xl border border-slate-800 hover:border-slate-700 transition-all text-left">
          <div className="w-12 h-12 bg-violet-950/50 text-violet-400 rounded-xl flex items-center justify-center mb-6">
            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
          </div>
          <h2 className="text-xl font-bold mb-2 text-slate-100">DevOps & CI/CD</h2>
          <p className="text-slate-400 text-sm leading-relaxed">Контейнеризация в Docker, построение пайплайнов GitHub Actions и управление инфраструктурой как кодом (IaC).</p>
        </div>
      </section>
    </div>
  )
}
