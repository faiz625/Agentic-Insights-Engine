# ---- Build stage ----
FROM node:20-bullseye AS build
WORKDIR /app

# 1) Install deps (include devDeps so vite exists)
COPY frontend/package.json frontend/package-lock.json* ./
# If no lockfile, fall back; ensure devDeps (production=false)
RUN npm ci --omit=optional || npm install --production=false

# 2) Ensure vite + plugin present (belt & suspenders)
RUN npm install -D vite @vitejs/plugin-react

# 3) Copy source
COPY frontend/ ./

# (optional) sanity check
RUN node -v && ls -la node_modules/.bin

# 4) **Call Vite via node’s JS entry (bypasses shell wrappers)**
RUN node ./node_modules/vite/bin/vite.js build

# ---- Runtime stage ----
FROM nginx:1.27-alpine AS runtime
RUN rm -rf /usr/share/nginx/html/*
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --retries=5 \
  CMD wget -qO- http://127.0.0.1:8080/ >/dev/null || exit 1
CMD ["nginx", "-g", "daemon off;"]
