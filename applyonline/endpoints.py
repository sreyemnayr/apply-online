from drf_auto_endpoint.router import router

import applyonline.models as models
from address.models import Address

router.register(models.Application)
router.register(models.Student)
router.register(models.Family)
router.register(models.Evaluation)
router.register(models.OtherSchool)
router.register(models.Parent)
router.register(models.SchoolYear)
router.register(models.Sibling)
router.register(Address)
