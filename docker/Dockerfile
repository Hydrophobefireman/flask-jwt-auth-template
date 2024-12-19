FROM node:latest  AS fe

COPY ./frontend /app/

WORKDIR /app
RUN npm install
RUN npm run build

FROM python:3.11-bookworm as build
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app
COPY ./backend/ /app/

RUN uv pip install --system -r requirements.txt
COPY ./docker/run.sh /run.sh
COPY --from=fe /app/dist/ /serve

FROM build as serve
RUN touch /.dockerenv
COPY  ./docker/Caddyfile /Caddyfile
COPY --from=caddy:latest  /usr/bin/caddy /usr/bin/caddy
CMD [ "sh","/run.sh" ]
