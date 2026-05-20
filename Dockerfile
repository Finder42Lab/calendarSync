FROM python:3.13-slim


ENV TZ=Europe/Moscow
ENV PATH="/root/.local/bin/:$PATH"
ENV UV_PROJECT_ENVIRONMENT=/.venv

RUN apt-get update
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/doc/* /usr/share/man/*

WORKDIR /app

COPY ./project/. .

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
RUN uv sync

CMD ["uv", "run", "plug.py"]