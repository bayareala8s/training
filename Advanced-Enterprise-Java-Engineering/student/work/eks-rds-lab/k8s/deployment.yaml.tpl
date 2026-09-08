apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service
  namespace: baypay
  labels:
    app: payment-service
spec:
  replicas: 1
  selector:
    matchLabels:
      app: payment-service
  template:
    metadata:
      labels:
        app: payment-service
    spec:
      containers:
        - name: payment
          image: ${CONTAINER_IMAGE}
          imagePullPolicy: IfNotPresent
          ports:
            - name: http
              containerPort: 8080
          env:
            - name: SPRING_PROFILES_ACTIVE
              value: eks
          envFrom:
            - secretRef:
                name: baypay-db
          readinessProbe:
            httpGet:
              path: /actuator/health/readiness
              port: http
            initialDelaySeconds: 90
            periodSeconds: 10
            timeoutSeconds: 3
            failureThreshold: 12
          livenessProbe:
            httpGet:
              path: /actuator/health/liveness
              port: http
            initialDelaySeconds: 150
            periodSeconds: 15
            timeoutSeconds: 3
            failureThreshold: 8
          resources:
            requests:
              cpu: 256m
              memory: 512Mi
            limits:
              cpu: 256m
              memory: 512Mi
