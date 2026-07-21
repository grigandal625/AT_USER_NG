import asyncio
import logging
import os

from at_queue.core.session import ConnectionParameters
from django.core import management
from uvicorn import Config
from uvicorn import Server

from at_user_ng.absolute.django_init import django_application
from at_user_ng.absolute.django_init import get_args
from at_user_ng.core.component import AuthWorker
import logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def get_at_user():
    args = get_args()
    logger.info('ARGS IN MAIN', args)
    print('ARGS IN MAIN', args)
    server_host = args.pop("server_host", "localhost")
    server_port = args.pop("server_port", 8000)
    connection_parameters = ConnectionParameters(**args)

    print('AMPQ ARGS', connection_parameters.connecion_kwargs)

    # Создание PID-файла (опционально)
    try:
        if not os.path.exists("/var/run/at_user_ng/"):
            os.makedirs("/var/run/at_user_ng/")

        with open("/var/run/at_user_ng/pidfile.pid", "w") as f:
            f.write(str(os.getpid()))
    except PermissionError:
        pass

    # Инициализация 
    at_user = AuthWorker(connection_parameters=connection_parameters)

    args['server_host'] = server_host
    args['server_port'] = server_port

    return at_user, args


async def main_with_django():
    """Основная функция для запуска Django."""
    at_user, args = get_at_user()
    server_host = args.pop("server_host", "localhost")
    server_port = args.pop("server_port", 8000)

    async def lifespan(app):
        """Пользовательский lifespan для управления жизненным циклом"""

        await at_user.initialize()
        await at_user.register()

        loop = asyncio.get_event_loop()
        # Запуск навыков в фоновом режиме
        loop.create_task(at_user.start())

        yield  # Приложение запущено

    # Обертываем Django-приложение с пользовательским lifespan
    async def app(scope, receive, send):
        if scope["type"] == "lifespan":
            # Обработка событий lifespan
            while True:
                message = await receive()
                if message["type"] == "lifespan.startup":
                    # Запуск lifespan
                    async for _ in lifespan(None):
                        pass
                    await send({"type": "lifespan.startup.complete"})
                elif message["type"] == "lifespan.shutdown":
                    # Завершение lifespan
                    await send({"type": "lifespan.shutdown.complete"})
                    break
        else:
            # Обработка HTTP-запросов через Django
            scope["at_user"] = at_user
            scope["components"] = {
                "at_user": at_user
            }
            await django_application(scope, receive, send)

    # Конфигурация и запуск сервера Uvicorn
    config = Config(
        app=app,  # Передаем обернутое ASGI-приложение
        host=server_host,
        port=server_port,
        lifespan="on",  # Включаем поддержку lifespan
    )
    server = Server(config=config)
    await server.serve()


if __name__ == "__main__":
    from django.contrib.auth import get_user_model

    User = get_user_model()

    management.call_command("migrate")
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser("admin", "admin@example.com", "1=qpALzm")
    asyncio.run(main_with_django())
