from fabric.api import run, sudo
from cloudify import ctx


def _apt_install(packages=[]):
    command = 'yum install -y {}'.format(' '.join(packages))
    _sudo(command)


def _sudo(command):
    ctx.logger.debug('Running command as root: "{}"'.format(command))
    sudo(command)


def _run(command):
    ctx.logger.debug('Running command: "{}"'.format(command))
    run(command)


def install():
    ctx.logger.info(
        'Installation of required dependencies for SNMPProxyCollector started'
    )

    ctx.logger.info('Installing system packages using apt ...')
    _apt_install(['gcc', 'python-devel'])

    ctx.logger.info('Installing pip ...')
    _sudo('curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py')
    _sudo('python get-pip.py')

    ctx.logger.info('Installing pysnmp ...')
    agent_path = '/home/centos/{}'.format(ctx.instance.id)
    virtualenv_path = '{}/env'.format(agent_path)
    ctx.logger.info(
        'Pysnmp will be installed in location: {}'.format(virtualenv_path)
    )
    _run('pip install pysnmp --prefix {}'.format(virtualenv_path))

    ctx.logger.info('Executing post-installation operations')
    _run(
        'mv {0}/lib64/python2.7/site-packages/* '
        '{0}/lib/python2.7/site-packages/'
        .format(virtualenv_path)
    )
    _run(
        'rm -rf {}/lib64/'
        .format(virtualenv_path)
    )
    _sudo('chmod 777 -R {}'.format(agent_path))

    ctx.logger.info(
        'Installation of required dependencies for SNMPProxyCollector finished'
    )