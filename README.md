# Google Scholar MCP

This project implements a Model Context Protocol (MCP) server for Google Scholar.

## Setup with VS Code and Docker

Follow these steps to set up and run the server in your local environment using VS Code and Docker.

### 1. Build the Docker Image

Open a terminal in the root of the project and run the following command to build the Docker image:

```bash
docker build . --tag "scholar-mcp"
```

### 2. Configure VS Code

To allow VS Code to communicate with the MCP server running in Docker, you need to create a configuration file.

1. Create a directory named `.vscode` in the root of the project if it doesn't already exist.
2. Inside the `.vscode` directory, create a file named `mcp.json`.
3. Add the following content to `mcp.json`:

    ```json
    {
      "servers": {
        "scholar_mcp": {
          "command": "docker",
          "args": ["run", "-i", "--rm", "scholar-mcp"]
        }
      }
    }
    ```

Now you can use the MCP features from within VS Code, which will connect to the server running in the Docker container.
