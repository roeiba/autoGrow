FROM python:3.11-slim

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    wget \
    gnupg \
    ca-certificates \
    jq \
    && rm -rf /var/lib/apt/lists/*

# Install GitHub CLI
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
    && chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && apt-get update \
    && apt-get install -y gh \
    && rm -rf /var/lib/apt/lists/*

# Create workspace directory
WORKDIR /workspace

# Copy Python requirements and install dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy Python source code
COPY src/ /agent/src/

# Copy prompt templates
COPY prompts/ /agent/prompts/

# Copy shell entrypoint script
COPY scripts/entrypoint.sh /agent-scripts/entrypoint.sh
RUN chmod +x /agent-scripts/entrypoint.sh

# Set up git configuration
RUN git config --global user.name "Claude Agent" && \
    git config --global user.email "claude-agent@automated.local" && \
    git config --global init.defaultBranch main

# Add Python path
ENV PYTHONPATH=/agent:$PYTHONPATH
ENV PYTHONUNBUFFERED=1

# Environment variables (to be provided at runtime)
ENV GITHUB_TOKEN=""
ENV ANTHROPIC_API_KEY=""
ENV REPO_URL=""
ENV ISSUE_NUMBER=""
ENV AGENT_MODE="auto"
ENV PROMPT_TEMPLATE="default"

# Entry point
ENTRYPOINT ["/agent-scripts/entrypoint.sh"]
