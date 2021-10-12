import json
import subprocess
from datetime import datetime
from pathlib import Path

SCANPATH = Path(__file__).parent.joinpath('scan')
SCANPATH.mkdir(exist_ok=True)


def get_sys_info():
    ps_info = parse_ps_info(exec_ps())
    save_info(ps_info)
    return ps_info


def exec_ps() -> str:
    return subprocess.run(['ps', 'aux'], capture_output=True, text=True).stdout


def parse_ps_info(info: str) -> dict:
    lines = info.split('\n')[1:-1]
    return {
        'users': list({line.split()[0] for line in lines}),
        'process_count': len(lines),
        'users_process_count': [{user: len([line for line in lines if line.split()[0] == user])} for user in list({line.split()[0] for line in lines})],
        'total_memory': f'{round(sum([float(line.split()[4]) + float(line.split()[5]) for line in lines]) / 1024, 1)} Mb',
        'total_cpu': f'{round(sum([float(line.split()[2]) for line in lines]), 1)} %',
        'most_memory_process_name': sorted(lines, key=lambda x: float(x.split()[3]))[-1].split()[10][:20],
        'most_cpu_process_name': sorted(lines, key=lambda x: float(x.split()[2]))[-1].split()[10][:20]
    }


def save_info(info):
    scan_file = SCANPATH.joinpath(str(datetime.now()).split('.')[0] + '-scan.txt')
    with scan_file.open('w') as f:
        json.dump(info, f, indent=4)


get_sys_info()
