# -*- coding: utf-8 -*-

"""Console script for mir."""

import os
import shutil

import click
import requests

from utilities import run_call

templates_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'templates'
)

ansible_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'ansible'
)


@click.group()
def main(args=None):
    pass


@main.command()
@click.argument('name')
def init(name):
    from lib.templating import template_factory

    vagrantfile = os.path.join(templates_path, 'Vagrantfile')
    dockerfile_template = os.path.join(templates_path, 'Dockerfile')
    requirements_template = os.path.join(templates_path, 'requirements.txt')
    init_template = os.path.join(templates_path, '__init__.template')
    settings_template= os.path.join(templates_path, 'settings.py')
    gitignore_file = os.path.join(templates_path, '.gitignore')
    editorconfig_file = os.path.join(templates_path, '.editorconfig')
    group_vars_template = os.path.join(templates_path, 'group_vars.template')
    hosts_template = os.path.join(templates_path, 'hosts.template')
    project_dir = os.path.join(os.getcwd(), name)

    if not os.path.exists(project_dir):
        click.echo(click.style('\n[-] Initializing "%s" project' % name), err=True)
        os.makedirs(project_dir)

        data = {
            'name': name,
            'cwd': os.getcwd()
        }
        rendered = template_factory(data, settings_template)
        dockerfile = template_factory(data, dockerfile_template)
        with open(os.path.join(project_dir, 'settings.py'), 'w') as f:
            f.write(rendered)

        # with open(os.path.join(project_dir, 'Dockerfile'), 'w') as f:
        #     f.write(dockerfile)

        shutil.copyfile(vagrantfile, os.path.join(project_dir, 'Vagrantfile'))
        shutil.copyfile(init_template, os.path.join(project_dir, '__init__.py'))
        shutil.copyfile(requirements_template, os.path.join(project_dir, 'requirements.txt'))
        shutil.copyfile(gitignore_file, os.path.join(project_dir, '.gitignore'))
        shutil.copyfile(editorconfig_file, os.path.join(project_dir, '.editorconfig'))

        open(os.path.join(project_dir, 'README.md'), 'w').close()
        open(os.path.join(project_dir, 'AUTHORS.md'), 'w').close()
        open(os.path.join(project_dir, 'CONTRIBUTING.md'), 'w').close()

        for item in ['routes', 'hooks', 'models']:
            path = os.path.join(project_dir, item)
            os.makedirs(path)
            open(os.path.join(path, '__init__.py'), 'w').close()

        for item in ['static', 'templates', 'client']:
            path = os.path.join(project_dir, item)
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

        with open(os.path.join(project_dir, 'templates/index.html'), 'w') as f:
            f.write('Hello World!')

        click.echo(click.style('[-] New Mir project created at "%s"' % project_dir), err=False)
        click.echo(click.style('[+] Finished!', bold=True, fg='white'), err=False)
    else:
        click.echo(click.style('[!] Directory exists!', bold=True, fg='red'), err=True)


@main.command()
def start():
    from mir import start_app
    start_app()

@main.command()
def dev():
    from mir import start_app
    start_app(reload=True)


@main.command()
@click.option('--example', '-e', is_flag=True, default=False)
@click.option('--url', '-u')
def model(example, url):
    out_dir = os.path.join(os.getcwd(), 'models')
    if not example:
        if url:
            name = click.prompt('What is the name of your model?')

            r = requests.get(url)
            with open(os.path.join(out_dir, '%s.py' % name), 'w') as f:
                f.write(r.text)
        else:
            from lib.templating import template_factory
            name = click.prompt('What is the name of your model?')
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
@click.option('--url', '-u')
def route(url):
    out_dir = os.path.join(os.getcwd(), 'routes')

    if url:
        name = click.prompt('What is the name of your route?')

        r = requests.get(url)
        with open(os.path.join(out_dir, '%s.py' % name), 'w') as f:
            f.write(r.text)
    else:
        from lib.templating import template_factory

        name = click.prompt('What is the name of your route?')

        data = {
            'name': name,
        }
        template = os.path.join(templates_path, 'route.template')
        rendered = template_factory(data, template)

        with open(os.path.join(out_dir, '%s.py' % name), 'w') as f:
            f.write(rendered)

    click.echo(click.style('[+] Finished!', bold=True, fg='white'), err=False)


@main.command()
@click.option('--url', '-u')
def hook(url):
    out_dir = os.path.join(os.getcwd(), 'hooks')

    if url:
        name = click.prompt('What is the name of your hook?')

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


        name = click.prompt('What is the name of your hook?')
        timing = validate_timing(click.prompt('Create a pre- or post-request hook? [pre/post]'))
        method = validate_method(click.prompt('Create a hook for which method? [GET/POST/PUT/PATCH/DELETE]'))
        resource = click.prompt('Create a hook for a specific resource?', default=None)

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
    if environment == 'local':
        click.echo(click.style('\n[-] Deploying to the local environment\n', bold=True, fg='white'), err=False)
        inventory = os.path.join(ansible_path, 'inventories/local/hosts')
        site = os.path.join(ansible_path, 'site.yml')
        cmd = 'ansible-playbook -i %s %s --extra-vars project_src=%s' % (inventory, site, os.getcwd())
        run_call(cmd, verbose=True)

        click.echo(click.style('\n[+] Finished!', bold=True, fg='white'), err=False)
    else:
        click.echo(click.style('[!] This is not implemented yet', bold=True, fg='red'), err=True)


if __name__ == "__main__":
    import sys
    sys.exit(main())
