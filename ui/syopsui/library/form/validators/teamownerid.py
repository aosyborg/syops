class TeamOwnerId(object):
    def is_valid(self, element, request):
        # Default to the current user if not set
        if not element.value:
            element.value = int(request.session['user'].id)

        return isinstance(element.value, int) and element.value > 0
