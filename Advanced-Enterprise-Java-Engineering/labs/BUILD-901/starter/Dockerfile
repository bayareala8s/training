# BUILD-901 starter — intentionally incomplete.
# Finish a multi-stage image that matches datasets/baypay-k8s/CLUSTER.md.
# If you choose to build, the context is reference-apps/baypay (where mvnw lives).

FROM eclipse-temurin:21-jdk
WORKDIR /app
COPY . .
RUN ./mvnw -pl payment-service -am -DskipTests package
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "payment-service/target/payment-service-1.0.0-SNAPSHOT.jar"]
