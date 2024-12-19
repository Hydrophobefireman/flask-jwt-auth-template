FROM python:3.11-bookworm as build
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app
COPY ../ /app/
RUN uv pip install --system -r requirements.txt

FROM build as serve
RUN touch /.dockerenv
CMD [ "gunicorn", "-c", "app/gunicorn.conf.py", "runner:core_app","--access-logfile","-" ]
