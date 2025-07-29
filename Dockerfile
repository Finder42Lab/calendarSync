FROM python:3.13-slim


ENV TZ=Europe/Moscow
ENV PATH="/opt/venv/bin:$PATH"
ENV PATH="/home/python/.local/bin:$PATH"

RUN apt-get update \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/doc/* /usr/share/man/*

WORKDIR /app

COPY ./project/. .

RUN pip install uv
RUN uv sync

CMD ["uv", "run", "plug.py"]