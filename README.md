# railway-v3.0-8080

Long-term-stability Railway + Xray XHTTP/REALITY service migrated from the verified `long-term-stable-frozen` baseline of `railway-v2.0-8080`.

## Runtime baseline

- Dockerfile deployment
- Gateway: `8080`
- Xray REALITY + XHTTP: `10087`
- Xray plain XHTTP: `10086`
- 1 HTTPS/XHTTP node + 7 verified REALITY SNI nodes
- Persistent runtime identity and subscription state under `/data`
- Atomic state writes and restricted runtime backups
- `/health` and `/ready` endpoints
- Railway healthcheck: `/ready`

The transport/runtime baseline is intentionally kept separate from the visual layer.

## Visual layer

`site/index.html` is a self-contained, dependency-free visual landing page. It uses HTML/CSS/native JavaScript only; it does not load Three.js, WebGL, external fonts, images, or CDNs.

It provides:

- Lightweight 3D-style periodic-table views: surface, sphere, helix, grid, particles, wave
- 118 element cards generated locally in the browser
- Solar-system mode with Sun, eight planets, orbital guides, asteroid belt and Kuiper belt
- Pointer rotation and wheel scaling for the periodic-table view
- Responsive mobile layout
- Reduced-motion compatibility

The visual layer is client-rendered and does not participate in Xray/Gateway processing.

## Railway

Deploy the repository as a Docker Service. Public HTTP networking should target container port `8080`. A Railway TCP Proxy is required for the REALITY nodes. A persistent Volume mounted at `/data` is strongly recommended.

Railway-provided `RAILWAY_PUBLIC_DOMAIN`, `RAILWAY_TCP_PROXY_DOMAIN`, and `RAILWAY_TCP_PROXY_PORT` are consumed automatically; `PUBLIC_DOMAIN`, `SERVER_HOST`, and `SERVER_PORT` may override them.

## Verification policy

This v3 repository intentionally does not depend on GitHub Actions as a deployment gate. Validate changes with the production Docker image, `/health`, `/ready`, subscription generation, and a Railway runtime check before promotion.
