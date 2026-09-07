"""PaperTrace validation library."""
from .model import REQUIRED_DIRS, REQUIRED_FILES, STAGE_SKILLS, Reporter
from .ideas import validate_intake
from .methods import validate_method_design
from .figures import validate_figure_arguments
from .project import validate_paper_state, validate_required_layout
from .graph import validate_research_graph
from .gates import validate_stage_gates

__all__ = [
    "REQUIRED_DIRS",
    "REQUIRED_FILES",
    "STAGE_SKILLS",
    "Reporter",
    "validate_intake",
    "validate_method_design",
    "validate_figure_arguments",
    "validate_paper_state",
    "validate_required_layout",
    "validate_research_graph",
    "validate_stage_gates",
]
