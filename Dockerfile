FROM alpine:3.14

WORKDIR /mve
COPY ["mve", "."]

RUN ["apk", "update"]
RUN ["apk", "add" ,"ffmpeg"]
