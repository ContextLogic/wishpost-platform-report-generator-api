from wish_flask.shell import ipshell, VariableCollector
from report_generator_service.server import app
try:
    from flask_mongoengine import Document
except:
    Document = object


ipshell(
    app,
    var_collectors=[
        VariableCollector(
            'report_generator_service.models',
            class_types=[Document],
            collect_subclasss=True
        )
    ]
)

# Try running this script by:
#    >> FLASK_ENV=dev python report_generator_service/shell.py
