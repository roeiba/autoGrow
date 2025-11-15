#!/usr/bin/env python3
"""
Product Agent - Specialized issue generator for product development tasks

Focuses on:
- Feature development and roadmap
- User experience and design
- Product analytics and metrics
- User feedback and research
- Product strategy and vision
"""

from typing import Dict
from .base_issue_agent import BaseIssueAgent, AgentConfig


class ProductAgent(BaseIssueAgent):
    """
    Product-focused issue generator
    
    Creates issues related to product features, UX improvements,
    user research, product strategy, and roadmap planning.
    """

    def get_agent_config(self) -> AgentConfig:
        """Configure the product agent"""
        return AgentConfig(
            domain="product",
            default_labels=["product", "feature"],
            min_issues=2,
            focus_areas=[
                "Feature development and enhancement",
                "User experience (UX) improvements",
                "User interface (UI) design",
                "Product analytics and metrics",
                "User research and feedback",
                "Product roadmap planning",
                "A/B testing and experiments",
                "Onboarding and user flows",
                "Accessibility improvements",
                "Mobile and responsive design"
            ],
            priority_keywords=[
                "feature", "ux", "ui", "design", "user",
                "experience", "analytics", "roadmap", "research", "accessibility"
            ]
        )

    def build_domain_prompt(self, context: Dict) -> str:
        """Build product-specific prompt"""
        config = self.get_agent_config()
        
        prompt = f"""
🚀 PRODUCT FOCUS AREAS:
{chr(10).join([f"  • {area}" for area in config.focus_areas])}

Your task is to identify {context['needed']} high-value product opportunities for this project.

Consider:
1. **Feature Development**: What new features would provide the most user value?
2. **User Experience**: How can we improve the user journey and satisfaction?
3. **Product Analytics**: What metrics and data should we track?
4. **User Research**: What do we need to learn about our users?
5. **Design System**: How can we improve consistency and usability?
6. **Product Strategy**: What should be on the roadmap for maximum impact?

Focus on actionable product tasks that will:
- Enhance user value and satisfaction
- Improve core product metrics
- Streamline user workflows
- Increase product adoption
- Differentiate from competitors

Each issue should be user-centric, data-driven, and aligned with product best practices.
"""
        return prompt
