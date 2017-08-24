from django.shortcuts import get_object_or_404
from django.utils import timezone

from models import Action, Badge
from ..notifications.models import Notification


def level_up(account, exp):
	level_up_exp = 100
	account.exp += exp
	if account.exp > level_up_exp:
		account.level += 1
		account.exp = 0
	notification = Notification(receiver_id=account.id)
	notification.content = 'You have reached Level %d!' % account.level
	notification.save()
	account.save()


def trigger_action(account, action_name):
	action = get_object_or_404(Action.objects.all(), name=action_name)

	linked_badge_types = action.linked_badge_types
	account_badges = account.badges.filter(finished=None)
	account_badge_types = []

	for account_badge in account_badges:
		# save account badge types for later
		account_badge_types.append(account_badge.badge_type.name)
		# add counter to all linked badges
		if account_badge.badge_type in linked_badge_types:
			account_badge.counter += 1
			# Finish badge
			if account_badge.counter == account_badge.badge_type.action_required:
				account_badge.finished = timezone.now()
				# Send notification
				notification = Notification(receiver_id=account.id)
				notification.content = 'You have achieved a new badge --- ' + account_badge.badge_type.name + '!'
				notification.save()

			account_badge.save()

	# New badge
	for linked_badge_type in linked_badge_types:
		if linked_badge_type.name not in account_badge_types:
			new_ongoing_badge = Badge(account_id=account.id, badge_type=linked_badge_type)
			new_ongoing_badge.save()

	level_up(account, action.exp)
