"""
Signals for syncing legacy M2M fields with unified relationship system.

These signals ensure backward compatibility by automatically creating/deleting
CaseEntityRelationship records when the legacy alleged_entities or related_entities
M2M fields are modified.
"""

from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Case, CaseEntityRelationship, RelationshipType


@receiver(m2m_changed, sender=Case.alleged_entities.through)
def sync_alleged_entities_to_unified(sender, instance, action, pk_set, **kwargs):
    """
    Sync alleged_entities M2M changes to CaseEntityRelationship.
    
    When entities are added/removed from case.alleged_entities, automatically
    create/delete corresponding CaseEntityRelationship records with
    relationship_type=ALLEGED.
    """
    if action == "post_add" and pk_set:
        # Create unified relationships for added entities
        for entity_id in pk_set:
            CaseEntityRelationship.objects.get_or_create(
                case=instance,
                entity_id=entity_id,
                relationship_type=RelationshipType.ALLEGED
            )
    
    elif action == "post_remove" and pk_set:
        # Delete unified relationships for removed entities
        CaseEntityRelationship.objects.filter(
            case=instance,
            entity_id__in=pk_set,
            relationship_type=RelationshipType.ALLEGED
        ).delete()
    
    elif action == "post_clear":
        # Delete all alleged relationships when cleared
        CaseEntityRelationship.objects.filter(
            case=instance,
            relationship_type=RelationshipType.ALLEGED
        ).delete()


@receiver(m2m_changed, sender=Case.related_entities.through)
def sync_related_entities_to_unified(sender, instance, action, pk_set, **kwargs):
    """
    Sync related_entities M2M changes to CaseEntityRelationship.
    
    When entities are added/removed from case.related_entities, automatically
    create/delete corresponding CaseEntityRelationship records with
    relationship_type=RELATED.
    """
    if action == "post_add" and pk_set:
        # Create unified relationships for added entities
        for entity_id in pk_set:
            CaseEntityRelationship.objects.get_or_create(
                case=instance,
                entity_id=entity_id,
                relationship_type=RelationshipType.RELATED
            )
    
    elif action == "post_remove" and pk_set:
        # Delete unified relationships for removed entities
        CaseEntityRelationship.objects.filter(
            case=instance,
            entity_id__in=pk_set,
            relationship_type=RelationshipType.RELATED
        ).delete()
    
    elif action == "post_clear":
        # Delete all related relationships when cleared
        CaseEntityRelationship.objects.filter(
            case=instance,
            relationship_type=RelationshipType.RELATED
        ).delete()
