from jinja2 import Environment, FileSystemLoader

def environment(**options):
    env = Environment(
        loader=FileSystemLoader('templates'),  # Path where Jinja2 templates are stored
        **options
    )
    return env