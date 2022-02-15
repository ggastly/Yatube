from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post, Comment

User = get_user_model()


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='authh')
        cls.group = Group.objects.create(
            title='Test_group',
            slug='test-slug',
            description='Тестовое описание',
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(PostCreateFormTests.user)

    def test_create_post(self):
        tasks_count = Post.objects.count()
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {
            'text': 'Тестовый пост',
            'group': PostCreateFormTests.group.id,
            'image': uploaded,
        }
        self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), tasks_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text='Тестовый пост',
                author=PostCreateFormTests.user,
                group=PostCreateFormTests.group.id
            ).exists()
        )

    def test_post_edit_form(self):
        post = Post.objects.create(
            text='Тесттовый пост',
            author=PostCreateFormTests.user,
            group=PostCreateFormTests.group,
        )
        form_data = {
            'text': 'Измененный текст',
            'group': PostCreateFormTests.group.id,
        }
        self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': post.id}),
            data=form_data,
            follow=True
        )
        post.refresh_from_db()
        self.assertTrue(
            Post.objects.filter(
                text='Измененный текст',
                author=PostCreateFormTests.user,
                group=PostCreateFormTests.group.id
            ).exists()
        )


class CommentsCreateTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='authh')
        cls.group = Group.objects.create(
            title='Test_group',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=cls.user,
            group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(CommentsCreateTest.user)

    def test_only_authorized_client_can_comment(self):
        post = CommentsCreateTest.post
        comments_count = Comment.objects.count()
        form_data = {
            'text': 'Тестовый комментарий',
        }
        self.authorized_client.post(
            reverse('posts:add_comment', kwargs={'post_id': post.id}),
            data=form_data,
            follow=True
        )
        self.assertEqual(Comment.objects.count(), comments_count + 1)
        self.assertTrue(
            Comment.objects.filter(
                text='Тестовый комментарий',
                author=CommentsCreateTest.user,
                post=CommentsCreateTest.post
            ).exists()
        )
