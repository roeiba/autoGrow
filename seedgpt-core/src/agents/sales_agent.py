#!/usr/bin/env python3
"""
Sales Agent - Specialized issue generator for sales and revenue tasks

Focuses on:
- Sales enablement and tools
- Pricing and monetization
- Customer success and support
- Sales funnel optimization
- Revenue growth strategies
"""

from typing import Dict
from .base_issue_agent import BaseIssueAgent, AgentConfig


class SalesAgent(BaseIssueAgent):
    """
    Sales-focused issue generator
    
    Creates issues related to sales enablement, revenue generation,
    customer success, pricing strategy, and sales operations.
    """

    def get_agent_config(self) -> AgentConfig:
        """Configure the sales agent"""
        return AgentConfig(
            domain="sales",
            default_labels=["sales", "revenue"],
            min_issues=2,
            focus_areas=[
                "Sales enablement and tools",
                "Pricing and monetization strategy",
                "Customer success and onboarding",
                "Sales funnel optimization",
                "CRM and sales automation",
                "Demo and trial experiences",
                "Customer support improvements",
                "Upsell and cross-sell opportunities",
                "Sales analytics and reporting",
                "Partnership and channel sales"
            ],
            priority_keywords=[
                "sales", "revenue", "pricing", "monetization", "customer",
                "conversion", "funnel", "crm", "support", "success"
            ]
        )

    def build_domain_prompt(self, context: Dict) -> str:
        """Build sales-specific prompt"""
        config = self.get_agent_config()
        
        prompt = f"""
💰 SALES FOCUS AREAS:
{chr(10).join([f"  • {area}" for area in config.focus_areas])}

Your task is to identify {context['needed']} high-impact sales opportunities for this project.

Consider:
1. **Sales Enablement**: What tools and resources would help close more deals?
2. **Monetization**: How can we optimize pricing and revenue streams?
3. **Customer Success**: How can we improve customer satisfaction and retention?
4. **Sales Funnel**: Where are the bottlenecks in the conversion process?
5. **Sales Operations**: What processes and automation can improve efficiency?
6. **Revenue Growth**: What strategies would drive sustainable revenue growth?

Focus on actionable sales tasks that will:
- Increase conversion rates and revenue
- Improve sales efficiency and velocity
- Enhance customer lifetime value
- Reduce churn and increase retention
- Scale sales operations

Each issue should be revenue-focused, measurable, and aligned with modern sales best practices.
"""
        return prompt
