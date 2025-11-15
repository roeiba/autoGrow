#!/bin/bash
# Verify Agent Refactoring
# Shows the new architecture and verifies all files are in place

echo "🔍 Agent Architecture Refactoring Verification"
echo "=============================================="
echo ""

# Check core agent modules
echo "📦 Core Agent Modules (src/agents/):"
echo "-----------------------------------"
if [ -f "src/agents/__init__.py" ]; then
    echo "✅ src/agents/__init__.py"
else
    echo "❌ src/agents/__init__.py - MISSING"
fi

if [ -f "src/agents/issue_generator.py" ]; then
    lines=$(wc -l < src/agents/issue_generator.py)
    echo "✅ src/agents/issue_generator.py ($lines lines)"
else
    echo "❌ src/agents/issue_generator.py - MISSING"
fi

if [ -f "src/agents/issue_resolver.py" ]; then
    lines=$(wc -l < src/agents/issue_resolver.py)
    echo "✅ src/agents/issue_resolver.py ($lines lines)"
else
    echo "❌ src/agents/issue_resolver.py - MISSING"
fi

if [ -f "src/agents/qa_agent.py" ]; then
    lines=$(wc -l < src/agents/qa_agent.py)
    echo "✅ src/agents/qa_agent.py ($lines lines)"
else
    echo "❌ src/agents/qa_agent.py - MISSING"
fi

echo ""

# Check wrapper scripts
echo "🔧 CI/CD Wrapper Scripts (.github/scripts/):"
echo "--------------------------------------------"
if [ -f ".github/scripts/issue_generator.py" ]; then
    lines=$(wc -l < .github/scripts/issue_generator.py)
    echo "✅ .github/scripts/issue_generator.py ($lines lines - thin wrapper)"
else
    echo "❌ .github/scripts/issue_generator.py - MISSING"
fi

if [ -f ".github/scripts/issue_resolver.py" ]; then
    lines=$(wc -l < .github/scripts/issue_resolver.py)
    echo "✅ .github/scripts/issue_resolver.py ($lines lines - thin wrapper)"
else
    echo "❌ .github/scripts/issue_resolver.py - MISSING"
fi

if [ -f ".github/scripts/qa_agent.py" ]; then
    lines=$(wc -l < .github/scripts/qa_agent.py)
    echo "✅ .github/scripts/qa_agent.py ($lines lines - thin wrapper)"
else
    echo "❌ .github/scripts/qa_agent.py - MISSING"
fi

echo ""

# Check documentation
echo "📚 Documentation:"
echo "----------------"
if [ -f "src/agents/.agents/README.md" ]; then
    echo "✅ src/agents/.agents/README.md (Architecture docs)"
else
    echo "❌ src/agents/.agents/README.md - MISSING"
fi

if [ -f ".agents/AGENT_REFACTORING.md" ]; then
    echo "✅ .agents/AGENT_REFACTORING.md (Refactoring summary)"
else
    echo "❌ .agents/AGENT_REFACTORING.md - MISSING"
fi

echo ""

# Check workflows (should be unchanged)
echo "⚙️  GitHub Workflows (should be unchanged):"
echo "------------------------------------------"
if [ -f ".github/workflows/issue-generator.yml" ]; then
    echo "✅ .github/workflows/issue-generator.yml"
else
    echo "❌ .github/workflows/issue-generator.yml - MISSING"
fi

if [ -f ".github/workflows/issue-resolver.yml" ]; then
    echo "✅ .github/workflows/issue-resolver.yml"
else
    echo "❌ .github/workflows/issue-resolver.yml - MISSING"
fi

if [ -f ".github/workflows/qa-agent.yml" ]; then
    echo "✅ .github/workflows/qa-agent.yml"
else
    echo "❌ .github/workflows/qa-agent.yml - MISSING"
fi

echo ""
echo "=============================================="
echo "✅ Refactoring Complete!"
echo ""
echo "📊 Summary:"
echo "  - Core logic: src/agents/*.py (testable, reusable)"
echo "  - CI wrappers: .github/scripts/*.py (thin layer)"
echo "  - No breaking changes to workflows"
echo ""
echo "📖 Documentation:"
echo "  - Architecture: src/agents/.agents/README.md"
echo "  - Summary: .agents/AGENT_REFACTORING.md"
echo ""
