from django.db import models

class oauth(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    nickname = models.CharField(max_length=50)
    reg_date = models.DateField()

    def __str__(self):
        return "id=" + self.id + "nickname" + self.nickname + "reg_date"
