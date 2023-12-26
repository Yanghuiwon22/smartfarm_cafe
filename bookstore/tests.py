from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import BookStore

class TestView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_post_list(self):
        #  1.1 포스트 목록 페이지를 가져온다.
        response = self.client.get('/bookstore/')

        # 1.2 정상적으로 페이지가 로드된다.
        self.assertEqual(response.status_code, 200)

        # 1.3 페이지 타이틀은 'JBNU SMARTFARM'이다
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'JBNU SMARTFARM')

        # 1.4 네이게이션 바가 있다.
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('책방', navbar.text)

        self.assertEqual(BookStore.objects.count(), 0)

        main_area = soup.find('div', id='main-area')  # 수정된 부분
        self.assertIn('아직 게시물이 없습니다', main_area.text)

        post_001 = BookStore.objects.create(  # 수정된 부분
            title='첫번째 포스트입니다.',
            content='Hello World. We are the world.'
        )

        post_002 = BookStore.objects.create(  # 수정된 부분
            title='두번째 포스트입니다.',
            content='1등이 전부는 아니잖아요?'
        )
        self.assertEqual(BookStore.objects.count(), 2)

        response = self.client.get('/bookstore/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)

        main_area = soup.find('div', id='main')  # 수정된 부분
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)
        self.assertNotIn('아직 게시물이 없습니다', main_area.text)  # 수정된 부분



