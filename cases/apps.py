from django.apps import AppConfig


class CasesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cases"

    def ready(self):
        """Import signals and register models with auditlog when app is ready."""
        # Import signals to register them
        import cases.signals  # noqa: F401

        # Register models with auditlog
        from auditlog.registry import auditlog
        from cases.models import Case, DocumentSource, JawafEntity

        auditlog.register(Case)
        auditlog.register(DocumentSource)
        auditlog.register(JawafEntity)
