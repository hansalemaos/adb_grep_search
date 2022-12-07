import os
import subprocess
from typing import Union

from subprocess_print_and_capture import (
    execute_subprocess_multiple_commands_with_timeout_bin,
)
import pandas as pd
from get_the_hell_out_of_here import remove_control_characters_from_binary


def isroot(adb_path, deviceserial, exit_keys="ctrl+x", timeout=None):
    # from https://github.com/wuseman/adb-cheatsheet

    roa = execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=[
            f"""which su -- &> /dev/null
    if [[ $? = "0" ]]; then
        echo "True"
    else
        echo "False"
    fi"""
        ],
        exit_keys=exit_keys,
        print_output=False,
        timeout=timeout,
    )
    isrooted = False
    if roa[0].decode("utf-8", "ignore").strip() == "True":
        isrooted = True

    return isrooted


def execute_multicommands_adb_shell(
    adb_path,
    device_serial,
    subcommands: list,
    exit_keys: str = "ctrl+x",
    print_output=True,
    timeout=None,
):
    if not isinstance(subcommands, list):
        subcommands = [subcommands]

    return execute_subprocess_multiple_commands_with_timeout_bin(
        cmd=f"{adb_path} -s {device_serial} shell",
        subcommands=subcommands,
        exit_keys=exit_keys,
        end_of_printline="",
        print_output=print_output,
        timeout=timeout,
    )


def connect_to_adb(adb_path, deviceserial):
    _ = subprocess.run(f"{adb_path} start-server", capture_output=True, shell=False)
    _ = subprocess.run(
        f"{adb_path} connect {deviceserial}", capture_output=True, shell=False
    )


def adb_grep(
    adb_path: str,
    deviceserial: str,
    folder_to_search: str,
    filetype: str,
    regular_expression: str,
    exit_keys: str = "ctrl+x",
    timeout: Union[float, int, None] = None,
    remove_control_characters: bool = True,
    has_root_access=False,
) -> pd.DataFrame:
    executecommand = [
        f"""cd {folder_to_search} && find . -name "{filetype}" -exec grep -Hbna "{regular_expression}" {{}} +"""
    ]
    if has_root_access:
        executecommand = [
            f"""cd {folder_to_search} && su -c 'find . -name "{filetype}" -exec grep -Hbna "{regular_expression}" {{}} +'"""
        ]

    xx = execute_multicommands_adb_shell(
        adb_path,
        deviceserial,
        subcommands=executecommand,
        exit_keys=exit_keys,
        print_output=False,
        timeout=timeout,
    )
    df = pd.DataFrame(xx)
    try:
        if remove_control_characters:
            df[0] = df[0].apply(
                lambda x: remove_control_characters_from_binary(x, b" ")
            )
        df = (
            df[0]
            .apply(lambda x: x.decode("utf-8", "replace"))
            .str.split(":", n=3, expand=True)
        )
        df[0] = df[0].apply(
            lambda x: os.path.join(folder_to_search, x.lstrip(" ./")).replace("\\", "/")
        )
        df.columns = ["aa_file", "aa_line", "aa_byte", "aa_result"]
        df["aa_regex"] = regular_expression
        try:
            df.aa_regex = df.aa_regex.astype("category")
        except Exception:
            pass
        try:
            df.aa_file = df.aa_file.astype("category")
        except Exception:
            pass
        try:
            df.aa_line = df.aa_line.astype("Int64")
        except Exception:
            pass
        try:
            df.aa_byte = df.aa_byte.astype("Int64")
        except Exception:
            pass
        try:
            df.aa_result = df.aa_result.astype("category")
        except Exception:
            pass

        return df
    except KeyError:
        return pd.DataFrame(
            columns=["aa_file", "aa_line", "aa_byte", "aa_result", "aa_regex"]
        )


class ADBGrep:
    def __init__(self, adb_path, deviceserial):
        self.adb_path = adb_path
        self.deviceserial = deviceserial
        self.root = False

    def activate_root_grep(self):
        self.root = isroot(self.adb_path, self.deviceserial)
        return self

    def connect_to_adb(self):
        connect_to_adb(self.adb_path, self.deviceserial)
        return self

    def grep(
        self,
        folder_to_search: str,
        filetype: str,
        regular_expression: str,
        exit_keys: str = "ctrl+x",
        timeout: Union[float, int, None] = None,
        remove_control_characters: bool = True,
    ) -> pd.DataFrame:
        return adb_grep(
            adb_path=self.adb_path,
            deviceserial=self.deviceserial,
            folder_to_search=folder_to_search,
            filetype=filetype,
            regular_expression=regular_expression,
            exit_keys=exit_keys,
            timeout=timeout,
            remove_control_characters=remove_control_characters,
            has_root_access=self.root,
        )
