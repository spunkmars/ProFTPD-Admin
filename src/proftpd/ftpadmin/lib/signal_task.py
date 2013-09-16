from proftpd.ftpadmin  import  signals
from proftpd.ftpadmin.models.ftpgroups import  Ftpgroup
from proftpd.ftpadmin.models.ftpusers import Ftpuser
from proftpd.ftpadmin.models.ftpacl import Ftpacl
from proftpd.ftpadmin.lib.common import initlog
from proftpd.ftpadmin.models.ftpquotalimits import Ftpquotalimits
from proftpd.ftpadmin.models.ftpquotatallies import Ftpquotatallies

logger2 = initlog()

#--------------------------------------------------------------
def sync_modify_ftpgroup_gid_to_ftpuser(sender, **kwargs):
    logger2.info('start sync_modify_ftpgroup_gid_to_ftpuser  ')
    ftpgroup = kwargs['obj']
    Ftpuser.objects.filter(group=ftpgroup).update(uid=ftpgroup.gid, gid=ftpgroup.gid)


signals.modify_ftpgroup_gid_done.connect(sync_modify_ftpgroup_gid_to_ftpuser, sender=Ftpgroup)


def sync_modify_ftpgroup_groupname_to_ftpacl(sender, **kwargs):
    ftpgroup = kwargs['obj']
    Ftpacl.objects.filter(groupname_id=ftpgroup.id).update(groupname = ftpgroup.groupname)

signals.modify_ftpgroup_groupname_done.connect(sync_modify_ftpgroup_groupname_to_ftpacl, sender=Ftpgroup)


def del_relate_ftpacl_from_ftpgroup(sender, **kwargs):
    ftpgroup = kwargs['obj']
    Ftpacl.objects.filter(groupname_id=ftpgroup.id).delete()
    tmp_user_id_list = [  s_item[0] for s_item in Ftpuser.objects.filter(group=ftpgroup).values_list('id') ]
    for tmp_user_id in tmp_user_id_list:
        Ftpacl.objects.filter(username_id=tmp_user_id).delete()

signals.delete_ftpgroup_done.connect(del_relate_ftpacl_from_ftpgroup, sender=Ftpgroup)


#--------------------------------------------------------------
def  init_ftpquotatallies(sender, **kwargs):
    logger2.info('start init_ftpquotatallies')
    ftpquotalimits = kwargs['obj']
    logger2.info(ftpquotalimits.username_id.username)
    logger2.info(ftpquotalimits.username_id.uid)
    logger2.info(ftpquotalimits.username_id.shell)
    logger2.info(ftpquotalimits.username)
    logger2.info(ftpquotalimits.quota_type)

    ftpquotatallies = Ftpquotatallies(
                        username = ftpquotalimits.username,
                        quota_type = ftpquotalimits.quota_type,
                        bytes_in_used = 0,
                        bytes_out_used = 0,
                        bytes_xfer_used = 0,
                        files_in_used = 0,
                        files_out_used = 0,
                        files_xfer_used = 0,
                        username_id = ftpquotalimits.username_id
    )
    ftpquotatallies.save()
    return ftpquotatallies

signals.create_ftpquotalimits_done.connect(init_ftpquotatallies, sender=Ftpquotalimits)





def sync_ftpquotalimits_quotatype_to_ftpquotatallies(sender, **kwargs):
    logger2.info('start sync_ftpquotalimits_quotatype_to_ftpquotatallies')
    ftpquotalimits = kwargs['obj']
    ftpquotatallies = Ftpquotatallies.objects.get(username_id = ftpquotalimits.username_id)
    ftpquotatallies.quota_type = ftpquotalimits.quota_type
    ftpquotatallies.save()
    return ftpquotatallies

signals.modify_ftpquotalimits_quotatype_done.connect(sync_ftpquotalimits_quotatype_to_ftpquotatallies, sender=Ftpquotalimits)




def del_relate_ftpquotatallies(sender, **kwargs):
    logger2.info('start  del_relate_ftpquotatallies')
    ftpquotalimits = kwargs['obj']
    Ftpquotatallies.objects.filter(username_id = ftpquotalimits.username_id).delete()


signals.delete_ftpquotalimits_done.connect(del_relate_ftpquotatallies, sender=Ftpquotalimits)


#--------------------------------------------------------------


def sync_ftpquotalimits_and_ftpquotatallies_ftpacl_username(sender, **kwargs):
    logger2.info('start sync_ftpquotalimits_and_ftpquotatallies_username')
    ftpuser = kwargs['obj']
    Ftpquotalimits.objects.filter(username_id=ftpuser).update(username = ftpuser.username)
    Ftpquotatallies.objects.filter(username_id=ftpuser).update(username = ftpuser.username)
    Ftpacl.objects.filter(username_id=ftpuser.id).update(username = ftpuser.username)



signals.modify_ftpuser_username_done.connect(sync_ftpquotalimits_and_ftpquotatallies_ftpacl_username, sender=Ftpuser)



def del_relate_ftpacl_from_ftpuser(sender, **kwargs):
    ftpuser = kwargs['obj']
    Ftpacl.objects.filter(username_id=ftpuser.id).delete()

signals.delete_ftpuser_done.connect(del_relate_ftpacl_from_ftpuser, sender=Ftpuser)