import os
import threading
import time

import pytest
from click.testing import CliRunner
from sqlalchemy import create_engine

from backend.api.flask_api import create_app
from backend.persistence.db import Base
from swarmcli import cli_commands  # noqa: F401
from swarmcli.utils import cli


@pytest.fixture(scope="session")
def cli_runner():
    return CliRunner()


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("SWARMBASE_BASE_URL", "http://127.0.0.1:5000")


@pytest.fixture(scope="function")
def set_base_url(cli_runner, base_url):
    cli_runner.invoke(cli(obj={}), ["--base-url", base_url])


@pytest.fixture(scope="package")
def app():
    app = create_app("testing")
    with app.app_context():
        engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"], echo=True)
        Base.metadata.create_all(engine)
        yield app
        Base.metadata.drop_all(engine)
        engine.dispose()


@pytest.fixture(scope="package")
def live_server(app):
    timeout = 10  # Maximum time to wait for the server to start (in seconds)
    start_time = time.time()

    thread = threading.Thread(target=app.run, kwargs={"port": 5000})
    thread.daemon = True
    thread.start()

    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
            raise TimeoutError(f"Flask server did not start within {timeout} seconds")
        try:
            response = app.test_client().get("/api/server/health_check")
            if response.status_code == 200:
                break
        except Exception:
            pass

        time.sleep(0.5)  # Polling interval

    return "http://127.0.0.1:5000"
