# PERFORMANCE-904 — layer-cached payment-service image
# Build context: reference-apps/baypay
# Runtime is a JRE. Heap is a percentage of the cgroup, not -Xmx equal to the limit.

FROM eclipse-temurin:21-jdk AS build
WORKDIR /src
COPY mvnw pom.xml ./
COPY .mvn/ .mvn/
COPY shared/pom.xml shared/pom.xml
COPY payment-service/pom.xml payment-service/pom.xml
COPY refund-service/pom.xml refund-service/pom.xml
COPY notification-service/pom.xml notification-service/pom.xml
COPY transaction-worker/pom.xml transaction-worker/pom.xml
RUN chmod +x mvnw \
 && ./mvnw -pl payment-service -am dependency:go-offline -B
COPY shared/ shared/
COPY payment-service/ payment-service/
COPY refund-service/ refund-service/
COPY notification-service/ notification-service/
COPY transaction-worker/ transaction-worker/
RUN ./mvnw -pl payment-service -am -DskipTests package

FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=build /src/payment-service/target/payment-service-1.0.0-SNAPSHOT.jar /app/app.jar
EXPOSE 8080
USER 10001
ENV JAVA_TOOL_OPTIONS="-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0"
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
