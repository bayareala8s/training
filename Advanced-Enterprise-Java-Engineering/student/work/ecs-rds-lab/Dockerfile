# Runtime-only. start.sh packages the fat JAR on the host first.
# Same heap contract as labs/PERFORMANCE-904: cgroup percentage, not -Xmx = 512.
FROM eclipse-temurin:21-jre
WORKDIR /app
COPY payment-service/target/payment-service-1.0.0-SNAPSHOT.jar /app/app.jar
ENV JAVA_TOOL_OPTIONS="-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0"
EXPOSE 8080
USER 10001
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
