# -*- coding: utf-8 -*-

"""Console script for mir."""

import os
import shutil

import click

templates_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'templates'
)


@click.group()
def main(args=None):
    pass


@main.command()
@click.argument('name')
def init(name):
    from lib.templating import template_factory

    requirements_template = os.path.join(templates_path, 'requirements.txt')
    init_template = os.path.join(templates_path, '__init__.template')
    settings_template= os.path.join(templates_path, 'settings.py')
    gitignore_file = os.path.join(templates_path, '.gitignore')
    editorconfig_file = os.path.join(templates_path, '.editorconfig')
    project_dir = os.path.join(os.getcwd(), name)

    if not os.path.exists(project_dir):
        click.echo(click.style('\n[-] Initializing "%s" project' % name), err=True)
        os.makedirs(project_dir)

        data = {
            'name': name,
        }
        rendered = template_factory(data, settings_template)
        with open(os.path.join(project_dir, 'settings.py'), 'w') as f:
            f.write(rendered)

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

        for item in ['static', 'templates', 'admin', 'client']:
            path = os.path.join(project_dir, item)
            os.makedirs(path)
            open(os.path.join(path, '.gitkeep'), 'w').close()

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
    from mir import start_dev_app
    start_dev_app()


@main.command()
@click.option('--example', '-e', is_flag=True, default=False)
def model(example):
    out_dir = os.path.join(os.getcwd(), 'models')
    if not example:
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
def route():
    from lib.templating import template_factory

    out_dir = os.path.join(os.getcwd(), 'routes')

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
def hook():
    from lib.templating import template_factory

    out_dir = os.path.join(os.getcwd(), 'hooks')

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
    resource = click.prompt('Create a hook for which resource?', default=False)

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




if __name__ == "__main__":
    import sys
    sys.exit(main())
