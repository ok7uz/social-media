from django.db import models


class CustomAutoField(models.BigAutoField):

    def get_next_value(self, *args, **kwargs):
        print(self.model.objects)
        if self.model.objects.exists():
            return self.model.objects.latest('id').id + 1
        else:
            return 10 ** 9
