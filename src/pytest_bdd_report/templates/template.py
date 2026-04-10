from abc import ABC, abstractmethod
from pathlib import Path

from jinja2 import Environment, FileSystemBytecodeCache, FileSystemLoader, Template

RESOURCES_PATH = Path(__file__).parent.joinpath("html_templates")

# Enable bytecode caching to avoid recompiling templates on every run
_cache_dir = RESOURCES_PATH / ".jinja2_cache"
_cache_dir.mkdir(parents=True, exist_ok=True)
_bytecode_cache = FileSystemBytecodeCache(str(_cache_dir))
ENVIRONMENT = Environment(
    loader=FileSystemLoader([RESOURCES_PATH]),
    bytecode_cache=_bytecode_cache,
    cache_size=10,  # Cache up to 10 parsed templates in memory
)


class BaseTemplate(ABC):
    # Class-level cache for compiled Jinja2 templates
    _template_cache: dict[str, Template] = {}

    def __init__(self, path: str) -> None:
        self.path: str = path
        self.template: Template = self._load_template()

    def _load_template(self) -> Template:
        """
        Load the template from cache or disk.
        Uses class-level cache to avoid repeated disk reads and compilation.
        @return: compiled template
        """
        if self.path not in self._template_cache:
            self._template_cache[self.path] = ENVIRONMENT.get_template(self.path)
        return self._template_cache[self.path]

    @abstractmethod
    def render_template(self, data, already_rendered_data: str = "") -> str:
        """
        Render the template with the data provided.
        @param data: object to render
        @param already_rendered_data: (optional) rendered object to inject as plain html
        @return: rendered object
        """
        ...
