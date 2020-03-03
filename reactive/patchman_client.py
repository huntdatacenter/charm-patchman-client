#!/usr/bin/env python

from charmhelpers.contrib.ansible import apply_playbook
from charmhelpers.core.hookenv import status_set
from charms.reactive.decorators import hook
from charms.reactive.decorators import when
from charms.reactive.decorators import when_not
from charms.reactive.flags import clear_flag
from charms.reactive.flags import register_trigger
from charms.reactive.flags import set_flag

register_trigger(when='config.changed',
                 clear_flag='patchman.client.configured')


@when_not('patchman.available')
@when_not('patchman.client.configured')
def wait_on_patchman():
    status_set('blocked', 'missing patchman relation')


@when('patchman.available')
@when_not('patchman.client.configured')
def configure_plugin():
    status_set('maintenance', 'configuring patchman client')
    apply_playbook(playbook='ansible/playbook.yaml')
    status_set('active', 'ready')
    set_flag('patchman.client.configured')


# Hooks
@hook('stop')
def cleanup():
    apply_playbook(playbook='ansible/playbook.yaml', tags=['uninstall'])


@hook('upgrade-charm')
def upgrade_charm():
    clear_flag('patchman.client.configured')
