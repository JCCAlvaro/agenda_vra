
Toda la lógica sensible (roles, prioridades, recordatorios, auditoría) vive en el backend. El cliente es una cáscara delgada que consume la API y puede actualizarse por separado.

---

## 🧰 Stack tecnológico

### Backend
| Componente | Versión |
|---|---|
| Python | 3.11+ |
| FastAPI | 0.115 |
| SQLAlchemy | 2.0 |
| PyMySQL | 1.1 |
| APScheduler | 3.10 |
| PyJWT | 2.9 |
| bcrypt | 4.2 |
| MySQL | 8.0 |

### Frontend
| Componente | Versión |
|---|---|
| Tauri | 2.x |
| React | 18.3 |
| TypeScript | 5.5 |
| Vite | 5.4 |
| FullCalendar | 6.1 |

---

## ✅ Requisitos previos

Antes de ejecutar el proyecto, instala:

- **Docker** y **Docker Compose** (para MySQL).
- **Python 3.11+** con `pip` y `venv`.
- **Node.js 20+** con `npm`.
- **Rust** (mediante [rustup](https://rustup.rs/)) y las dependencias de Tauri según tu SO:
  - **macOS:** `xcode-select --install`
  - **Windows:** Visual Studio Build Tools (workload *Desktop development with C++*) + WebView2.
  - **Linux (Ubuntu/Debian):**
    ```bash
    sudo apt install libwebkit2gtk-4.1-dev build-essential curl wget file \
      libxdo-dev libssl-dev libayatana-appindicator3-dev librsvg2-dev