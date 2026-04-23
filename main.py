import sys
from pathlib import Path

# Add sibling packages to sys.path for proper module resolution
code_dir = Path(__file__).parent
# Add SportsAppService directory so that 'app' subpackage can be found
sys.path.insert(0, str(code_dir / "SportsAppService"))
# Add SportsAppModels parent so "SportsAppModels.models" resolves correctly
sys.path.insert(0, str(code_dir / "SportsAppModels"))

from app.main import app

__all__ = ["app"]
