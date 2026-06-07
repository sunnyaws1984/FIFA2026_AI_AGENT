apiVersion: apps/v1
kind: Deployment
metadata:
  name: fifa2026-agent
spec:
  replicas: 1
  selector:
    matchLabels:
      app: fifa2026-agent
  template:
    metadata:
      labels:
        app: fifa2026-agent
    spec:
      containers:
        - name: fifa2026-agent
          image: fifa2026-agent:latest
          imagePullPolicy: Never        # use local Docker image
          ports:
            - containerPort: 7860
          env:
            - name: MONGO_HOST
              value: "mongodb-service"  # ✅ K8s service name — no port-forward needed
            - name: MONGO_PORT
              value: "27017"
            - name: MONGO_USER
              value: "admin"
            - name: MONGO_PASS
              value: "admin123"
          envFrom:
            - secretRef:
                name: agent-secret      # injects GOOGLE_API_KEY
---
apiVersion: v1
kind: Service
metadata:
  name: fifa2026-agent-service
spec:
  type: NodePort
  selector:
    app: fifa2026-agent
  ports:
    - port: 7860
      targetPort: 7860
      nodePort: 32760