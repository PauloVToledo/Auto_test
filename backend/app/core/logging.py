import sys
import structlog
import logging


def configure_logging():
    """
    Configura structlog para emitir logs en formato JSON estandarizado.
    """

    # 1. Configurar procesadores compartidos (timestamp, nivel, etc.)
    shared_processors = [
        structlog.contextvars.merge_contextvars,  # Permite agregar variables globales (ej: request_id)
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,  # Formatea trazas de error completas
        structlog.processors.UnicodeDecoder(),
    ]

    # 2. Configurar Structlog
    structlog.configure(
        processors=shared_processors
        + [structlog.processors.JSONRenderer()],  # <--- LA CLAVE: Salida JSON pura
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # 3. Interceptar los logs nativos de Python (uvicorn, fastapi) y forzarlos a JSON
    # Esto hace que incluso los logs de inicio de servidor salgan en JSON.
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )

    # Redirigir logs estándar a structlog
    def json_renderer(logger, name, event_dict):
        # Renderiza el diccionario a JSON
        return structlog.processors.JSONRenderer()(logger, name, event_dict)

    # Opcional: Silenciar logs ruidosos de uvicorn access si quieres controlar tu propio log de request
    # logging.getLogger("uvicorn.access").disabled = True
