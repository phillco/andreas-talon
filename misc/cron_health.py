from talon import actions, cron
import time

window_size = 60
interval = 16
ts = time.perf_counter()
ts_summary = ts
deviation_count = 0
deviation_sum = 0


def on_interval():
    global ts, ts_summary, deviation_count, deviation_sum
    ts2 = time.perf_counter()
    delta = abs(interval - (ts2 - ts) * 1000)
    ts = ts2
    if delta >= 1:
        deviation_count += 1
        deviation_sum += delta
    if ts2 >= ts_summary + window_size:
        actions.user.persist_append(
            "cron_deviation",
            {
                "window_size": window_size,
                "count": deviation_count,
                "sum": deviation_sum,
            },
        )
        # print(
        #     f"Deviation count: {deviation_count}, sum: {round(deviation_sum)}, avg: {round(deviation_sum/deviation_count, 1)}"
        # )
        ts_summary = ts2
        deviation_count = 0
        deviation_sum = 0


"""
    60s

    Sleep mode: no tobii, no parrot
        Deviation count: 35, sum: 54, avg: 1.6

    Command mode: no tobii, no parrot
        Deviation count: 27, sum: 62, avg: 2.3

    Command mode: +tobii
        Deviation count: 31, sum: 50, avg: 1.6
        Deviation count: 52, sum: 190, avg: 3.6

    Command mode: +parrot
        Deviation count: 56, sum: 114, avg: 2.0
        Deviation count: 43, sum: 88, avg: 2.1

    Command mode: +tobii, +parrot
        Deviation count: 63, sum: 167, avg: 2.7
"""

"""
    5min

    Command mode: +tobii
        Deviation count: 655, sum: 2331, avg: 3.6
        Deviation count: 564, sum: 1644, avg: 2.9
        Deviation count: 597, sum: 1499, avg: 2.5

    Command mode: +tobii, +parrot
        Deviation count: 703, sum: 2729, avg: 3.9
        Deviation count: 304, sum: 722, avg: 2.4
        Deviation count: 839, sum: 3539, avg: 4.2

"""


cron.interval(f"{interval}ms", on_interval)
