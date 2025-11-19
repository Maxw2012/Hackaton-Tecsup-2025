**Lluvia de ideas:**

| ALMA |  |  |
| :---- | :---- | :---- |
| **Detección de índice de riesgo(0-1)** |  |  |
| **8Chatbot que use datos de índice de riesgo** |  |  |
|  |  |  |

**🌟 Nombre ganador propuesto:**

**“ALMA AI”**

**(Acompañamiento y Lealtad para Mantener el Aprendizaje con Inteligencia Artificial)**

**💫 Concepto y esencia**

**ALMA AI es más que un sistema — es el “alma digital” de la universidad.**  
**Detecta, cuida y acompaña a los estudiantes durante toda su trayectoria académica.**  
**Su misión: “Que ningún estudiante abandone su sueño.”**

**Este nombre golpea emocionalmente, es fácil de pronunciar, tiene identidad local e internacional (puede decirse igual en inglés o español) y transmite empatía \+ tecnología \+ propósito.**

**⚙️ Cómo funciona (visión completa y realista)**

**🧩 1\. Módulo de Análisis Predictivo (Cerebro de ALMA)**

**Recibe datos desde la universidad (notas, asistencias, retrasos en Moodle, uso de la intranet, encuestas breves, participación).**

**Con un modelo de machine learning (XGBoost o Random Forest) calcula un Índice de Riesgo de Deserción (IRD) entre 0 y 1\.**

**IRD \> 0.7 → riesgo alto.**

**IRD 0.4–0.7 → riesgo medio.**

**IRD \< 0.4 → bajo riesgo.**

**El modelo se entrena con datasets históricos o simulados de universidades similares (por ejemplo, TECSUP, USAT o UNI).**

**💬 2\. Módulo Conversacional (Voz y Chat de ALMA)**

**Un chatbot empático 24/7 que conversa con el estudiante en WhatsApp, Telegram o dentro del portal web.**

**Detecta palabras de frustración, ansiedad o desánimo.**

**Usa IA de sentimientos (análisis de texto \+ emojis) para ajustar sus respuestas.**

**Si nota señales de riesgo emocional, activa una alerta automática al tutor o psicólogo institucional.**

**Ejemplo:**

**\> ALMA: “He notado que últimamente mencionas estar agotado. ¿Te gustaría agendar una tutoría o ver técnicas de manejo de estrés?”**  
**Estudiante: “Sí.”**  
**→ Se crea automáticamente una cita con el orientador disponible.**

**❤️ 3\. Módulo de Bienestar y Motivación (Corazón de ALMA)**

**Envía microdesafíos semanales (“Asiste a 3 clases seguidas y gana 10 puntos de motivación”).**

**Ofrece mensajes motivacionales personalizados:**

**\> “Esta semana tu esfuerzo en Cálculo fue excelente. Vas por el camino correcto.”**

**Crea una ruta de bienestar emocional y académico combinada (descanso, objetivos, conexión con mentores).**

**🧭 4\. Módulo de Mentoría Inteligente**

**Conecta automáticamente a estudiantes de primer ciclo con mentores (de últimos ciclos o egresados).**

**Matching basado en IA: intereses, carrera, objetivos.**

**Genera un canal de comunicación directo y medible.**

**📊 5\. Panel Administrativo**

**Para tutores y coordinadores:**

**Mapa de calor de riesgo por facultad.**

**Alertas automáticas de alumnos en zona roja.**

**Reportes visuales (PowerBI embebido o dashboard Laravel/Vue).**

**\---**

**🔐 Cómo se integran los módulos (flujo técnico simplificado)**

**\[Datos del estudiante\]**   
     **↓**  
**\[Módulo Predictivo \- IRD\]**  
     **↓**  
**\[Motor de decisión IA\] → \[Chat empático\] → \[Tutor/Psicólogo\]**  
     **↓**  
**\[Gamificación \+ Mentoría \+ Recomendaciones\]**  
     **↓**  
**\[Dashboard institucional con alertas\]**

**Tecnologías clave:**

**Backend: Laravel \+ Python (FastAPI para IA)**

**Frontend: Vue 3 \+ TailwindCSS**

**Chatbot: Rasa / GPT API / Llama3 (open source)**

**Base de datos: PostgreSQL (análisis estructurado)**

**Infra: Docker \+ Railway / Hugging Face Spaces**

**Análisis emocional: HuggingFace Transformers (modelo Sentiment Analysis)**

**\---**

**🚀 Por qué ganará**

**Criterio del jurado	Cómo ALMA AI lo domina**

**Innovación	Combina IA predictiva, emocional y mentoría gamificada.**  
**Impacto	Acompaña emocional y académicamente a miles de estudiantes.**  
**Factibilidad	Basado en tecnologías libres, escalable en servidores ligeros.**  
**Usabilidad	Interfaz natural (WhatsApp y web), no requiere capacitación.**  
**Escalabilidad	Adaptable a cualquier universidad, solo cambia dataset.**

**\---**

**🎯 Ejemplo de caso real (para el pitch)**

**\> “Luis, estudiante de ingeniería, bajó su rendimiento y dejó de asistir.**  
**ALMA detectó un 0.82 de riesgo y lo contactó.**  
**Tras conversar, identificó ansiedad y lo conectó con un tutor.**  
**Hoy, Luis volvió a clases. Una IA salvó un sueño.”**

**\---**

**🔥 Frase final del pitch**

**\> “No creamos solo un asistente.**  
**Creamos ALMA, la inteligencia artificial que escucha, comprende y acompaña a cada estudiante para que nunca abandone sus sueños.”**

**.**

---

## **🧭 PLAN DEFINITIVO — “ALMA AI” (Versión Ganadora Hackathon TECSUP 2025\)**

**Framework: Django 5**  
 **IA: Google Gemini (vía API Python SDK)**  
 **Dataset: Donado por universidad local (anónimo, real)**  
 **Infraestructura: Django local \+ PostgreSQL \+ despliegue en Render**  
 **Duración total: 4 semanas (1 mes exacto)**

---

## **👥 ROLES AJUSTADOS Y RESPONSABILIDADES GLOBALES**

| Integrante | Rol Principal | Responsabilidad Global |
| ----- | ----- | ----- |
| **Frank** | **Líder general / Arquitectura / Coordinación IA** | **Dirige el proyecto, define arquitectura, narrativa, flujo, validación final** |
| **Brayan** | **Data Engineer / Limpieza y validación de datos** | **Prepara dataset, transforma variables, asiste a Bulnes en features** |
| **Bulnes** | **Chief AI Engineer / Pitch técnico** | **Desarrolla y entrena el modelo predictivo, integra Gemini, lidera demo técnica** |
| **Geancarlos** | **Fullstack Django (UI \+ Views \+ Templates)** | **Construye vistas y lógicas de interacción del usuario (chat, dashboard, alertas)** |
| **Bartolo** | **UI Designer \+ Testing \+ Pitch visual** | **Diseña interfaz, asegura experiencia fluida, arma la presentación final visual** |

---

## **📆 CRONOGRAMA DETALLADO (4 SEMANAS EXACTAS)**

---

### **🗓️ SEMANA 1 — ESTRUCTURA \+ DATOS \+ BASE VISUAL**

**Objetivo: dejar el entorno, datos y diseño inicial listos.**

#### **🔹 Frank**

* **Diseñar arquitectura Django (`core`, `students`, `ai`, `dashboard`, `chat`).**  
* **Configurar PostgreSQL, `.env`, y settings base.**  
* **Definir modelo de usuario extendido (`UserProfile` con rol: estudiante, tutor, admin).**  
* **Documentar flujo principal (casos de uso: riesgo → chat → tutoría).**  
* **Coordinar avances diarios (20 min standup).**

#### **🔹 Brayan**

* **Analizar dataset donado: limpieza, normalización y etiquetado.**  
* **Seleccionar variables predictoras (notas, asistencia, edad, estado emocional).**  
* **Exportar CSV limpio (`students_data_clean.csv`).**  
* **Generar primeros gráficos estadísticos (histograma de riesgo, correlación Pearson).**

#### **🔹 Bulnes**

* **Crear entorno IA (`ai/models.py`, `ai/utils.py`).**  
* **Leer dataset limpio y hacer *feature engineering*.**  
* **Entrenar modelo predictivo inicial con XGBoost o RandomForest.**  
* **Guardar modelo (`risk_model.pkl`) y registrar precisión base.**  
* **Esquematizar lógica IRD (Índice de Riesgo de Deserción).**

#### **🔹 Geancarlos**

* **Iniciar proyecto Django y maquetar templates base (login, dashboard, chat).**  
* **Navbar, colores institucionales y plantillas responsive con Bootstrap 5\.**  
* **Configurar sistema de roles: estudiante / tutor / admin.**

#### **🔹 Bartolo**

* **Diseñar logo oficial “ALMA AI” 💜 y paleta de color (violeta suave \+ amarillo energía).**  
* **Crear prototipo visual rápido en Figma (referencia para front).**  
* **Documentar estilo UI (botones, tarjetas, chat).**

**Entrega Semana 1:**  
 **✅ Proyecto Django estructurado \+ BD funcional.**  
 **✅ Dataset limpio.**  
 **✅ Modelo IA entrenado (versión 1).**  
 **✅ Mock visual base.**

---

### **🗓️ SEMANA 2 — IA PREDICTIVA \+ INTEGRACIÓN GEMINI**

**Objetivo: conectar modelo local y IA empática.**

#### **🔹 Bulnes**

* **Integrar modelo predictivo en Django (`predict_student_risk()` en `ai/utils.py`).**  
* **Crear endpoint `/predict/<student_id>` que devuelva IRD y nivel (“bajo”, “medio”, “alto”).**  
* **Implementar conexión con Gemini API (módulo `alma_ai_agent.py`).**  
* **Definir prompt principal de ALMA (“actúa como mentora empática que detecta emociones y motiva al estudiante”).**  
* **Pruebas unitarias del flujo completo: predicción → mensaje IA.**

#### **🔹 Brayan**

* **Asistir a Bulnes en normalización de datos de entrada (min-max scaling, one-hot).**  
* **Crear función que genere dataset incremental (para simular nuevos semestres).**  
* **Apoyar en análisis de correlación entre IRD y sentimiento.**

#### **🔹 Frank**

* **Supervisar arquitectura IA y definir umbrales de alerta.**  
* **Validar calidad de respuestas de Gemini con ejemplos reales (prompts iterativos).**  
* **Integrar middleware que guarde logs de predicción.**

#### **🔹 Geancarlos**

* **Conectar chat front → view Django → función Gemini.**  
* **Mostrar respuestas IA en tiempo real (spinner de escritura).**  
* **Mostrar colores emocionales (verde motivado, naranja estresado, rojo desanimado).**

#### **🔹 Bartolo**

* **Ajustar CSS del chat y dashboard.**  
* **Diseñar animaciones suaves para IA “pensando”.**  
* **Documentar UX y preparar material gráfico para pitch.**

**Entrega Semana 2:**  
 **✅ Modelo predictivo \+ Gemini integrados y funcionales.**  
 **✅ Chat empático operativo.**  
 **✅ Base de alertas lista.**

---

### **🗓️ SEMANA 3 — DASHBOARDS \+ ALERTAS \+ SIMULACIONES**

**Objetivo: cerrar el ecosistema funcional de los 3 roles.**

#### **🔹 Bulnes**

* **Integrar módulo de predicción masiva (batch) → dashboard admin.**  
* **Conectar IA con motor de alertas:**  
  * **IRD \> 0.75 \= alerta roja.**  
  * **IRD 0.5–0.75 \= seguimiento.**  
* **Agregar método de simulación (“predecir todos los estudiantes del dataset”).**  
* **Preparar script demo técnica (usará en el pitch).**

#### **🔹 Brayan**

* **Graficar evolución IRD (Chart.js / Plotly).**  
* **Implementar dashboard estadístico:**  
  * **Total estudiantes monitoreados.**  
  * **% riesgo alto / medio / bajo.**  
  * **Tendencia mensual.**

#### **🔹 Frank**

* **Integrar módulo de notificaciones a tutores.**  
* **Validar flujo completo (student → predicción → mensaje → alerta → tutor).**  
* **Crear casos de prueba reales (“Luis”, “Camila”).**

#### **🔹 Geancarlos**

* **Terminar vistas completas:**  
  * **Dashboard tutor (alertas activas, historial).**  
  * **Panel admin (gráficos globales).**  
  * **Chat IA 100% funcional.**  
* **Conectar templates con datos reales del backend.**

#### **🔹 Bartolo**

* **Revisar diseño global y coherencia visual.**  
* **Agregar efectos suaves y favicon animado.**  
* **Test de accesibilidad (mobile / desktop).**  
* **Empezar a construir presentación visual (Gamma o Tome).**

**Entrega Semana 3:**  
 **✅ Sistema funcional con todos los roles activos.**  
 **✅ Alertas reales.**  
 **✅ Dashboard \+ Chat IA.**  
 **✅ Demo lista para presentación.**

---

### **🗓️ SEMANA 4 — PRUEBAS FINALES \+ PITCH**

**Objetivo: afinar el sistema, crear historia y presentarla como ganadores.**

#### **🔹 Bulnes (Protagonista técnico del pitch)**

* **Preparar demo guiada del modelo en acción:**  
  * **Mostrar predicción real.**  
  * **Explicar cómo Gemini adapta el mensaje según el IRD.**  
  * **Hacer en vivo “detección de riesgo \+ respuesta empática”.**  
* **Afinar tiempos de respuesta IA.**  
* **Revisar logs y métricas del modelo.**  
* **Practicar exposición técnica (2 minutos).**

#### **🔹 Frank**

* **Redactar narrativa del pitch (estructura: Problema → Solución → Tecnología → Impacto → Demo).**  
* **Coordinar ensayos del equipo.**  
* **Introducir con historia emocional (“Luis casi abandona… ALMA lo acompañó”).**  
* **Control general de tiempos y presentación.**

#### **🔹 Brayan**

* **Mostrar métricas de impacto en el pitch:**  
  * **Precisión del modelo.**  
  * **Reducción estimada de deserción.**  
  * **Comparación antes/después.**  
* **Asistir a Bulnes en la demo en vivo.**

#### **🔹 Geancarlos**

* **Asegurar que todo el flujo esté libre de errores.**  
* **Preparar pantallas para demo en secuencia (login → chat → dashboard → alerta).**  
* **Soporte técnico durante la exposición.**

#### **🔹 Bartolo**

* **Diseñar presentación Gamma / Tome con storytelling visual:**  
   **1️⃣ Problema educativo**  
   **2️⃣ Nacimiento de ALMA AI**  
   **3️⃣ Flujo IA predictiva**  
   **4️⃣ Interfaz empática**  
   **5️⃣ Impacto y escalabilidad**  
* **Editar video demo (30–60 s) con voz IA femenina de fondo.**  
* **Supervisar visuales durante el pitch.**

**Entrega Semana 4:**  
 **✅ ALMA AI 100% funcional y demostrable.**  
 **✅ Pitch de alto impacto (emocional \+ técnico).**  
 **✅ Video \+ presentación visual.**  
 **✅ Documentación y métricas.**

---

## **🏁 HITOS PRINCIPALES**

| Semana | Hito | Responsable principal |
| ----- | ----- | ----- |
| **1** | **Base Django \+ dataset limpio \+ modelo inicial** | **Brayan \+ Bulnes** |
| **2** | **Modelo \+ Gemini integrados** | **Bulnes** |
| **3** | **Plataforma con alertas y dashboards** | **Geancarlos \+ Bulnes** |
| **4** | **Pitch final y demo técnica** | **Frank \+ Bulnes** |

---

## **🎯 CONCLUSIÓN**

**💡 Con esta estructura:**

* **Bulnes se convierte en el eje técnico y rostro IA (explica cómo predice y conversa).**  
* **Frank lidera el enfoque narrativo, propósito y arquitectura.**  
* **Brayan da rigor analítico y valida impacto.**  
* **Geancarlos hace visible todo (UI Django).**  
* **Bartolo convierte el proyecto en una experiencia visual memorable.**

**Así aseguras equilibrio perfecto entre tecnología, empatía e impacto social, justo lo que los jurados buscan.**

---

**¿Quieres que te prepare ahora la versión editable para Freedcamp / Trello (con fechas exactas y checklists por integrante)?**  
 **Puedo entregártela en formato JSON o tabla markdown para importarla directo.**

