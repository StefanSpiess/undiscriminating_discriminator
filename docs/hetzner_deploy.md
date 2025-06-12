# Hosting auf Hetzner Cloud

Diese Anleitung beschreibt ein einfaches Setup, um die Django-Anwendung per Docker-Container auf Hetzner zu betreiben.

## Voraussetzungen
- Hetzner Cloud Konto mit eingerichtetem [Container Registry](https://docs.hetzner.com/de/cloud/containers/registry/) und Kubernetes Cluster
- API-Token für Hetzner Cloud (`HCLOUD_TOKEN`)
- Zugriffsdaten für die Container Registry (`HCR_REGISTRY`, `HCR_USERNAME`, `HCR_PASSWORD`)
- Kubernetes-Konfigurationsdatei (`KUBE_CONFIG`) für den Cluster
- GitHub Repository mit hinterlegten Secrets für die oben genannten Werte

## Schritte
1. **Docker-Image lokal bauen und testen**
   ```bash
   docker build -t $HCR_REGISTRY/undiscriminating-discriminator:local .
   docker run --rm -p 8000:8000 $HCR_REGISTRY/undiscriminating-discriminator:local
   ```
2. **Login bei der Container Registry**
   ```bash
   echo "$HCR_PASSWORD" | docker login $HCR_REGISTRY -u "$HCR_USERNAME" --password-stdin
   ```
3. **Image pushen**
   ```bash
   docker push $HCR_REGISTRY/undiscriminating-discriminator:local
   ```
4. **Deployment im Kubernetes-Cluster aktualisieren**
   ```bash
   kubectl --kubeconfig "$KUBE_CONFIG" set image deployment/undiscriminating-discriminator app=$HCR_REGISTRY/undiscriminating-discriminator:local
   ```

Die folgenden Abschnitte beschreiben einen Beispiel-Workflow für GitHub Actions.

## Beispiel-Workflow für GitHub Actions
Speichere folgende Datei als `.github/workflows/hetzner-deploy.yml` im Repository. Die Secrets müssen zuvor in den Repository-Einstellungen angelegt werden.

```yaml
name: Build and Deploy to Hetzner

on:
  push:
    branches: [ "development" ]
  release:
    types: [ published ]
  workflow_dispatch:

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Hetzner Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ secrets.HCR_REGISTRY }}
          username: ${{ secrets.HCR_USERNAME }}
          password: ${{ secrets.HCR_PASSWORD }}

      - name: Build and push image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ secrets.HCR_REGISTRY }}/undiscriminating-discriminator:${{ github.sha }}

      - name: Setup kubectl
        uses: azure/setup-kubectl@v3
        with:
          version: "latest"

      - name: Deploy to cluster
        env:
          KUBECONFIG: ${{ secrets.KUBE_CONFIG }}
        run: |
          kubectl set image deployment/undiscriminating-discriminator app=${{ secrets.HCR_REGISTRY }}/undiscriminating-discriminator:${{ github.sha }}
```

Der Workflow baut das Docker-Image, pusht es in die Hetzner Container Registry und aktualisiert anschließend das Deployment im Kubernetes-Cluster. Er wird bei Änderungen im Branch `development` sowie beim Veröffentlichen eines Releases ausgeführt.
