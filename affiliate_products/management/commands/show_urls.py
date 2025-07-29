# affiliate_products/management/commands/show_urls.py
from django.core.management.base import BaseCommand
from django.urls import get_resolver
from collections import deque

class Command(BaseCommand):
    help = 'Show all URLs in the project'

    def handle(self, *args, **options):
        resolver = get_resolver()
        queue = deque([(resolver, '')])
        
        while queue:
            current_resolver, path_prefix = queue.popleft()
            
            for pattern in current_resolver.url_patterns:
                if hasattr(pattern, 'url_patterns'):  # URLResolver
                    queue.append((pattern, f"{path_prefix}{pattern.pattern}"))
                else:  # URLPattern
                    self.stdout.write(f"{path_prefix}{pattern.pattern} -> {pattern.name or '(no name)'}")