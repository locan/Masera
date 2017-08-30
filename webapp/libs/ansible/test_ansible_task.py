# -*- coding:utf-8 -*-
import json
import shutil
from collections import namedtuple

import ansible.constants as C
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.inventory import Inventory, Host
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.plugins.callback import CallbackBase
from ansible.vars import VariableManager


class ResultCallback(CallbackBase):
    def v2_runner_on_ok(self, result, **kwargs):
        host = result._host
        print u'%s 执行结果' % result._task
        print json.dumps({host.name: result._result}, indent=4)
        print '-' * 20


host_lists = ['192.168.224.128']

variable_manager = VariableManager()

loader = DataLoader()

Options = namedtuple('Options', ['ssh_extra_args',
                                 'ssh_common_args',
                                 'connection',
                                 'module_path',
                                 'forks',
                                 'become',
                                 'become_method',
                                 'become_user',
                                 'check'])

options = Options(ssh_extra_args='', ssh_common_args='', connection='smart',
                  module_path=None, forks=5, become=None,
                  become_method=None, become_user=None, check=False)

passwords = dict(conn_pass='123456', become_pass='123456')

results_callback = ResultCallback()

inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list=host_lists)
variable_manager.set_inventory(inventory)

# 定义ansible主机
host_info = Host(name='192.168.224.128', port=22)
# 设置主机的用户名和密码
variable_manager.set_host_variable(host_info, 'ansible_ssh_user', 'root')
variable_manager.set_host_variable(host_info, 'ansible_ssh_pass', '123456')

host_pattern = '192.168.224.128'

play_source = dict(
    name='Ansible Ad-Hoc',
    hosts=host_pattern,
    gather_facts='no',
    tasks=[
        dict(action=dict(module='shell', args='whoami'), register='shell_out', async=0, poll=15),
        dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}')), async=0, poll=15)
    ]
)

play = Play().load(play_source, variable_manager=variable_manager, loader=loader)
tqm = None
try:
    tqm = TaskQueueManager(
        inventory=inventory,
        variable_manager=variable_manager,
        loader=loader,
        options=options,
        passwords=passwords,
        stdout_callback=results_callback
    )
    results = tqm.run(play)
    print '任务执行的返回码：%s' % results
finally:
    if tqm is not None:
        tqm.cleanup()
    if loader:
        loader.cleanup_all_tmp_files()
    shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)
