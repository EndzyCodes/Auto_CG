from .bb_utils import bb_attack_loop

def run_builder_base(is_switch_acc=False, is_2_camps=False):
    bb_attack_loop(isSwitchAcc=is_switch_acc, is_2_camps=is_2_camps)

if __name__ == '__main__':
    run_builder_base()
