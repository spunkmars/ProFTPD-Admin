from proftpd.ftpadmin.views.common import initlog
from  celery.task import Task, PeriodicTask
from datetime import date, timedelta
from celery.schedules import crontab, crontab_parser


logger = initlog
class task_test1(Task):
    def run(self, **kwargs):
        #logger.info("Runing task_test1 !")
        print("I am task_test1")
        return True


class task_test2(PeriodicTask):
    run_every = timedelta(seconds=10)
    def run(self, **kwargs):
        #logger.info("Ruing task_test2 !")
        print("I am task_test2, I will run every 10 seconds")
        return True

class EveryMinutePeriodic(PeriodicTask):
    run_every = crontab()
    def run(self, **kwargs):
        print("I will run every minute")
        return True

class QuarterlyPeriodic(PeriodicTask):
    run_every = crontab(minute="*/15")
    def run(self, **kwargs):
        print("I will run every 15 minutes")
        return True

class HourlyPeriodic(PeriodicTask):
    run_every = crontab(minute=30)
    def run(self,**kwargs):
        print("I will run at 30 minutes every hour")
        return True

class DailyPeriodic(PeriodicTask):
    run_every = crontab(hour=7, minute=30)
    def run(self, **kwargs):
        print("I will run at 7:30 every day")
        return True


class WeeklyPeriodic(PeriodicTask):
    run_every = crontab(hour=7, minute=30, day_of_week="thursday")
    def run(self, **kwargs):
        print("I will run at 7:30 every thursday")
        return True


