from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Группа',
        help_text='Группа, к которой будет относится пост',
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        db_index=True,
        verbose_name='Адрес',
        help_text='Уникальный адрес группы',
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Описание группы',
        max_length=255
    )

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        verbose_name='Текст поста',
        help_text='Текст нового поста'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время и дата создания',
        help_text='Время и дата, когда пост был написан'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
        help_text='Автор поста',
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группа',
        help_text='Группа, к которой будет относится пост'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True,
    )

    class Meta:
        ordering = ('-pk', )
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return f"«{self.text[0:15]}...»"


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост',
        help_text='Комментируемый пост'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
        help_text='Автор комментария',
    )
    text = models.TextField(
        verbose_name='Комментарий',
        help_text='Оставьте ваш комментарий здесь'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время и дата создания',
        help_text='Время и дата, когда коммент был написан'
    )

    def __str__(self):
        return f"«{self.text[0:15]}...»"


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
        help_text='Подписанный пользователь'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
        help_text='Автор, на которого можно подписаться'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='user_is_author',
            )
        )

    def __str__(self):
        return f"{self.user.username} подписан на {self.author.username}"
