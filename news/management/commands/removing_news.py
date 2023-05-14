from django.core.management.base import BaseCommand, CommandError

from news.models import Post


class Command(BaseCommand):
    help = 'Удаление всех новостей'
    requires_migrations_checks = True

    def handle(self, *args, **options):
        self.stdout.readable()
        self.stdout.write('Вы действительно хотите удалить все новости? yes/no')
        answer = input()
        if answer =='yes':
            Post.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Все новости удалены успешно!'))
            return
        self.stdout.write(self.style.ERROR('В доступе отказано!'))
