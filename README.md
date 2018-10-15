# sidecar-mysql-monitoring
Docker or Kubernetes sidecar MySQL monitoring tool for Prometheus

## How to use it

Run: `sudo docker run -p 9100:9100 adrianbalcan/sidecar-mysql-monitoring`

- This tool is using Scapy (a tcpdump python library), also the reason why it requires root access.
- If you have the MySQL DB on other port, you can change it in `mysql-stats.py` file.
- Grafana Dashboard: [https://grafana.com/dashboards/8367](https://grafana.com/dashboards/8367)


### Kubernetes integration

```
      - image: adrianbalcan/sidecar-mysql-monitoring:latest
        name: sidecar-mysql-monitoring
        ports:
        - containerPort: 9100
          name: metrics
          protocol: TCP
        resources:
          limits:
            cpu: 50m
            memory: 50Mi
          requests:
            cpu: 10m
            memory: 10Mi
```
