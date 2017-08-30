# -*- coding:utf-8 -*-
import json
from collections import namedtuple

from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.inventory import Inventory
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.plugins.callback import CallbackBase
from ansible.vars import VariableManager


# 自定义 callback，即在运行 api 后调用本类中的 v2_runner_on_ok()，在这里会输出 host 和 result 格式
class ResultCallback(CallbackBase):
    def v2_runner_on_ok(self, result, **kwargs):
        # result 包含 '_check_key', '_host', '_result', '_task', '_task_fields', 'is_changed', 'is_failed', 'is_skipped', 'is_unreachable', 'task_name'
        host = result._host
        print u"%s 执行结果" % result._task
        print json.dumps({host.name: result._result}, indent=4)
        print "-----------------------------------------------"


# 初始话需要的类
variable_manager = VariableManager()
# 用来管理变量，包括主机、组、扩展等变量，该类在之前的Inventory内置

loader = DataLoader()
# 用来加载解析yaml文件或JSON内容,并且支持vault的解密

# 定义选项
Options = namedtuple('Options',
                     ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check'])

# 定义连接远端的额方式为smart
options = Options(connection='smart', module_path=None, forks=100, become=None, become_method=None, become_user=None,
                  check=False)

# 定义默认的密码连接，主机未定义密码的时候才生效，conn_pass指连接远端的密码，become_pass指提升权限的密码
passwords = dict(conn_pass='123456', become_pass='123456')

# Instantiate our ResultCallback for handling results as they come in
# 结果回调类实例化
results_callback = ResultCallback()

# create inventory and pass to var manager
# 创建inventory、并带进去参数
inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list=['192.168.224.128']) #host_list='/home/luan/ansible_hosts')
# hosts文件，也可以是 ip列表 '10.1.162.18:322, 10.1.167.36' 或者 ['10.1.162.18:322', '10.1.167.36']，
# 如果不设置，默认取ansible.cfg配置文件中的inventory值，默认为/etc/ansible/hosts.
print inventory.get_hosts()
variable_manager.set_inventory(inventory)
# 把inventory传递给variable_manager管理

# create play with tasks
# 创建要执行play的内容并引入上面的变量
play_source = dict(
    name="Ansible Play",
    hosts='RHELBased',  # 匹配host_list中的主机的正则表达式
    gather_facts='no',
    # 定义任务列表
    tasks=[
        dict(action=dict(module='shell', args='hostname'), register='shell_out', async=0, poll=15),
        dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}')), async=0, poll=15)
    ]
)

play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

# actually run it
# TaskQueueManager 是创建进程池，负责输出结果和多进程间数据结构或者队列的共享协作
tqm = None
try:
    tqm = TaskQueueManager(
        inventory=inventory,
        variable_manager=variable_manager,
        loader=loader,
        options=options,
        passwords=passwords,
        stdout_callback=results_callback,  # Use our custom callback instead of the ``default`` callback plugin
        # 如果注释掉 callback 则会调用原生的 DEFAULT_STDOUT_CALLBACK，输出 task result的output，同 ansible-playbook debug
    )
    result = tqm.run(play)
    print u'任务执行返回码: %s' % result  # 返回码，只要有一个 host 出错就会返回 非0 数字
finally:
    if tqm is not None:
        tqm.cleanup()
    if loader:
        print 'end'
        loader.cleanup_all_tmp_files()
   # shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)
