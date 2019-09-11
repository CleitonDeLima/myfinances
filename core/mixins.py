class RedirectToRefererSuccessMixin:
    """
    Redireciona para a url de HTTP_REFERER
    """
    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', self.success_url)
