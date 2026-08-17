FROM golang:1.22-alpine
WORKDIR /app
COPY go.mod ./
COPY chaos ./chaos
COPY src ./src
COPY scripts ./scripts
COPY experiments ./experiments
RUN go mod tidy
EXPOSE 8103
CMD ["go", "run", "./src/main.go", "--serve", "--port", "8103"]
