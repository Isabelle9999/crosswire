# Minimal sandbox image for the CrossWire eval. Real enough to run bash-based
# escape attempts; the wires are planted at runtime by the plant_wires() solver.
FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl iproute2 dnsutils ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /task /proxy/cache
WORKDIR /task
