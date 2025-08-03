# Example OAuth Flow with Keycloak

## Run
1. `docker compose up`
2. Navigate to `http://localhost:8000/`
3. This should bring you to an unprotected html page
4. Click "protected"
5. This should route you to a keycloak login page
6. Login with the username, and password (admin, admin)
7. You should be redirected back to a similar page saying you're logged in