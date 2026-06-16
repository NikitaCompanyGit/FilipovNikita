export default function AboutPage() {
  return (
    <div className="max-w-4xl mx-auto py-4">
      <h1 className="text-4xl font-extrabold mb-8 text-slate-100 tracking-tight">Обо мне</h1>
      
      <div className="grid md:grid-cols-2 gap-8">
        <div className="bg-slate-950 p-8 rounded-3xl border border-slate-800">
          <h2 className="text-2xl font-bold mb-6 flex items-center gap-2 text-slate-100">
            <svg className="w-6 h-6 text-violet-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
            </svg>
            Мой Стек
          </h2>
          <ul className="space-y-3">
            {[
              'Бэкенд: Python (FastAPI, Flask, Django), Node.js (Express)',
              'Базы данных: PostgreSQL (SQL, оптимизация индексов), MongoDB (NoSQL)',
              'Инструменты: Docker, Docker Compose, Git, GitHub Actions',
              'Стрим-системы: Apache Kafka (Producer, Consumer, Windowing)',
              'Анализ и ИИ: SAST/SCA безопасность, интеграция Sber GigaChat API',
              'Разработка фронтенда: React, Next.js, Tailwind CSS (базовый уровень)'
            ].map((skill, index) => (
              <li key={index} className="flex items-start gap-3">
                <div className="w-2 h-2 rounded-full bg-violet-400 mt-2.5 shrink-0"></div>
                <span className="text-slate-300 font-medium text-sm leading-relaxed">{skill}</span>
              </li>
            ))}
          </ul>
        </div>
        
        <div className="bg-slate-950 p-8 rounded-3xl border border-slate-800">
          <h2 className="text-2xl font-bold mb-6 flex items-center gap-2 text-slate-100">
            <svg className="w-6 h-6 text-violet-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
            Деятельность
          </h2>
          <div className="space-y-6">
            <div className="border-l-4 border-violet-500/30 pl-4 py-1">
              <h3 className="text-lg font-bold text-slate-100">Инженер Бэкенд-решений</h3>
              <p className="text-sm text-violet-400 font-semibold mb-2">Разработка инфраструктуры • 2025 - Наст. время</p>
              <p className="text-slate-400 text-sm leading-relaxed">Специализируюсь на проектировании REST API, интеграции со стриминговыми системами сообщений и обеспечении сетевой безопасности.</p>
            </div>
            <div className="border-l-4 border-violet-500/30 pl-4 py-1">
              <h3 className="text-lg font-bold text-slate-100">Младший разработчик</h3>
              <p className="text-sm text-violet-400 font-semibold mb-2">Фриланс / Web-сервисы • 2024 - 2025</p>
              <p className="text-slate-400 text-sm leading-relaxed">Создание серверной логики веб-приложений, администрирование реляционных баз данных и написание парсеров.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
