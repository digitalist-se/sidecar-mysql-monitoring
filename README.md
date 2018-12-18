# sidecar-mysql-monitoring
Docker or Kubernetes sidecar MySQL monitoring tool for Prometheus.  
Here you can find a detailed description about this tool: https://medium.com/@Adrian_Balcan/mysql-monitor-sidecar-adventure-2f30df33bd33

## How to use it

Run: `sudo docker run -p 9100:9100 adrianbalcan/sidecar-mysql-monitoring`

- This tool is using Scapy (a tcpdump python library), also the reason why it requires root access.
- If you have the MySQL DB on other port, you can change it in `mysql-stats.py` file.
- Grafana Dashboard: [https://grafana.com/dashboards/8367](https://grafana.com/dashboards/8367)
- The python script will flush the scraped data after 30 seconds, so keep your ServiceMonitor interval at 30s.

## Kubernetes integration

### Pod/Deployment/Statefullset/Daemonset
```
      - image: adrianbalcan/sidecar-mysql-monitoring:latest
        name: sidecar-mysql-monitoring
        ports:
        - containerPort: 9100
          name: mysql-metrics
          protocol: TCP
        resources:
          limits:
            cpu: 50m
            memory: 50Mi
          requests:
            cpu: 10m
            memory: 10Mi
```
### ServiceMonitor
```
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: sidecar-mysql-monitoring
  labels:
    k8s-app: my-website
spec:
  selector:
    matchLabels:
      k8s-app: my-website
  namespaceSelector:
    any: true
  endpoints:
  - port: mysql-metrics
    interval: 30s
```
