#!/bin/bash
# ─────────────────────────────────────────────────────
#  FIFA 2026 — Single-node MongoDB on Kubernetes
# ─────────────────────────────────────────────────────

set -e

NAMESPACE="fifa2026"
MONGO_USER="admin"
MONGO_PASS="admin123"

echo "🚀 Deploying MongoDB to namespace: $NAMESPACE"

# ── 1. Namespace ───────────────────────────────────────
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# ── 2. Secret ──────────────────────────────────────────
kubectl apply -n $NAMESPACE -f - <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: mongodb-secret
type: Opaque
stringData:
  MONGO_INITDB_ROOT_USERNAME: "$MONGO_USER"
  MONGO_INITDB_ROOT_PASSWORD: "$MONGO_PASS"
EOF

# ── 3. PersistentVolume ────────────────────────────────
kubectl apply -f - <<EOF
apiVersion: v1
kind: PersistentVolume
metadata:
  name: mongodb-pv
  labels:
    app: mongodb
spec:
  capacity:
    storage: 2Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  hostPath:
    path: /mnt/fifa2026-mongodb
    type: DirectoryOrCreate
EOF

# ── 4. PersistentVolumeClaim ───────────────────────────
kubectl apply -n $NAMESPACE -f - <<EOF
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mongodb-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 2Gi
  selector:
    matchLabels:
      app: mongodb
EOF

# ── 5. Deployment ──────────────────────────────────────
kubectl apply -n $NAMESPACE -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mongodb
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mongodb
  template:
    metadata:
      labels:
        app: mongodb
    spec:
      containers:
        - name: mongodb
          image: mongo:7.0
          ports:
            - containerPort: 27017
          env:
            - name: MONGO_INITDB_ROOT_USERNAME
              valueFrom:
                secretKeyRef:
                  name: mongodb-secret
                  key: MONGO_INITDB_ROOT_USERNAME
            - name: MONGO_INITDB_ROOT_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: mongodb-secret
                  key: MONGO_INITDB_ROOT_PASSWORD
            - name: MONGO_INITDB_DATABASE
              value: fifa2026
          resources:
            requests:
              cpu: "250m"
              memory: "512Mi"
            limits:
              cpu: "1"
              memory: "1Gi"
          volumeMounts:
            - name: mongo-data
              mountPath: /data/db
      volumes:
        - name: mongo-data
          persistentVolumeClaim:
            claimName: mongodb-pvc
EOF

# ── 6. Service (NodePort) ──────────────────────────────
kubectl apply -n $NAMESPACE -f - <<EOF
apiVersion: v1
kind: Service
metadata:
  name: mongodb-service
spec:
  type: NodePort
  selector:
    app: mongodb
  ports:
    - port: 27017
      targetPort: 27017
      nodePort: 32017
EOF

# ── 7. Wait for pod to be ready ────────────────────────
echo "⏳ Waiting for MongoDB pod to be ready..."
kubectl rollout status deployment/mongodb -n $NAMESPACE --timeout=120s

# ── 8. Verify PV and PVC ───────────────────────────────
echo ""
echo "📦 PersistentVolume status:"
kubectl get pv mongodb-pv
echo ""
echo "📦 PersistentVolumeClaim status:"
kubectl get pvc mongodb-pvc -n $NAMESPACE

# ── 9. Print connection info ───────────────────────────
POD=$(kubectl get pod -n $NAMESPACE -l app=mongodb -o jsonpath='{.items[0].metadata.name}')
echo ""
echo "✅ MongoDB is running!"
echo ""
echo "  Pod:              $POD"
echo "  Namespace:        $NAMESPACE"
echo "  Username:         $MONGO_USER"
echo "  Password:         $MONGO_PASS"
echo "  Database:         fifa2026"
echo "  Data stored at:   /mnt/fifa2026-mongodb (on the node)"
echo ""
echo "  Connect from inside cluster:"
echo "    mongodb://$MONGO_USER:$MONGO_PASS@mongodb-service.$NAMESPACE.svc.cluster.local:27017/fifa2026?authSource=admin"
echo ""
echo "  Connect from your laptop (port-forward):"
echo "    kubectl port-forward -n $NAMESPACE svc/mongodb-service 27017:27017"
echo "    mongodb://$MONGO_USER:$MONGO_PASS@localhost:27017/fifa2026?authSource=admin"
echo ""
echo "  Open a shell inside MongoDB:"
echo "    kubectl exec -it -n $NAMESPACE $POD -- mongosh -u $MONGO_USER -p $MONGO_PASS --authenticationDatabase admin"