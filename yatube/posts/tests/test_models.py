from django.contrib.auth import get_user_model
from django.test import TestCase
from posts.models import Group, Post

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
