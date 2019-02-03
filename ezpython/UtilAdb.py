# -*- coding: utf-8 -*-
import commands


def adb_cmd(cmd):
    (status, result) = commands.getstatusoutput(cmd)
    return status, result, cmd


def adb_on_click_home(adb_target):
    return adb_cmd('adb -s {0} shell input keyevent 3'.format(adb_target))


def adb_push_file(adb_target, pc_file_full_path, adb_target_file_full_path):
    return adb_cmd('adb -s {0} push {1} {2}'.format(adb_target, pc_file_full_path, adb_target_file_full_path))


def adb_start_app(adb_target, package_name, activity_name):
    return adb_cmd('adb -s {0} shell am start -n {1}/{2}'.format(adb_target, package_name, activity_name))


def adb_media_scanner_scan_file(adb_target, file_path):
    '''
    adb shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///mnt/sdcard/ig_tool/20180326/dontest.jpg
    :param adb_target:
    :param file_path:
    :return:
    '''
    return adb_cmd(
        'adb -s {0} shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d {1}'.format(adb_target,
                                                                                                       file_path))


def adb_ls(adb_target, adb_target_dir):
    return adb_cmd('adb -s {0} shell ls -l {1}'.format(adb_target, adb_target_dir))


def adb_rm(adb_target, adb_target_file_path):
    return adb_cmd('adb -s {0} shell rm -rf {1}'.format(adb_target, adb_target_file_path))


def adb_wait_for_device(adb_target):
    return adb_cmd('adb -s {0} wait-for-device '.format(adb_target))


def adb_tap_back(adb_target):
    return adb_cmd('adb -s {0} shell input keyevent 4'.format(adb_target))


def adb_force_stop(adb_target, package_name):
    return adb_cmd('adb -s {0} shell am force-stop {1}'.format(adb_target, package_name))


def adb_tap(adb_target, dx, dy):
    return adb_cmd('adb -s {0} shell input tap {1} {2} '.format(adb_target, str(dx), str(dy)))


def adb_uiautomator_dump(adb_target, adb_path):
    return adb_cmd('adb -s {0} shell uiautomator dump {1}'.format(adb_target, adb_path))


def adb_swipe(adb_target, start_x, start_y, end_x, end_y, time=100):
    return adb_cmd(
        'adb -s {0} shell input swipe {1} {2} {3} {4}'.format(adb_target, start_x, start_y, end_x, end_y, time))


def adb_url(adb_target, url):
    return adb_cmd('adb -s {0} shell am start -a android.intent.action.VIEW -d {1}'.format(adb_target, url))


def adb_pull(adb_target, adb_path, pc_path):
    """
    adb shell /system/bin/screencap -p /sdcard/screenshot.png
    :param adb_target:
    :param adb_path:
    :param pc_path:
    :return:
    """
    return adb_cmd('adb -s {0} pull {1} {2}'.format(adb_target, adb_path, pc_path))


def adb_share_video_2_ig(adb_target, adb_target_file_full_path):
    cmd = 'adb -s {0} shell am start -a "android.intent.action.SEND" -t "video/*" --eu "android.intent.extra.STREAM" "{1}"'
    cmd = cmd.format(adb_target, adb_target_file_full_path)
    return adb_cmd(cmd)


def adb_share_image_2_ig(adb_target, adb_target_file_full_path):
    cmd = 'adb -s {0} shell am start -a "android.intent.action.SEND" -t "image/*" --eu "android.intent.extra.STREAM" "{1}"'
    cmd = cmd.format(adb_target, adb_target_file_full_path)
    return adb_cmd(cmd)


def adb_input_text_with(adb_target, text):
    """
    調用adbkeyboard輸入文字
    :param text:
    :param adb_target:
    :return:
    """
    return adb_cmd('adb -s {0} shell am broadcast -a ADB_INPUT_CHARS --eia chars "{1}"'.format(adb_target, text))


def adb_cap_photo(adb_target, adb_path):
    """
    adb shell /system/bin/screencap -p /sdcard/screenshot.png
    :return:
    """
    return adb_cmd('adb -s {0} shell screencap -p {1}'.format(adb_target, adb_path))
