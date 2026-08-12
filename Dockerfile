FROM alpine:3.20

RUN apk add --no-cache bash curl git git-subtree github-cli openssh-client

WORKDIR /workspace

COPY scripts/module-sync-local.sh /usr/local/bin/module-sync-local
RUN chmod +x /usr/local/bin/module-sync-local

ENTRYPOINT ["module-sync-local"]
