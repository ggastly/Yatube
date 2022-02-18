from django.contrib.auth import get_user_model
from django.test import TestCase
from posts.models import Group, Post, Comment, Follow

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )

        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=cls.user,
            group=cls.group,
        )

    def test_post_object_name_id_title_field(self):
        post = PostModelTest.post
        expected_object_name = f"«{post.text[0:15]}...»"
        self.assertEqual(expected_object_name, str(post))

    def test_post_title_label(self):
        post = PostModelTest.post
        verbose_names = {
            'text': 'Текст поста',
            'author': 'Автор',
            'group': 'Группа',
        }
        for field, verbose_name in verbose_names.items():
            with self.subTest(field=field):
                verbose = post._meta.get_field(field).verbose_name
                self.assertEqual(verbose, verbose_name)

    def test_post_title_help_text(self):
        post = PostModelTest.post
        help_texts = {
            'text': 'Текст нового поста',
            'author': 'Автор поста',
            'group': 'Группа, к которой будет относится пост',
        }
        for field, help_text in help_texts.items():
            with self.subTest(field=field):
                verbose = post._meta.get_field(field).help_text
                self.assertEqual(verbose, help_text)


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='groupp',
            slug='kinop',
            description='Denissss'
        )

    def test_group_object_name_id_title_field(self):
        group = GroupModelTest.group
        expected_object_name = group.title
        self.assertEqual(expected_object_name, str(group))

    def test_group_title_label(self):
        group = GroupModelTest.group
        verbose_names = {
            'title': 'Группа',
            'slug': 'Адрес',
            'description': 'Описание',
        }
        for field, verbose_name in verbose_names.items():
            with self.subTest(field=field):
                verbose = group._meta.get_field(field).verbose_name
                self.assertEqual(verbose, verbose_name)

    def test_group_title_help_text(self):
        group = GroupModelTest.group
        help_texts = {
            'title': 'Группа, к которой будет относится пост',
            'slug': 'Уникальный адрес группы',
            'description': 'Описание группы',
        }
        for field, help_text in help_texts.items():
            with self.subTest(field=field):
                verbose = group._meta.get_field(field).help_text
                self.assertEqual(verbose, help_text)


class FollowModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_1 = User.objects.create_user(username='authhh')
        cls.user_2 = User.objects.create_user(username='authhhh')
        cls.group = Group.objects.create(
            title='Тестовая группаa',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            text='Тестовый постn',
            author=cls.user_2,
            group=cls.group,
        )
        cls.follow = Follow.objects.create(
            user=cls.user_1,
            author=cls.user_2,
        )

    def test_follow_object_name_id_title_field(self):
        follow = FollowModelTest.follow
        expected_object_name = (f'{follow.user.username} '
                                f'подписан на {follow.author.username}')
        self.assertEqual(expected_object_name, str(follow))

    def test_follow_title_labelfff(self):
        follow = FollowModelTest.follow
        verbose_names = {
            'user': 'Подписчик',
            'author': 'Автор',
        }
        for field, verbose_name in verbose_names.items():
            with self.subTest(field=field):
                verbose = follow._meta.get_field(field).verbose_name
                self.assertEqual(verbose, verbose_name)

    def test_follow_title_help_textfff(self):
        follow = FollowModelTest.follow

        help_texts = {
            'user': 'Подписанный пользователь',
            'author': 'Автор, на которого можно подписаться',
        }
        for field, help_text in help_texts.items():
            with self.subTest(field=field):
                verbose = follow._meta.get_field(field).help_text
                self.assertEqual(verbose, help_text)


class CommentModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='authhh')
        cls.group = Group.objects.create(
            title='Тестовая группаa',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=cls.user,
            group=cls.group,
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=cls.user,
            text='Тестовый комментарий',
        )

    def test_comment_object_name_id_title_field(self):
        comment = CommentModelTest.comment
        expected_object_name = f"«{comment.text[0:15]}...»"
        self.assertEqual(expected_object_name, str(comment))

    def test_comment_title_labelfff(self):
        comment = CommentModelTest.comment
        verbose_names = {
            'post': 'Пост',
            'author': 'Автор',
            'text': 'Комментарий',
            'created': 'Время и дата создания',
        }
        for field, verbose_name in verbose_names.items():
            with self.subTest(field=field):
                verbose = comment._meta.get_field(field).verbose_name
                self.assertEqual(verbose, verbose_name)

    def test_comment_title_help_textfff(self):
        comment = CommentModelTest.comment
        help_texts = {
            'post': 'Комментируемый пост',
            'author': 'Автор комментария',
            'text': 'Оставьте ваш комментарий здесь',
            'created': 'Время и дата, когда коммент был написан',
        }
        for field, help_text in help_texts.items():
            with self.subTest(field=field):
                verbose = comment._meta.get_field(field).help_text
                self.assertEqual(verbose, help_text)
