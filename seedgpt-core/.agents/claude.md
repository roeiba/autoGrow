the Claude CLI agent and the Anthropic SDK are not the same thing, but they are closely related and complementary tools. The Claude CLI agent (also known as Claude Code) is a standalone command-line interface application, while the Anthropic SDK (specifically the Claude Agent SDK for Python, Node.js, etc.) is a library for building custom applications and agents. 
Claude CLI Agent (Claude Code)
Functionality: A ready-to-use tool that brings the power of Claude directly into your terminal or IDE (via extensions).
Use Case: Designed for immediate, interactive tasks like asking questions about a codebase, generating code snippets, fixing bugs, managing git workflows, running tests, and more, within your existing development environment.
Design: Intentionally low-level and "unopinionated," it provides close to raw model access and flexibility without forcing specific workflows.
Installation: Typically installed via a package manager (e.g., npm install -g @anthropic-ai/claude-code). 
Anthropic SDK (Claude Agent SDK)
Functionality: A collection of tools and libraries (e.g., in Python) that allows developers to programmatically build and integrate Claude's agentic capabilities into their own applications.
Use Case: Provides the underlying infrastructure (the same core agent harness that powers Claude Code) to build custom agents with specific tools, hooks, memory management, and permissions. It's for creating new, autonomous AI applications beyond just coding, such as an email agent or a research assistant.
Design: Provides the primitives (file system operations, bash execution, MCP integration, etc.) needed to automate complex, long-running tasks in a controlled and customizable manner.
Relationship to CLI: You can think of the SDK as the foundation upon which the Claude CLI agent is built, and which you can use to create similar or entirely different agentic tools. 
In short, the CLI is an end-user application, while the SDK is a developer toolkit used to build applications (including the CLI itself) that leverage Claude's agentic capabilities. 