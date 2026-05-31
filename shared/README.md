# Shared Resources

This directory contains resources shared across all CampusHub microservices.

## Contents

- **error-response-schema.json** - JSON Schema defining the standard error response format. All services should return errors matching this schema.
- **jwt-public-key.pem** - Mock RSA public key for JWT token validation during development. The Auth service signs tokens with the corresponding private key; all other services use this public key to verify them.

## Usage

Services reference these shared resources to ensure consistency:

- Error responses follow the schema: `{ "error": "CODE", "message": "description", "status": 400 }`
- JWT validation uses the public key to verify tokens issued by the Auth service

## Important

The `jwt-public-key.pem` file is a **mock key for development only**. In production, this would be replaced with a real RSA public key and distributed securely.
