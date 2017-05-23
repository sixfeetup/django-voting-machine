from django.apps import AppConfig


class VotingmachineConfig(AppConfig):
    name = 'voting.votingmachine'
    verbose_name = "Votingmachine"

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
