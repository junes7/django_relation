from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.pk}번째 글, {self.title}-{self.content}'

class Comment(models.Model):
    # CASCADE속성은 게시글이 삭제되면 댓글도 같이 삭제된다.
    # 멤버 변수 = models.외래키(참조하는 객체, 삭제 되었을 때 처리 방법)
    # n:n 관계일 때 역 참조값 설정인 related_name='comments'를 사용한다.
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE
        )
    content = models.CharField(max_length=200)
    # 생성 된 시간 저장 옵션
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Article:{self.article}, {self.pk}-{self.content}'