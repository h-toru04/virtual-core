# -*- coding: utf-8 -*-
'''
.. module:: wizard.__main__
   :synopsis: A Web based wizard to setup the core, entry point
   :noindex:
   :copyright: Copyright 2016 by Tiago Antao
   :license: GNU Affero, see LICENSE for details

.. moduleauthor:: Tiago Antao <tra@popgen.net>

'''
import os

from flask import Flask, render_template, redirect, request, url_for

import wizard

app = Flask(__name__)


def _delist(form, exceptions=[]):
    delist = {}
    for k, v in form.items():
        if type(v) == list and k not in exceptions:
            delist[k] = v[0]
        else:
            delist[k] = v
    return delist


def _has_all_parameters(form, parameters):
    for parameter in parameters:
        if parameter in form:
              if form[parameter] == '':
                  return False
        else:
            return False
    return True


@app.route('/', methods=['GET'])
@app.route('/<int:run>', methods=['GET', 'POST'])
def welcome(run=0):
    if run == 0:
        form = wizard.config.get('General', {})
    else:
        form = _delist(request.form)
        if _has_all_parameters(form, ['country', 'state', 'locality', 'orgname', 'orgunit', 'commonname', 'email']):
            wizard.change_config('General', **form)
            return redirect(url_for('determine_ssh_status', run=0))
    all_params = {'run': run, **form}
    return render_template('welcome.html', **all_params)


@app.route('/sshkey/<int:run>')
def determine_ssh_status(run=0):
    if not os.path.exists('etc/ssh'):
        os.mkdir('etc/ssh')
    if not os.path.exists('etc/ssh/authorized_keys'):
        return render_template('need_ssh.html', run=run)
    else:
        return redirect(url_for('explain_certificate_authority', run=0))


@app.route('/ca/<int:run>')
def explain_certificate_authority(run=0):
    if not os.path.exists('etc/ca'):
        os.mkdir('etc/ca')
    if not os.path.exists('etc/ca/UNDERSTAND') or \
            not os.path.exists('etc/ca/demoCA'):
        return render_template('need_ca.html', run=run)
    else:
        return redirect(url_for('get_named_directories_root'))


@app.route('/create_ca')
def create_certificate_authority(run=0):
    if os.path.exists('etc/ca/demoCA'):
        return render_template('exists_ca.html', next_route='/named_directories')


@app.route('/named_directories')
def get_named_directories_root():
    if root is None or not os.path.isdir(root):
        return render_template('named_directories.html', root=root)
    else:
        return redirect(url_for('choose_containers'))


@app.route('/choose')
def choose_containers():
    return render_template('choose_containers.html')

if __name__ == "__main__":
    app.debug = True
    app.run()
