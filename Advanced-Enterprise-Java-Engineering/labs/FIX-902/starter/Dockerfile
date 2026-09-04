FROM ubuntu:latest
WORKDIR /app
USER root
RUN apt-get update && apt-get install -y openjdk-21-jdk
ENV BAYPAY_DB_PASSWORD=changeme-baypay
COPY . .
EXPOSE 8080
CMD ["java", "-jar", "payment-service/target/payment-service-1.0.0-SNAPSHOT.jar"]
