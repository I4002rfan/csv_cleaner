from django.db import models

LEVEL_CHOICES = [
    ('beginner', 'Beginner'),
    ('intermediate', 'Intermediate'),
    ('advanced', 'Advanced'),
]

EXAM_TYPE_CHOICES = [
    ('midterm', 'Midterm'),
    ('endterm', 'Endterm'),
    ('practice', 'Practice'),
]

class Course(models.Model):
    course_name = models.CharField(max_length=500)
    course_level = models.CharField(choices=LEVEL_CHOICES, max_length=20)
    syllabus = models.JSONField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.course_name

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    module_name = models.CharField(max_length=500)
    order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.module_name

class Problem(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    module_tags = models.JSONField()
    subtopic_tags = models.JSONField(null=True, blank=True)
    lecture_tags = models.JSONField(null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=10000)
    problem_level = models.CharField(choices=LEVEL_CHOICES, max_length=20)  
    exam_type = models.CharField(choices=EXAM_TYPE_CHOICES, max_length=20, null=True, blank=True)

    def __str__(self):
        return self.title
