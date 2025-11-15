# Makefile - Auto-detect OS and use appropriate Makefile
# AI Project Template

# Detect operating system
UNAME_S := $(shell uname -s)

ifeq ($(UNAME_S),Darwin)
    OS_MAKEFILE := Makefile.macos
    OS_NAME := macOS
else ifeq ($(UNAME_S),Linux)
    OS_MAKEFILE := Makefile.linux
    OS_NAME := Linux
else
    $(error Unsupported operating system: $(UNAME_S))
endif

# Default target
.DEFAULT_GOAL := help

# Show detected OS
.PHONY: show-os
show-os:
	@echo "Detected OS: $(OS_NAME)"
	@echo "Using: $(OS_MAKEFILE)"

# Forward all targets to the OS-specific Makefile
%:
	@$(MAKE) -f $(OS_MAKEFILE) $@
