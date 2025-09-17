FROM python:3.13.2-slim AS app
WORKDIR /app

ARG UID=1000
ARG GID=1000
ARG DEBUG="false"

#RUN apt-get update \
#    && apt-get install -y --no-install-recommends \
#        build-essential \
#        curl \
#        libpq-dev \
#    && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
#    && apt-get clean

RUN groupadd -g "${GID}" python \
    && useradd --create-home --no-log-init -u "${UID}" -g "${GID}" python

RUN chown python:python /app

USER python

ENV PIP_CACHE_DIR=/app/.cache/pip
COPY --chown=python:python requirements*.txt ./
RUN pip install --user --no-cache-dir --upgrade pip \
    && pip install --user --no-cache-dir --upgrade setuptools wheel \
    && pip install --user --no-cache-dir -r requirements.txt

ENV DEBUG="${DEBUG}" \
    PYTHONUNBUFFERED="true" \
    PYTHONPATH="." \
    PATH="${PATH}:/home/python/.local/bin" \
    USER="python"

COPY --chown=python:python . .
WORKDIR /app/src

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]