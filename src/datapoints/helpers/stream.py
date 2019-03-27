class Stream():
    @staticmethod
    def take(generator, n):
        items = []
        for item in generator:
            items.append(item)
            if len(items) == n:
                yield items
                items = []
        yield items
