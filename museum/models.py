from django.db import models
from django.contrib.auth.models import User

class Car(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    rarity = models.CharField(max_length=50, choices=[
        ('common', 'Common'), ('uncommon', 'Uncommon'), ('rare', 'Rare'),
        ('very_rare', 'Very Rare'), ('import', 'Import'), 
        ('exotic', 'Exotic'), ('black_market', 'Black Market')
    ])
    hitbox = models.CharField(max_length=50)
    release_date = models.DateField()
    description = models.TextField()
    image = models.ImageField(upload_to='cars/', blank=True, null=True)
    price = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.name

class Arena(models.Model):
    name = models.CharField(max_length=100)
    arena_type = models.CharField(max_length=50, choices=[
        ('standard', 'Standard'), ('competitive', 'Competitive'), 
        ('special', 'Special Event')
    ])
    environment = models.CharField(max_length=100)
    capacity = models.CharField(max_length=50)
    special_features = models.TextField()
    image = models.ImageField(upload_to='arenas/', blank=True, null=True)
    
    def __str__(self):
        return self.name

class GameUpdate(models.Model):
    version = models.CharField(max_length=50)
    release_date = models.DateField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    major_changes = models.TextField()
    image = models.ImageField(upload_to='updates/', blank=True, null=True)
    
    def __str__(self):
        return f"v{self.version} - {self.title}"

class Achievement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=50, choices=[
        ('easy', 'Easy'), ('medium', 'Medium'), 
        ('hard', 'Hard'), ('expert', 'Expert')
    ])
    requirements = models.TextField()
    reward = models.CharField(max_length=100, blank=True)
    icon = models.ImageField(upload_to='achievements/', blank=True, null=True)
    
    def __str__(self):
        return self.title

class Tournament(models.Model):
    name = models.CharField(max_length=200)
    season = models.CharField(max_length=50)
    date = models.DateField()
    prize_pool = models.CharField(max_length=100)
    winner = models.CharField(max_length=100)
    runner_up = models.CharField(max_length=100)
    mvp = models.CharField(max_length=100)
    highlights = models.TextField(blank=True)
    image = models.ImageField(upload_to='tournaments/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - Season {self.season}"

class Highlight(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_url = models.URLField(help_text="YouTube или Vimeo ссылка", blank=True)
    video_file = models.FileField(
        upload_to='highlights/videos/', 
        blank=True, 
        null=True,
        help_text="Загрузите видео файл (MP4, WebM, MOV)"
    )
    thumbnail = models.ImageField(
        upload_to='highlights/thumbnails/', 
        blank=True, 
        null=True,
        help_text="Превью для видео"
    )
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='highlights_videos')
    player = models.CharField(max_length=100, help_text="Игрок или команда")
    moment_type = models.CharField(max_length=50, choices=[
        ('aerial', 'Ариал'),
        ('double_tap', 'Двойное касание'),
        ('ceiling_shot', 'Удар с потолка'),
        ('musty_flick', 'Флик Масти'),
        ('bump_play', 'Столкновение'),
        ('save', 'Сейв'),
        ('pass_play', 'Командная игра'),
        ('zero_second', 'Гол на последней секунде'),
        ('other', 'Другое')
    ])
    duration = models.CharField(max_length=20, help_text="Например: 0:15")
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.title} - {self.player}"
    
    def increment_views(self):
        self.views += 1
        self.save()
    
    def get_video_source(self):
        """Возвращает источник видео (URL или файл)"""
        if self.video_file:
            return self.video_file.url
        return self.video_url
    
    def is_uploaded_file(self):
        """Проверяет, является ли видео загруженным файлом"""
        return bool(self.video_file)

class VisitorComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    
    def __str__(self):
        return f"Comment by {self.user.username} - {self.rating}/5"