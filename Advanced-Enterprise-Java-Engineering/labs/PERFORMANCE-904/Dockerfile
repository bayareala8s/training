# PERFORMANCE-904 — layer cache + cgroup heap (not -Xmx = limit)
# registry.baypay.example/baypay/payment-service:<tag>
# Build context: reference-apps/baypay
#
# Cache: Wrapper + every module pom.xml, then dependency:go-offline,
# then sources, then package. A controller edit must not re-download plugins.
# Runtime: 21-jre, USER 10001, no secrets, no -Xmx.
# Heap: JAVA_TOOL_OPTIONS percentage of the cgroup (LAB-704 / INC-JVM-806).

FROM eclipse-temurin:21-jdk AS build
WORKDIR /src
COPY mvnw .
COPY .mvn .mvn
COPY pom.xml .
COPY shared/pom.xml shared/pom.xml
COPY payment-service/pom.xml payment-service/pom.xml
COPY refund-service/pom.xml refund-service/pom.xml
COPY notification-service/pom.xml notification-service/pom.xml
COPY transaction-worker/pom.xml transaction-worker/pom.xml
RUN chmod +x mvnw \
    && ./mvnw -pl payment-service -am dependency:go-offline -B

COPY shared shared
COPY payment-service payment-service
COPY refund-service refund-service
COPY notification-service notification-service
COPY transaction-worker transaction-worker
RUN ./mvnw -pl payment-service -am -DskipTests package

FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=build /src/payment-service/target/payment-service-1.0.0-SNAPSHOT.jar /app/app.jar
ENV JAVA_TOOL_OPTIONS="-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0"
EXPOSE 8080
USER 10001
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
