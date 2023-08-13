from datetime import datetime

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiExample


play_doc_params = [
    OpenApiParameter(
        "title",
        type=str,
        description="Filter by title name (e.g. ?title=name_of_the_play)",
    ),
    OpenApiParameter(
        "genres",
        type={"type": "list", "items": {"type": "number"}},
        description="Filter by genre id (e.g. ?genres=1,2,5)",
    ),
    OpenApiParameter(
        "actors",
        type={"type": "list", "items": {"type": "number"}},
        description="Filter by actor id (e.g. ?actors=1,2,5)",
    ),
]

play_doc_examples = [
    OpenApiExample(
        name="Filter by title",
        description="Get plays with title containing 'Hamlet'.",
        value="?title=Hamlet",
    ),
    OpenApiExample(
        name="Filter by genres",
        description="Get plays with specific genre IDs.",
        value="?genres=1,2,3",
    ),
    OpenApiExample(
        name="Filter by actors",
        description="Get plays with specific actor IDs.",
        value="?actors=1,2,3",
    ),
]

performance_doc_parameters = [
    OpenApiParameter(
        "date",
        type=OpenApiTypes.DATE,
        description="Filter by date (e.g. ?date=2024-10-08)",
    ),
    OpenApiParameter(
        "play",
        type=str,
        description="Filter by play title (e.g. ?play=macbeth)",
    ),
]

performance_doc_examples = [
    OpenApiExample(
        name="Filter by date",
        description="Get performances on a specific date.",
        value="?date=2024-10-08",
    ),
    OpenApiExample(
        name="Filter by play title",
        description="Get performances for a specific play.",
        value="?play=Macbeth",
    ),
]
