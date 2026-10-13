# 🔔 Notificador Universal de Citas

Herramienta de automatización en Python de alta fiabilidad, diseñada para pequeños negocios que quieren eliminar las ausencias a citas. El sistema envía recordatorios por correo electrónico personalizados directamente desde tu cuenta de Gmail a tus clientes, garantizando una comunicación profesional y coherente.

## 🚀 Características principales

* **Inteligencia de fechas global**: motor de análisis robusto que reconoce automáticamente los formatos internacional (ISO: AAAA/MM/DD) y europeo (DD/MM/AAAA).
* **Importación inteligente de CSV**: detector automático de delimitadores (admite `,` y `;`) y un "filtro de ruido" que omite filas vacías o columnas fantasma generadas habitualmente por Excel o Google Sheets.
* **Seguridad ante todo**: gestión de credenciales mediante variables de entorno (`.env`) y cifrado seguro a través de SMTP_SSL.
* **Envío con comportamiento humano**: "pausa inteligente" integrada entre correos para proteger la reputación de tu cuenta de Gmail y garantizar una alta tasa de entrega.
* **Registro profesional**: genera un archivo `activity.log` detallado para monitorizar en tiempo real y resolver incidencias.

## 🛠️ Instalación y configuración

1. **Clonar el repositorio**:
```bash
   git clone https://github.com/Edu-jg8/universal-appointment-notifier.git
   cd universal-appointment-notifier
```

2. **Configuración del entorno**:
   Crea un archivo `.env` en el directorio raíz con tus credenciales:
```env
   EMAIL_USER=tu-correo@gmail.com
   EMAIL_PASS=tu-contraseña-de-aplicacion-de-16-caracteres
```

3. **Instalar dependencias**:
```bash
   pip install -r requirements.txt
```

## 📋 Guía de uso

1. **Prepara tus datos**: usa Google Sheets o Excel para gestionar tu agenda. Asegúrate de tener estas cabeceras: `DATE`, `TIME`, `CLIENT_NAME`, `EMAIL`, `SERVICE`, `LOCATION`.
2. **Exporta y guarda**: guarda el archivo como `appointments.csv` dentro de la carpeta `data/`.
3. **Ejecuta la aplicación**: desde la terminal o con el archivo `run_app.bat` incluido:
```bash
   python main.py
```
4. **Supervisa**: revisa `logs/activity.log` para comprobar que todos los recordatorios se enviaron correctamente.

---

## 🔒 Nota de seguridad de Gmail

Esta aplicación requiere tener activada la **verificación en dos pasos** en tu cuenta de Google. Debes generar una **contraseña de aplicación** específica (de 16 caracteres) para que el script envíe correos de forma segura sin exponer tu contraseña principal.
