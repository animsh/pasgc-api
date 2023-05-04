from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# Create your models here.


class UserAccountManager(BaseUserManager):
    def create_user(self, email, name, enrollment_number, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name,
                          enrollment_number=enrollment_number)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, enrollment_number, password):
        user = self.create_user(email, name, enrollment_number, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    enrollment_number = models.IntegerField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "enrollment_number"]

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email


class UserGradeAnalysisData(models.Model):
    user = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE)
    enrollment_number = models.IntegerField(primary_key=True)
    sex = models.CharField(max_length=255)
    age = models.IntegerField()
    address = models.CharField(max_length=1)
    family_size = models.CharField(max_length=3)
    parent_status = models.CharField(max_length=1)
    mother_education = models.IntegerField()
    father_education = models.IntegerField()
    mother_job = models.CharField(max_length=255)
    father_job = models.CharField(max_length=255)
    reason = models.CharField(max_length=255)
    guardian = models.CharField(max_length=255)
    travel_time = models.IntegerField()
    study_time = models.IntegerField()
    failures = models.IntegerField()
    school_support = models.CharField(max_length=3)
    family_support = models.CharField(max_length=3)
    extra_activities = models.CharField(max_length=3)
    nursery = models.CharField(max_length=3)
    higher = models.CharField(max_length=3)
    internet = models.CharField(max_length=3)
    family_relationship = models.IntegerField()
    free_time = models.IntegerField()
    go_out = models.IntegerField()
    health = models.IntegerField()
    absences = models.IntegerField()
    mid_sem_marks = models.IntegerField()
    end_sem_marks = models.IntegerField(blank=True, null=True)
    attendance_rate = models.IntegerField()
    class_participation = models.IntegerField()
    motivation = models.IntegerField()
    self_discipline = models.IntegerField()
    teacher_quality = models.IntegerField()
    time_management = models.IntegerField()
    peer_influence = models.IntegerField()
    parental_involvement = models.IntegerField()
    teacher_student_relationship = models.IntegerField()
    stress_level = models.IntegerField()
    mental_health = models.IntegerField()
    goal_setting = models.IntegerField()
    learning_resources = models.IntegerField()
    group_study = models.IntegerField()
    time_spent_on_homework = models.IntegerField()
    subject_interest = models.IntegerField()
    classroom_environment = models.IntegerField()
    test_preparation = models.IntegerField()
    time_spent_on_extracurricular_activities = models.IntegerField()
    workload = models.IntegerField()
    degree = models.CharField(max_length=255)
    subjects = models.CharField(max_length=255)
    subjects_codes = models.CharField(max_length=255)
    semester = models.IntegerField()

    def __str__(self):
        return self.enrollment_number


class UserCareerAnalysisData(models.Model):
    user = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE)
    enrollment_number = models.IntegerField(primary_key=True)
    logical_quotient_rating = models.IntegerField()
    hackathons = models.IntegerField()
    coding_skills_rating = models.IntegerField()
    public_speaking_points = models.IntegerField()
    self_learning_capability = models.CharField(max_length=3)
    extra_courses_did = models.CharField(max_length=3)
    certifications = models.CharField(max_length=100)
    workshops = models.CharField(max_length=100)
    reading_writing_skills = models.CharField(max_length=10)
    memory_capability_score = models.CharField(max_length=10)
    interested_subjects = models.CharField(max_length=100)
    interested_career_area = models.CharField(max_length=100)
    type_of_company_want_to_settle_in = models.CharField(max_length=100)
    taken_inputs_from_seniors_or_elders = models.CharField(max_length=3)
    interested_type_of_books = models.CharField(max_length=100)
    management_or_technical = models.CharField(max_length=10)
    hard_or_smart_worker = models.CharField(max_length=20)
    worked_in_teams_ever = models.CharField(max_length=3)
    introvert = models.CharField(max_length=3)
    suggested_job_role = models.CharField(
        max_length=100, blank=True, null=True)

    def __str__(self):
        return self.suggested_job_role
