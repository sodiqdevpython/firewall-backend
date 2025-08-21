from django.db import models
from .choices import FirewallRuleChoices, FirewallRuleDirectionChoices, FirewallRuleActionChoices
from utils.models import BaseModel

class FirewallRule(BaseModel):
    host = models.ForeignKey('hosts.Device', on_delete=models.SET_NULL, null=True, blank=True)
    application = models.ForeignKey('applications.Application', on_delete=models.SET_NULL, null=True, blank=True)
    port = models.PositiveIntegerField(null=True, blank=True)
    protocol = models.CharField(max_length=10, choices=FirewallRuleChoices.choices)
    direction = models.CharField(max_length=10, choices=FirewallRuleDirectionChoices.choices)
    action = models.CharField(max_length=10, choices=FirewallRuleActionChoices.choices)

    def __str__(self):
        return f"{self.host}:{self.port}"

class RuleAssignment(BaseModel):
    rule = models.ForeignKey(FirewallRule, on_delete=models.CASCADE)
    host = models.ForeignKey('hosts.Device', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=FirewallRuleActionChoices.choices)

    def __str__(self):
        return f"{self.rule}:{self.host}"