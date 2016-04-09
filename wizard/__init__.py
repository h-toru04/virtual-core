# -*- coding: utf-8 -*-
'''
.. module:: wizard
   :synopsis: A Web based wizard to setup the core
   :noindex:
   :copyright: Copyright 2016 by Tiago Antao
   :license: GNU Affero, see LICENSE for details

.. moduleauthor:: Tiago Antao <tra@popgen.net>

'''
from collections import defaultdict
import glob

import yaml

__version__ = '0.0.1+'

descriptive_names = {}
dependencies = defaultdict(list)  # container dependencies extracted from links
role_containers = defaultdict(list)

def get_server_dependencies():
    main_roles = glob.glob('ansible/roles/**/tasks/main.yml')
    print(main_roles)
    for main_role in main_roles:
        role = main_role.split('/')[2]
        with open(main_role) as f:
            doc = yaml.load(f)
            for entry in doc:
                if 'docker' in entry:
                    descriptive_name = entry['name']
                    name = entry['docker']['name']
                    role_containers[role].append(name)
                    descriptive_names[name] = descriptive_name
                    if 'links' in entry['docker']:
                        for link in entry['docker']['links']:
                            docker_name, internal_name = tuple(link.split(':'))
                            dependencies[name].append(docker_name)
    print(dependencies)

def get_all_dependencies(container):
    '''Returns all containers that are required by a certain container
    '''
    my_dependencies = []
    check_containers = [container]
    while check_containers is not []:
        check_dependencies = dependencies[check]
        check_containers.extend(check_dependencies)
        my_dependencies.extend(check_containers)
        del check_containers[container]
    return my_dependencies

get_server_dependencies()
