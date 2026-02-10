Frontend scaffold for Angular 17 + Tailwind + PrimeNG + Angular Material.

This folder contains a minimal Angular 17 standalone-component scaffold and example services wired to the backend API.

Quick start:

1. If you don't have the Angular CLI, install it:

```bash
npm install -g @angular/cli
```

2. From the `frontend` folder, install dependencies:

```bash
npm install
```

3. Create a proxy to forward API calls to backend. Create `proxy.conf.json` in this folder with:

```json
{
	"/auth": { "target": "http://localhost:8000", "secure": false },
	"/accounts": { "target": "http://localhost:8000", "secure": false },
	"/transactions": { "target": "http://localhost:8000", "secure": false }
}
```

4. Start the dev server with the proxy:

```bash
ng serve --proxy-config proxy.conf.json
```

Notes:
- The provided services live in `src/app/services` and use relative endpoints (e.g. `/auth/login`).
- Tailwind and PrimeNG integration can be added after the initial scaffold; ask me and I will add the Tailwind config and sample PrimeNG components.
