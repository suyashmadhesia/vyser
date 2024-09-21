class RuleFactory:

    _instance = None
    _rule_contexts = {}

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(RuleFactory, cls).__new__(cls)
        return cls._instance

    @classmethod
    def register_rule_context(cls, rule_context):
        if rule_context._rule_name in cls._rule_contexts:
            raise Exception(
                f"rule with name {rule_context._rule_name} already registered"
            )
        cls._rule_contexts[rule_context._rule_name] = rule_context

    @classmethod
    def get_rule_context(cls, rule_name):
        if rule_name in cls._rule_contexts:
            return cls._rule_contexts[rule_name]
        return None
