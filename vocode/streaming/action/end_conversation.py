from typing import Type

from loguru import logger
from pydantic.v1 import BaseModel

from vocode.streaming.action.base_action import BaseAction
from vocode.streaming.models.actions import ActionConfig as VocodeActionConfig
from vocode.streaming.models.actions import ActionInput, ActionOutput

_END_CONVERSATION_ACTION_DESCRIPTION = """
Ends the current conversation. Use this action when it is clear that the caller expects the call to end, and there are no further objectives to address. Common scenarios include when the user explicitly says goodbye or uses another farewell phrase. 
Farewell phrases in English and Estonian may include: goodbye, see you, take care, so long, later, nägemist, head aega, etc. 
Note that farewell phrases may sometimes be part of a longer sentence, so listen carefully for context. For example: "This sounds great! Talk to you soon." In such cases, the conversation should also be concluded."""


class EndConversationParameters(BaseModel):
    pass


class EndConversationResponse(BaseModel):
    success: bool


class EndConversationVocodeActionConfig(
    VocodeActionConfig, type="action_end_conversation"  # type: ignore
):
    def action_attempt_to_string(self, input: ActionInput) -> str:
        assert isinstance(input.params, EndConversationParameters)
        return "Attempting to end conversation"

    def action_result_to_string(self, input: ActionInput, output: ActionOutput) -> str:
        assert isinstance(output.response, EndConversationResponse)
        if output.response.success:
            action_description = "Successfully ended conversation"
        else:
            action_description = "Did not end call because user interrupted"
        return action_description


class EndConversation(
    BaseAction[
        EndConversationVocodeActionConfig,
        EndConversationParameters,
        EndConversationResponse,
    ]
):
    description: str = _END_CONVERSATION_ACTION_DESCRIPTION
    parameters_type: Type[EndConversationParameters] = EndConversationParameters
    response_type: Type[EndConversationResponse] = EndConversationResponse

    def __init__(
        self,
        action_config: EndConversationVocodeActionConfig,
    ):
        super().__init__(
            action_config,
            quiet=True,
            should_respond="sometimes",
            is_interruptible=False,
        )

    async def _end_of_run_hook(self) -> None:
        """This method is called at the end of the run method. It is optional but intended to be
        overridden if needed."""
        pass

    async def run(
        self, action_input: ActionInput[EndConversationParameters]
    ) -> ActionOutput[EndConversationResponse]:
        if action_input.user_message_tracker is not None:
            await action_input.user_message_tracker.wait()

        if self.conversation_state_manager.transcript.was_last_message_interrupted():
            logger.info("Last bot message was interrupted")
            return ActionOutput(
                action_type=action_input.action_config.type,
                response=EndConversationResponse(success=False),
            )

        await self.conversation_state_manager.terminate_conversation()

        await self._end_of_run_hook()
        return ActionOutput(
            action_type=action_input.action_config.type,
            response=EndConversationResponse(success=True),
        )
