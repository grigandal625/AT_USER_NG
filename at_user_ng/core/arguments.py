import argparse
import os

from dotenv import load_dotenv


load_dotenv()


def get_args() -> dict:
    parser = argparse.ArgumentParser(
        prog="at-user",
        description="User and auth service",
    )

    # RabbitMQ URL (оставляем для совместимости)
    parser.add_argument(
        "-u",
        "--url",
        help="RabbitMQ URL to connect",
        default=os.getenv("RABBITMQ_URL"),
    )

    # Database
    parser.add_argument(
        "--db_host",
        help="Database host",
        default=os.getenv("DB_HOST", "localhost"),
    )
    parser.add_argument(
        "--db_port",
        help="Database port",
        type=int,
        default=int(os.getenv("DB_PORT", 5432)),
    )
    parser.add_argument(
        "--db_name",
        help="Database name",
        default=os.getenv("DB_NAME", "postgres"),
    )
    parser.add_argument(
        "--db_user",
        help="Database user",
        default=os.getenv("DB_USER", "postgres"),
    )
    parser.add_argument(
        "--db_pass",
        help="Database password",
        default=os.getenv("DB_PASS", "postgres"),
    )

    # RabbitMQ
    parser.add_argument(
        "-H",
        "--host",
        "--rabbitmq_host",
        dest="rabbitmq_host",
        help="RabbitMQ host to connect",
        default=os.getenv("RABBITMQ_HOST", "localhost"),
    )
    parser.add_argument(
        "-p",
        "--port",
        "--rabbitmq_port",
        dest="rabbitmq_port",
        help="RabbitMQ port to connect",
        type=int,
        default=int(os.getenv("RABBITMQ_PORT", 5672)),
    )
    parser.add_argument(
        "-L",
        "--login",
        "-U",
        "--user",
        "--user-name",
        "--username",
        "--user_name",
        "--rabbitmq_login",
        dest="rabbitmq_login",
        help="RabbitMQ login to connect",
        default=os.getenv("RABBITMQ_LOGIN", "guest"),
    )
    parser.add_argument(
        "-P",
        "--password",
        "--rabbitmq_password",
        dest="rabbitmq_password",
        help="RabbitMQ password to connect",
        default=os.getenv("RABBITMQ_PASSWORD", "guest"),
    )
    parser.add_argument(
        "-v",
        "--virtualhost",
        "--virtual-host",
        "--virtual_host",
        "--rabbitmq_vhost",
        dest="rabbitmq_vhost",
        help="RabbitMQ virtual host to connect",
        default=os.getenv("RABBITMQ_VHOST", "/"),
    )

    # Server
    parser.add_argument(
        "-sh",
        "--server-host",
        dest="server_host",
        help="Server host",
        default=os.getenv("SERVER_HOST", "localhost"),
    )
    parser.add_argument(
        "-sp",
        "--server-port",
        "--server_port",
        dest="server_port",
        help="Server port",
        type=int,
        default=int(os.getenv("SERVER_PORT", 8000)),
    )

    args = vars(parser.parse_args())

    env_mapping = {
        "db_host": "DB_HOST",
        "db_port": "DB_PORT",
        "db_name": "DB_NAME",
        "db_user": "DB_USER",
        "db_pass": "DB_PASS",
        "rabbitmq_host": "RABBITMQ_HOST",
        "rabbitmq_port": "RABBITMQ_PORT",
        "rabbitmq_login": "RABBITMQ_LOGIN",
        "rabbitmq_password": "RABBITMQ_PASSWORD",
        "rabbitmq_vhost": "RABBITMQ_VHOST",
        "server_host": "SERVER_HOST",
        "server_port": "SERVER_PORT",
        "url": "RABBITMQ_URL",
    }

    for arg_name, env_name in env_mapping.items():
        value = args.get(arg_name)
        if value is not None:
            os.environ[env_name] = str(value)

    return args
    return vars(args)