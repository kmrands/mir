# -*- coding: utf-8 -*-

"""Console script for mir."""

import os
import re
import shutil

import click
import requests

from utilities import run_call, generate_password, generate_secret_key

templates_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'templates'
)

ansible_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'ansible'
)

def validate_name(ctx, param, name):
    if re.match('^[a-zA-Z0-9_]+$', name):
        return name
    else:
        raise click.BadParameter('Must contain only alphanumeric characters and underscores')


@click.group()
def main(args=None):
    pass


@main.command()
@click.argument('name')
def init(name):
    from lib.templating import template_factory

    name = validate_name(None, None, name)

    vagrantfile = os.path.join(templates_path, 'Vagrantfile')
    dockerfile_template = os.path.join(templates_path, 'Dockerfile')
    docker_compose_template= os.path.join(templates_path, 'docker-compose.yml')
    requirements_template = os.path.join(templates_path, 'requirements.txt')
    init_template = os.path.join(templates_path, '__init__.template')
    settings_template= os.path.join(templates_path, 'settings.py')
    gitignore_file = os.path.join(templates_path, '.gitignore')
    editorconfig_file = os.path.join(templates_path, '.editorconfig')
    group_vars_template = os.path.join(templates_path, 'group_vars.template')
    hosts_template = os.path.join(templates_path, 'hosts.template')

    project_dir = os.path.join(os.getcwd(), name)
    app_dir = os.path.join(project_dir, 'application')

    if not os.path.exists(project_dir):
        click.echo(click.style('\n[-] Initializing "%s" project' % name), err=True)
        os.makedirs(project_dir)
        os.makedirs(app_dir)

        data = {
            'name': name,
            'cwd': os.getcwd()
        }
        # Create Settings and Dockerfile
        rendered = template_factory(data, settings_template)
        dockerfile = template_factory(data, dockerfile_template)

        with open(os.path.join(app_dir, 'settings.py'), 'w') as f:
            f.write(rendered)

        with open(os.path.join(app_dir, 'Dockerfile'), 'w') as f:
            f.write(dockerfile)

        shutil.copyfile(vagrantfile, os.path.join(project_dir, 'Vagrantfile'))
        shutil.copyfile(docker_compose_template, os.path.join(project_dir, 'docker-compose.yml'))
        shutil.copyfile(init_template, os.path.join(app_dir, '__init__.py'))
        shutil.copyfile(requirements_template, os.path.join(app_dir, 'requirements.txt'))
        shutil.copyfile(gitignore_file, os.path.join(project_dir, '.gitignore'))
        shutil.copyfile(editorconfig_file, os.path.join(project_dir, '.editorconfig'))

        open(os.path.join(project_dir, '.mir'), 'w').close()
        open(os.path.join(project_dir, 'README.md'), 'w').close()
        open(os.path.join(project_dir, 'AUTHORS.md'), 'w').close()
        open(os.path.join(project_dir, 'CONTRIBUTING.md'), 'w').close()

        for item in ['routes', 'hooks', 'models']:
            path = os.path.join(app_dir, item)
            os.makedirs(path)
            open(os.path.join(path, '__init__.py'), 'w').close()

        for item in ['static', 'templates']:
            path = os.path.join(app_dir, item)
            os.makedirs(path)
            open(os.path.join(path, '.gitkeep'), 'w').close()

        inventories = os.path.join(project_dir, 'inventories')
        os.makedirs(inventories)
        for item in ['staging', 'production']:
            path = os.path.join(inventories, item)
            os.makedirs(path)
            group_vars = os.path.join(path, 'group_vars')
            os.makedirs(group_vars)
            shutil.copyfile(group_vars_template, os.path.join(group_vars, 'all'))
            shutil.copyfile(hosts_template, os.path.join(path, 'hosts'))

        with open(os.path.join(app_dir, 'templates/index.html'), 'w') as f:
            f.write('Hello World!')

        click.echo(click.style('[-] New Mir project created at "%s"' % project_dir), err=False)
        click.echo(click.style('[+] Finished!', bold=True, fg='white'), err=False)
    else:
        click.echo(click.style('[!] Directory exists!', bold=True, fg='red'), err=True)


@main.command()
@click.option('--port', '-p', default='8080')
def start(port):
    from mir import start_app
    start_app(port=port)

@main.command()
@click.option('--port', '-p', default='8080')
def dev(port):
    from mir import start_app
    start_app(reload=True, port=port)


@main.command()
@click.option(
    '--name',
    '-n',
    prompt="What is the name of your model?",
    callback=validate_name
)
@click.option('--example', '-e', is_flag=True, default=False)
@click.option('--url', '-u')
def model(name, example, url):
    from config import APP_DIR

    out_dir = os.path.join(APP_DIR, 'models')
    if not example:
        if url:
            r = requests.get(url)
            with open(os.path.join(out_dir, '%s.py' % name), 'w') as f:
                f.write(r.text)
        else:
            from lib.templating import template_factory
            data = {
                'name': name,
            }
            template = os.path.join(templates_path, 'model.template')
            rendered = template_factory(data, template)

            with open(os.path.join(out_dir, '%s.py' % name), 'w') as f:
                f.write(rendered)
    else:
        example_file = os.path.join(templates_path, 'example.py')
        shutil.copyfile(example_file, os.path.join(out_dir, 'example.py'))

    click.echo(click.style('[+] Finished!', bold=True, fg='white'), err=False)


@main.command()
@click.option(
    '--name',
    '-n',
    prompt="What is the name of your route?",
    callback=validate_name
)
@click.option('--url', '-u')
def route(name, url):
    from config import APP_DIR

    out_dir = os.path.join(APP_DIR, 'routes')

    if url:
        r = requests.get(url)
        with open(os.path.join(out_dir, '%s.py' % name), 'w') as f:
            f.write(r.text)
    else:
        from lib.templating import template_factory
        data = {
            'name': name,
        }
        template = os.path.join(templates_path, 'route.template')
        rendered = template_factory(data, template)

        with open(os.path.join(out_dir, '%s.py' % name), 'w') as f:
            f.write(rendered)

    click.echo(click.style('[+] Finished!', bold=True, fg='white'), err=False)


@main.command()
@click.option(
    '--name',
    '-n',
    prompt="What is the name of your hook?",
    callback=validate_name
)
@click.option(
    '--timing',
    '-t',
    prompt="Create a pre- or post-request hook? [pre/post]"
)
@click.option(
    '--method',
    '-m',
    prompt="Create a hook for which method? [GET/POST/PUT/PATCH/DELETE]"
)
@click.option(
    '--resource',
    '-r',
    prompt="Create a hook for a specific resource?",
    default=None
)
@click.option('--url', '-u')
def hook(name, timing, method, resource, url):
    from config import APP_DIR

    out_dir = os.path.join(APP_DIR, 'hooks')

    if url:

        r = requests.get(url)
        with open(os.path.join(out_dir, '%s.py' % name), 'w') as f:
            f.write(r.text)
    else:
        from lib.templating import template_factory

        def validate_timing(value):
            if value == 'pre' or value == 'post':
                return value
            else:
                raise click.BadParameter('Must be "pre" or "post"')

        def validate_method(value):
            options = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
            if value in options:
                return value
            else:
                raise click.BadParameter('Must be one of "%s"' % ', '.join(options))

        data = {
            'name': name,
            'timing': timing,
            'method': method,
            'resource': resource
        }
        template = os.path.join(templates_path, 'hook.template')
        rendered = template_factory(data, template)

        with open(os.path.join(out_dir, '%s.py' % name), 'w') as f:
            f.write(rendered)

    click.echo(click.style('[+] Finished!', bold=True, fg='white'), err=False)


@main.command()
@click.argument('environment')
def deploy(environment):
    from config import ROOT_DIR, APP_DIR

    if environment == 'local':
        click.echo(click.style('\n[-] Deploying to the local environment\n', bold=True, fg='white'), err=False)
        inventory = os.path.join(ansible_path, 'inventories/local/hosts')
        site = os.path.join(ansible_path, 'site.yml')
        cmd = 'ansible-playbook -i %s %s --extra-vars project_src=%s' % (inventory, site, APP_DIR)
        run_call(cmd, verbose=True)

        click.echo(click.style('\n[+] Finished!', bold=True, fg='white'), err=False)
    else:
        click.echo(click.style('\n[-] Deploying to the %s environment\n' % environment, bold=True, fg='white'), err=False)
        inventory = os.path.join(ROOT_DIR, 'inventories/%s/hosts' % environment)
        if inventory:
            site = os.path.join(ansible_path, 'site.yml')
            cmd = 'ansible-playbook -i %s %s --extra-vars project_src=%s' % (inventory, site, APP_DIR)
            run_call(cmd, verbose=True)
            click.echo(click.style('\n[+] Finished!', bold=True, fg='white'), err=False)
        else:
            click.echo(click.style('\n[!] No inventory exists for that environment', bold=True, fg='red'), err=True)

@main.command()
def password():
    click.echo(generate_password())

@main.command()
def secret():
    click.echo(generate_secret_key())

if __name__ == "__main__":
    import sys
    sys.exit(main())
