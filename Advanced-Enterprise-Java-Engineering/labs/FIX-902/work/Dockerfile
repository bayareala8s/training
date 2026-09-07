# FIX-902 repair — CLUSTER.md image contract
# Teaching name: registry.baypay.example/baypay/payment-service:<tag>
# Build context: reference-apps/baypay
# Starter smells removed: ubuntu:latest, apt JDK, USER root,
# ENV BAYPAY_DB_PASSWORD, COPY . . into runtime.
# Credentials at process start only. No -Xmx.

FROM eclipse-temurin:21-jdk AS build
WORKDIR /src
COPY mvnw .
COPY .mvn .mvn
COPY pom.xml .
COPY shared shared
COPY payment-service payment-service
COPY refund-service refund-service
COPY notification-service notification-service
COPY transaction-worker transaction-worker
RUN chmod +x mvnw \
    && ./mvnw -pl payment-service -am -DskipTests package

FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=build /src/payment-service/target/payment-service-1.0.0-SNAPSHOT.jar /app/app.jar
EXPOSE 8080
USER 10001
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
