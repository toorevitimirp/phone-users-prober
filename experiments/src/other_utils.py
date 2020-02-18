import os


def beep():
    """
    在程序结束时发出提示声
    :return:
    """
    duration = 1  # second
    freq = 440  # Hz
    os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (duration, freq))
