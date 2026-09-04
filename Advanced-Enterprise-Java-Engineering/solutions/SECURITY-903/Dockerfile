# SECURITY-903 — hardened payment-service image
# Build context: reference-apps/baypay
# Image: registry.baypay.example/baypay/payment-service:<tag>
#
# Production pin (replace with the digest you pulled):
#   FROM eclipse-temurin:21-jre@sha256:<digest-from-registry>
# Lab minimum: tag 21-jre, never :latest.

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
# No apt-get. No extra packages. No password ENV. No :latest.
# Runtime contract (platform YAML, not this file):
#   runAsNonRoot: true
#   runAsUser: 10001
#   readOnlyRootFilesystem: true
#   allowPrivilegeEscalation: false
#   privileged: false
# Mount a writable volume at /tmp when the root filesystem is read-only.
EXPOSE 8080
USER 10001
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
