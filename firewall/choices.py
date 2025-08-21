from django.db.models import TextChoices

class FirewallRuleChoices(TextChoices):
    TCP = 'TCP'
    UDP = 'UDP'
    ANY = 'ANY'

class FirewallRuleDirectionChoices(TextChoices):
    INBOUND = 'INBOUND'
    OUTBOUND = 'OUTBOUND'
    BOTH = 'BOTH'

class FirewallRuleActionChoices(TextChoices):
    ALLOW = 'ALLOW'
    BLOCK = 'BLOCK'

class FirewallRuleAssignmentChoices(TextChoices):
    APPLIED = 'APPLIED'
    FAILED = 'FAILED'
    PENDING = 'PENDING'