def generate_id_for(model) -> int:
    return 10 ** 9 + 1 if not model.objects.exists() else model.objects.latest('id').id + 1

