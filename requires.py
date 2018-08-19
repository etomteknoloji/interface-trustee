#!/usr/bin/python
# Copyright 2018 Cloudbase Solutions SRL

from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes


class TrusteeRequires(RelationBase):
    scope = scopes.GLOBAL

    # These remote data fields will be automatically mapped to accessors
    # with a basic documentation string provided.

    auto_accessors = [
        'domain_name', 'domain_admin_name', 'domain_admin_password']

    @hook('{requires:trustee}-relation-joined')
    def joined(self):
        self.set_state('{relation_name}.connected')
        self.update_state()

    def update_state(self):
        if self.base_data_complete():
            self.remove_state('{relation_name}.departed')
            self.set_state('{relation_name}.available')
        else:
            self.remove_state('{relation_name}.available')

    @hook('{requires:trustee}-relation-changed')
    def changed(self):
        self.update_state()

    @hook('{requires:trustee}-relation-{broken,departed}')
    def departed(self):
        self.remove_state('{relation_name}.available')
        self.set_state('{relation_name}.departed')

    def base_data_complete(self):
        data = {
            "domain_name": self.domain_name(),
            "domain_admin_password": self.domain_admin_password(),
            "domain_admin_name": self.domain_admin_name(),
        }
        return all(data.values())

    def request_domain(self, domain_name, admin_user):
        relation_info = {
            'domain': domain_name,
            'username': admin_user,
        }
        self.set_local(**relation_info)
        self.set_remote(**relation_info)
