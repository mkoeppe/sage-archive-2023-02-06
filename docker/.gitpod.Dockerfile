FROM ghcr.io/mkoeppe/sage/sage-docker-gitpod-standard-with-system-packages:dev
COPY --chown=gitpod:gitpod --from=ghcr.io/mkoeppe/sage/sage-docker-gitpod-standard-with-targets:dev /home/gitpod/sage/logs  /home/gitpod/sage/logs
COPY --chown=gitpod:gitpod --from=ghcr.io/mkoeppe/sage/sage-docker-gitpod-standard-with-targets:dev /home/gitpod/sage-local /home/gitpod/sage-local
