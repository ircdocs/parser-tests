from pathlib import Path

import yaml

__all__ = (
    'mask_match', 'msg_join', 'msg_split',
    'userhost_split', 'validate_hostname',
)

DATA_DIR = Path(__file__).resolve().parent / 'data'


def load_data(name):
    with (DATA_DIR / '{}.yaml'.format(name)).open(encoding='utf-8') as f:
        data = yaml.safe_load(f)

    return data


mask_match = load_data('mask-match')
msg_join = load_data('msg-join')
msg_split = load_data('msg-split')
userhost_split = load_data('userhost-split')
validate_hostname = load_data('validate-hostname')
