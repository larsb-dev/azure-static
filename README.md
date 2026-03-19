# Static Web Apps

## Create the Web App

```bash
npm create vite@latest app-name
```

- This sets up a new app

## Manual Deployment

- Let's you deploy static web apps directly from the CLI, let's explore this a bit further
- If your frontend builds to static files, SWA can serve it
	- Vue.js
	- React
	- Angular
	- etc.
- Vue Router works by default
- Can also handle...
	- Serverless APIs via Azure Functions
	- AuthN/AuthZ built-in
	- Custom domains & SSL
	- Env vars

### swa init

- Run this command in the project folder
- Creates a `swa-cli-config.json` file with configurations
- Could technically also be in the `projects` folder and contain all the projects
- Need to specify the key of the config object

```bash
swa <command> myApp
```

### swa build

- Can be used to build frontend and API
- Uses settings specified in the `swa-cli.config.json`

### swa start

```bash
swa start http://localhost:5173 --run "npm run dev" --api-location ./api
```

- You can serve the web app from a dev server
- Add the correct default port, in this case Vite's port, and the command to start the dev server
- The Python Azure function is located in the ./api folder
- You could also start the API server manually which would involve `func host start` from the Azure Functions Core Tools and another SWA command
- The app will be available on port 4280 by default

### swa deploy

```bash
{
  "platform": {
    "apiRuntime": "python:3.11"
  }
}
```

- Add a `staticwebapp.config.json` file to the project rood and declare the apiRuntime version

```bash
npm run build
swa deploy ./dist --api-location ./api
```

- Will deploy the contents of the dist folder and the serverless function

## Automatic Deployment

### Env vars

```bash
- name: Install & Build Vue App
  run: |
    npm install
    npm run build
  env:
    VITE_APP_ENVIRONMENT: ${{ github.ref == 'refs/heads/main' && secrets.APP_ENVIRONMENT_PRODUCTION || secrets.APP_ENVIRONMENT_DEVELOPMENT }}
```

- In the workflow you specify env vars by pulling the value from repository secrets
- They will be injected at build time
- This requires a manual build which gives more control

###  SWA step

```bash
- name: Deploy to Azure SWA
  uses: Azure/static-web-apps-deploy@v1
  with:
    azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
    repo_token: ${{ secrets.GITHUB_TOKEN }} # used for PRs and comments
    action: "upload"
    production_branch: "main" # force production branch mapping
    app_location: "dist" # deploy prebuilt Vite artifact directly
    skip_app_build: true # already built above
    api_location: "api" # Azure Function folder
    deployment_environment: "Development" # set environment for non-production branches

```

- When we build the app manually, see above, the app location is the dist folder in the root of the project
- We can skip the app build

## Realizations

- If you wanna use the Azure env vars you have to deploy to Azure and not use GitHub Actions!
- `swa-cli.config.json` is only relevant for local manual swa deploy
- `staticwebapp.config.json` is used by Azure at runtime and is copied to dist during build

## See Also

- [Static Web Apps CLI](https://azure.github.io/static-web-apps-cli/)
- [Build configuration for Azure Static Web Apps](https://learn.microsoft.com/en-us/azure/static-web-apps/build-configuration?tabs=identity&pivots=github-actions#build-and-deploy)
- [Create named preview environments in Azure Static Web Apps](https://learn.microsoft.com/en-us/azure/static-web-apps/named-environments?tabs=github-actions)
