import inspect
import sys
# from datetime import timedelta
#
# from bubbles.commands.periodic.test_command import test_periodic_callback
# from bubbles.tl_utils import TLJob
#
#
# class PeriodicCheck(TLJob):
#     def job(self):
#         test_periodic_callback()
#
#     class Meta:
#         start_interval = timedelta(seconds=1)
#         regular_interval = timedelta(seconds=4)


def enable_tl_jobs() -> None:
    """Find and load all job classes in this file."""
    all_jobs = [
        i[1]
        for i in inspect.getmembers(sys.modules[__name__])
        if inspect.isclass(i[1]) and hasattr(i[1], "Meta") and i[0] != "TLJob"
    ]

    print(f"Enabling {len(all_jobs)} periodic jobs.")

    for job in all_jobs:
        job()
