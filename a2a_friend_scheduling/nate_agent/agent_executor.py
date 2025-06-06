from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.types import (
    InternalError,
    InvalidParamsError,
    Part,
    TextPart,
    UnsupportedOperationError,
)
from a2a.utils import (
    completed_task,
    new_artifact,
)
from a2a.utils.errors import ServerError

from .agent import SchedulingAgent


class SchedulingAgentExecutor(AgentExecutor):
    """AgentExecutor for the scheduling agent."""

    def __init__(self):
        """Initializes the SchedulingAgentExecutor."""
        self.agent = SchedulingAgent()

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Executes the scheduling agent."""
        if self._validate_request(context):
            raise ServerError(error=InvalidParamsError())

        query = context.get_user_input()
        try:
            result = self.agent.invoke(query)
            print(f"Final Result ===> {result}")
        except Exception as e:
            print(f"Error invoking agent: {e}")
            raise ServerError(error=InternalError()) from e

        if not context.task_id or not context.context_id or not context.message:
            raise ServerError(error=InvalidParamsError())

        parts = [Part(root=TextPart(text=result))]

        event_queue.enqueue_event(
            completed_task(
                context.task_id,
                context.context_id,
                [new_artifact(parts, f"availability_response_{context.task_id}")],
                [context.message],
            )
        )

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Handles task cancellation."""
        raise ServerError(error=UnsupportedOperationError())

    def _validate_request(self, context: RequestContext) -> bool:
        """Validates the request context."""
        return False
