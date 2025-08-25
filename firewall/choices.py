from django.db.models import TextChoices


class FirewallRuleChoices(TextChoices):
    TCP = 'TCP'
    UDP = 'UDP'
    ANY = 'ANY'


class FirewallRuleDirectionChoices(TextChoices):
    IN = 'IN', 'Inbound'
    OUT = 'OUT', 'Outbound'
    BOTH = 'BOTH', 'Both'


class FirewallRuleActionChoices(TextChoices):
    ALLOW = 'ALLOW'
    BLOCK = 'BLOCK'
