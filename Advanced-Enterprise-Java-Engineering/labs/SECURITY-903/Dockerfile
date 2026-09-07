# SECURITY-903 — hardened payment-service (AEJE-D-040)
# registry.baypay.example/baypay/payment-service:<tag>
# Build context: reference-apps/baypay
#
# Trust boundary (image):
#   pinned JRE (tag 21-jre; production uses digest), JAR only, USER 10001,
#   no extra packages, no secret ENV/ARG values, no :latest.
# Platform must continue the story:
#   readOnlyRootFilesystem: true + writable volume at /tmp (JVM / Spring temp).
#   Never --privileged / privileged: true. Privileged is not how you get /tmp.
# Secrets: BAYPAY_DB_* at process start (Module 10 Secret baypay-db).
# Do not set -Xmx. Heap ≠ cgroup (INC-JVM-806).

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

# Lab minimum: tag 21-jre (not :latest).
# Production: pin a digest and rebuild when Temurin publishes a CVE fix
# (Jordan owns the bump). Example amd64 manifest, 2026-09-06 inspect:
#   FROM eclipse-temurin:21-jre@sha256:d1d7f43094ea37e9ae77ea3ca40026bc1de1bf1dc2cad37b08d66b9a016a2ea6
FROM eclipse-temurin:21-jre
WORKDIR /app
# No apt-get / curl / vim / sudo. The JRE image is the toolbox.
COPY --from=build /src/payment-service/target/payment-service-1.0.0-SNAPSHOT.jar /app/app.jar
EXPOSE 8080
USER 10001
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
