#!/usr/bin/env python3
"""
Marketing Agent - Specialized issue generator for marketing tasks

Focuses on:
- Content creation and campaigns
- SEO and analytics
- Social media and community engagement
- Brand awareness and growth strategies
- User acquisition and retention
"""

from typing import Dict
from .base_issue_agent import BaseIssueAgent, AgentConfig


class MarketingAgent(BaseIssueAgent):
    """
    Marketing-focused issue generator
    
    Creates issues related to marketing initiatives, content strategy,
    user acquisition, brand building, and growth tactics.
    """

    def get_agent_config(self) -> AgentConfig:
        """Configure the marketing agent"""
        return AgentConfig(
            domain="marketing",
            default_labels=["marketing", "growth"],
            min_issues=2,
            focus_areas=[
                "Content marketing and blog posts",
                "SEO optimization and analytics",
                "Social media campaigns",
                "Email marketing and newsletters",
                "Community building and engagement",
                "Brand awareness initiatives",
                "User acquisition strategies",
                "Marketing automation",
                "Landing pages and conversion optimization",
                "Partnership and collaboration opportunities"
            ],
            priority_keywords=[
                "campaign", "content", "seo", "social", "growth",
                "engagement", "acquisition", "brand", "analytics", "conversion"
            ]
        )

    def build_domain_prompt(self, context: Dict) -> str:
        """Build marketing-specific prompt"""
        config = self.get_agent_config()
        
        prompt = f"""
🎯 MARKETING FOCUS AREAS:
{chr(10).join([f"  • {area}" for area in config.focus_areas])}

Your task is to identify {context['needed']} high-impact marketing opportunities for this project.

Consider:
1. **Content Strategy**: What content would attract and engage users?
2. **Growth Channels**: Which marketing channels should be explored?
3. **Brand Building**: How can we strengthen the project's brand and visibility?
4. **User Acquisition**: What tactics could drive more users to the project?
5. **Community Engagement**: How can we build and nurture a community?
6. **Analytics & Optimization**: What metrics should we track and optimize?

Focus on actionable marketing tasks that will:
- Increase project visibility and awareness
- Drive user acquisition and retention
- Build community and engagement
- Establish thought leadership
- Optimize conversion funnels

Each issue should be specific, measurable, and aligned with modern marketing best practices.
"""
        return prompt
