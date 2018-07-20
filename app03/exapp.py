# from extraapp.server_model import v1
# from app03 import models
# from .views.branch import BranchAdmin
# v1.site.register(models.Branch,BranchAdmin)


from extraapp.server_model import v1
from app03 import models

v1.site.register(models.Branch)
v1.site.register(models.Course)
v1.site.register(models.ClassList)
v1.site.register(models.UserProfile)
v1.site.register(models.CourseRecord)
v1.site.register(models.Customer)
v1.site.register(models.Enrollment)
v1.site.register(models.CustomerFollowUp)
v1.site.register(models.StudyRecord)
v1.site.register(models.StuAccount)
v1.site.register(models.PaymentRecord)
