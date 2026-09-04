# BUILD-901 — payment-service multi-stage image
# Build context: reference-apps/baypay
# Image: registry.baypay.example/baypay/payment-service:<tag>

FROM eclipse-temurin:21-jdk AS build
WORKDIR /src
COPY mvnw pom.xml ./
COPY .mvn/ .mvn/
COPY shared/ shared/
COPY payment-service/ payment-service/
COPY refund-service/ refund-service/
COPY notification-service/ notification-service/
COPY transaction-worker/ transaction-worker/
RUN chmod +x mvnw \
 && ./mvnw -pl payment-service -am -DskipTests package

FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=build /src/payment-service/target/payment-service-1.0.0-SNAPSHOT.jar /app/app.jar
EXPOSE 8080
USER 10001
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
