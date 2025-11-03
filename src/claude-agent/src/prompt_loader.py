"""Prompt template loader and formatter"""

from pathlib import Path
from typing import Dict, Any, Optional


class PromptLoader:
    """Load and format prompt templates"""
    
    def __init__(self, prompts_dir: Path = None):
        """
        Initialize prompt loader
        
        Args:
            prompts_dir: Directory containing prompt templates
        """
        if prompts_dir is None:
            # Default to prompts directory relative to this file
            self.prompts_dir = Path(__file__).parent.parent / 'prompts'
        else:
            self.prompts_dir = Path(prompts_dir)
    
    def load_template(self, template_name: str, custom_path: Optional[str] = None) -> str:
        """
        Load a prompt template
        
        Args:
            template_name: Name of the template (e.g., 'default', 'minimal', 'detailed')
            custom_path: Optional custom path to template file
            
        Returns:
            Template content as string
            
        Raises:
            FileNotFoundError: If template file doesn't exist
        """
        if custom_path:
            template_path = Path(custom_path)
        else:
            template_path = self.prompts_dir / f"{template_name}.txt"
        
        if not template_path.exists():
            raise FileNotFoundError(
                f"Prompt template not found: {template_path}\n"
                f"Available templates: {self.list_templates()}"
            )
        
        return template_path.read_text()
    
    def format_prompt(self, template: str, context: Dict[str, Any]) -> str:
        """
        Format a prompt template with context variables
        
        Args:
            template: Template string with {variable} placeholders
            context: Dictionary of variables to substitute
            
        Returns:
            Formatted prompt string
        """
        # Convert lists to comma-separated strings
        formatted_context = {}
        for key, value in context.items():
            if isinstance(value, list):
                formatted_context[key] = ', '.join(str(v) for v in value)
            elif value is None:
                formatted_context[key] = ''
            else:
                formatted_context[key] = str(value)
        
        try:
            return template.format(**formatted_context)
        except KeyError as e:
            raise ValueError(
                f"Missing required variable in prompt template: {e}\n"
                f"Available variables: {list(formatted_context.keys())}"
            )
    
    def list_templates(self) -> list[str]:
        """
        List available prompt templates
        
        Returns:
            List of template names (without .txt extension)
        """
        if not self.prompts_dir.exists():
            return []
        
        templates = []
        for file in self.prompts_dir.glob('*.txt'):
            templates.append(file.stem)
        
        return sorted(templates)
    
    def get_template_info(self, template_name: str) -> Dict[str, Any]:
        """
        Get information about a template
        
        Args:
            template_name: Name of the template
            
        Returns:
            Dictionary with template metadata
        """
        template_path = self.prompts_dir / f"{template_name}.txt"
        
        if not template_path.exists():
            return {
                'name': template_name,
                'exists': False,
                'path': str(template_path)
            }
        
        content = template_path.read_text()
        
        # Extract variables from template
        import re
        variables = set(re.findall(r'\{(\w+)\}', content))
        
        return {
            'name': template_name,
            'exists': True,
            'path': str(template_path),
            'size': len(content),
            'lines': content.count('\n') + 1,
            'variables': sorted(variables)
        }


def load_and_format_prompt(
    template_name: str,
    context: Dict[str, Any],
    custom_path: Optional[str] = None
) -> str:
    """
    Convenience function to load and format a prompt in one call
    
    Args:
        template_name: Name of the template
        context: Context variables for formatting
        custom_path: Optional custom template path
        
    Returns:
        Formatted prompt string
    """
    loader = PromptLoader()
    template = loader.load_template(template_name, custom_path)
    return loader.format_prompt(template, context)
