# BUILD-901 — payment-service image (AEJE-D-039)
# Teaching name: registry.baypay.example/baypay/payment-service:<tag>
# Build context: reference-apps/baypay (Maven Wrapper lives there).
# Secrets: BAYPAY_DB_URL, BAYPAY_DB_USER, BAYPAY_DB_PASSWORD at runtime only.
# Do not ENV a password. Do not set -Xmx (heap ≠ cgroup; INC-JVM-806).

# --- build: JDK + ./mvnw ---
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

# --- runtime: JRE only, non-root ---
FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=build /src/payment-service/target/payment-service-1.0.0-SNAPSHOT.jar /app/app.jar
EXPOSE 8080
USER 10001
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
