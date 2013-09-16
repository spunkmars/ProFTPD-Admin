from django.contrib import admin
from proftpd.ftpadmin.models.ftpusers import Ftpuser
from proftpd.ftpadmin.models.ftpgroups import Ftpgroup
from proftpd.ftpadmin.models.ftpxferstat import Ftpxferstat
from proftpd.ftpadmin.models.ftpquotatallies import Ftpquotatallies
from proftpd.ftpadmin.models.ftpquotalimits import Ftpquotalimits
from proftpd.ftpadmin.models.ftpacl import Ftpacl


admin.site.register(Ftpuser)
admin.site.register(Ftpgroup)
admin.site.register(Ftpxferstat)
admin.site.register(Ftpquotatallies)
admin.site.register(Ftpquotalimits)
admin.site.register(Ftpacl)
