from abc import ABC, abstractmethod

class BaseCommand(ABC):
    """
    Abstract base class for all command classes in the Discord bot.

    This class provides a template method pattern, defining the structure of the 
    execution flow, and ensures that all concrete command classes implement the 
    core execution logic.
    """

    def __init__(self, context, *args, **kwargs):
        """
        Initialize the command with the context and any arguments needed for execution.

        Args:
            context: The context in which the command is executed, typically includes 
                     information like the user, channel, message, etc.
            *args: Positional arguments necessary for the command.
            **kwargs: Keyword arguments necessary for the command.
        """
        self.context = context
        self.args = args
        self.kwargs = kwargs

    @abstractmethod
    async def execute(self):
        """
        The core method that each command must implement, containing the logic for command execution.

        This method must be implemented by all subclasses to handle the specific actions that
        the command is responsible for.
        """
        pass

    async def run(self):
        """
        A template method that defines the skeleton of the execution flow.
        This method calls the execute method, which is defined by each subclass.

        This could also handle common pre-execution and post-execution tasks if needed,
        such as logging, error handling, etc.
        """
        try:
            await self.execute()
        except Exception as e:
            await self.handle_error(e)

    async def handle_error(self, error):
        """
        Handle any errors that occur during the execution of the command.

        Args:
            error: The exception that was raised during command execution.
        """
        # Log the error, alert the user, etc.
        # Here you can log the error to a logging service or send a message to the user.
        print(f"An error occurred: {error}")
        await self.context.respond(f"An error occurred while executing the command: {error}")
