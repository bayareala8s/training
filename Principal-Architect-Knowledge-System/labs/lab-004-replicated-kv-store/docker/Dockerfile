FROM golang:1.22-alpine
WORKDIR /app
COPY go.mod ./
COPY kvstore ./kvstore
COPY src ./src
COPY scripts ./scripts
RUN go mod tidy
EXPOSE 8095
CMD ["go", "run", "./src/main.go", "--serve", "--port", "8095"]
