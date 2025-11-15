#!/usr/bin/env python3
"""
Multi-Agent Workflow Example
Demonstrates using both Claude and Gemini agents together
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import gemini_agent
sys.path.insert(0, str(Path(__file__).parent.parent))

from gemini_agent import GeminiAgent


class MultiAgentWorkflow:
    """
    Example workflow using both Claude and Gemini agents.

    Use cases:
    - Claude for complex reasoning and code generation
    - Gemini for quick analysis, reviews, and documentation
    """

    def __init__(self):
        """Initialize both agents."""
        # Load environment
        self._load_env()

        # Initialize Gemini agent
        self.gemini = GeminiAgent(debug=False)

        print("🤖 Multi-Agent Workflow Initialized")
        print("  - Gemini Agent: Ready")
        print("  - Claude Agent: Available via agentic_workflow.py")

    def _load_env(self):
        """Load environment variables from .env file."""
        env_file = Path(__file__).parent.parent / ".env"
        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    if line.strip() and not line.startswith("#"):
                        key, value = line.strip().split("=", 1)
                        os.environ[key] = value

    def analyze_issue(self, issue_description: str) -> dict:
        """
        Use Gemini to quickly analyze an issue and provide initial assessment.

        Args:
            issue_description: The issue description

        Returns:
            Analysis results
        """
        print("\n🔍 Analyzing issue with Gemini...")

        prompt = f"""Analyze this GitHub issue and provide:
        1. Issue type (bug, feature, documentation, etc.)
        2. Severity level (critical, high, medium, low)
        3. Estimated complexity (simple, moderate, complex)
        4. Key areas of codebase likely affected
        5. Recommended approach
        
        Issue:
        {issue_description}
        
        Provide a structured analysis."""

        result = self.gemini.query(prompt, model="gemini-2.5-flash")
        return result

    def review_code_changes(self, file_path: str) -> dict:
        """
        Use Gemini to review code changes before committing.

        Args:
            file_path: Path to the file to review

        Returns:
            Review results
        """
        print(f"\n📝 Reviewing code with Gemini: {file_path}")
        return self.gemini.code_review(file_path)

    def generate_pr_description(self, changes_summary: str, issue_number: int) -> dict:
        """
        Use Gemini to generate a comprehensive PR description.

        Args:
            changes_summary: Summary of changes made
            issue_number: Related issue number

        Returns:
            PR description
        """
        print(f"\n📄 Generating PR description for issue #{issue_number}...")

        prompt = f"""Generate a comprehensive Pull Request description for these changes:

        Issue: #{issue_number}
        Changes: {changes_summary}
        
        Include:
        1. Summary of changes
        2. Technical details
        3. Testing recommendations
        4. Potential impacts
        5. Checklist for reviewers
        
        Format as Markdown."""

        result = self.gemini.query(prompt, model="gemini-2.5-pro")
        return result

    def validate_fix(self, original_issue: str, fix_description: str) -> dict:
        """
        Use Gemini to validate that a fix addresses the original issue.

        Args:
            original_issue: The original issue description
            fix_description: Description of the fix

        Returns:
            Validation results
        """
        print("\n✅ Validating fix with Gemini...")

        prompt = f"""Validate if this fix properly addresses the issue:

        Original Issue:
        {original_issue}
        
        Proposed Fix:
        {fix_description}
        
        Provide:
        1. Does the fix address the root cause? (Yes/No)
        2. Are there any gaps or missing considerations?
        3. Potential side effects or risks
        4. Recommendations for testing
        5. Overall confidence level (High/Medium/Low)"""

        result = self.gemini.query(prompt, model="gemini-2.5-pro")
        return result

    def generate_documentation(self, code_path: str) -> dict:
        """
        Use Gemini to generate documentation for code changes.

        Args:
            code_path: Path to code file or directory

        Returns:
            Generated documentation
        """
        print(f"\n📚 Generating documentation with Gemini: {code_path}")

        if os.path.isfile(code_path):
            return self.gemini.generate_docs(code_path)
        else:
            # For directories, generate overview
            prompt = f"""Generate comprehensive documentation for this codebase at {code_path}.
            Include:
            1. Overview
            2. Architecture
            3. Key components
            4. Usage examples
            5. Setup instructions
            
            Format as Markdown."""

            result = self.gemini.query(
                prompt, include_dirs=[code_path], model="gemini-2.5-pro"
            )
            return result


def example_workflow():
    """Example: Complete issue resolution workflow with multi-agent approach."""

    print("=" * 70)
    print("Multi-Agent Workflow Example")
    print("=" * 70)

    try:
        workflow = MultiAgentWorkflow()

        # Example issue
        issue_description = """
        Bug: Application crashes when processing large CSV files
        
        When uploading CSV files larger than 100MB, the application runs out of memory
        and crashes. This happens in the data processing module.
        
        Steps to reproduce:
        1. Upload a CSV file > 100MB
        2. Click 'Process Data'
        3. Application crashes with OutOfMemoryError
        
        Expected: Should process large files without crashing
        Actual: Crashes with memory error
        """

        # Step 1: Analyze issue with Gemini (fast initial analysis)
        print("\n" + "=" * 70)
        print("STEP 1: Initial Issue Analysis")
        print("=" * 70)

        analysis = workflow.analyze_issue(issue_description)
        print("\nAnalysis Result:")
        print(analysis.get("response", "No response"))

        # Step 2: At this point, you would use Claude for complex code generation
        print("\n" + "=" * 70)
        print("STEP 2: Generate Fix (Claude Agent)")
        print("=" * 70)
        print("📌 Note: This would use Claude via agentic_workflow.py")
        print("   Claude excels at complex code generation and reasoning")

        # Simulated fix description
        fix_description = """
        Implemented streaming CSV processing:
        - Changed from loading entire file to memory to streaming approach
        - Process data in chunks of 10,000 rows
        - Added progress tracking
        - Implemented proper resource cleanup
        """

        # Step 3: Validate fix with Gemini
        print("\n" + "=" * 70)
        print("STEP 3: Validate Fix")
        print("=" * 70)

        validation = workflow.validate_fix(issue_description, fix_description)
        print("\nValidation Result:")
        print(validation.get("response", "No response"))

        # Step 4: Generate PR description
        print("\n" + "=" * 70)
        print("STEP 4: Generate PR Description")
        print("=" * 70)

        pr_desc = workflow.generate_pr_description(fix_description, 123)
        print("\nPR Description:")
        print(pr_desc.get("response", "No response"))

        print("\n" + "=" * 70)
        print("✅ Workflow Complete!")
        print("=" * 70)
        print("\nThis example demonstrates:")
        print("  1. Gemini for quick analysis and validation")
        print("  2. Claude for complex code generation (via agentic_workflow.py)")
        print("  3. Gemini for documentation and PR descriptions")
        print("\nBenefits of multi-agent approach:")
        print("  - Use the right tool for each task")
        print("  - Faster initial analysis with Gemini")
        print("  - Complex reasoning with Claude")
        print("  - Cost optimization")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


def main():
    """Main entry point."""
    if len(sys.argv) > 1 and sys.argv[1] == "example":
        return example_workflow()

    # Interactive mode
    print("🤖 Multi-Agent Workflow")
    print("\nUsage:")
    print("  python multi_agent_workflow.py example    # Run example workflow")
    print("\nOr import and use in your code:")
    print("  from multi_agent_workflow import MultiAgentWorkflow")
    print("  workflow = MultiAgentWorkflow()")
    print("  result = workflow.analyze_issue('...')")

    return 0


if __name__ == "__main__":
    sys.exit(main())
