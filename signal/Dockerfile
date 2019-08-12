ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

RUN apk add --no-cache jq openjdk8-jre

ADD https://github.com/AsamK/signal-cli/releases/download/v0.6.2/signal-cli-0.6.2.tar.gz /signal-cli.tar.gz

RUN tar xvzf signal-cli.tar.gz

COPY run.sh /

CMD [ "/run.sh" ]
