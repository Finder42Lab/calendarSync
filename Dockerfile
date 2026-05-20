FROM python:3.13-slim


ENV TZ=Europe/Moscow
ENV PATH="/opt/venv/bin:$PATH"
ENV PATH="/home/python/.local/bin:$PATH"
ENV UV_PROJECT_ENVIRONMENT=/.venv

RUN apt-get update
RUN apt-get install -qq --no-install-recommends curl
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/doc/* /usr/share/man/*

WORKDIR /app

COPY ./project/. .

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
RUN uv sync

CMD ["uv", "run", "plug.py"]