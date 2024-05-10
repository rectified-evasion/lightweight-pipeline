
import argparse
import sys
import model.pipeline_element as pe
import os
import importlib

from model.config import Config

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version", action="version", version="0.1"
    )

    parser.add_argument(
        "--run", action="store_true", help="Run the entire pipeline"
    )

    parser.add_argument(
        "-c", "--config", help="Path to the configuration file"
    )

    options = parser.parse_args()

    config = Config()

    if options.config:
        config_file = os.path.abspath(options.config)
        if os.path.isfile(config_file):
            config_dir = os.path.dirname(config_file)
            sys.path.insert(0, config_dir)  # add the config directory to the module search path

            module_name = os.path.splitext(os.path.basename(config_file))[0]
            config_module = importlib.import_module(module_name)
        
            # Update the current variables in the config class with the ones from the specified configuration file
            vars(config).update({k: v for k, v in vars(config_module).items() if not k.startswith("_")} )
        
            print(f"Using configuration file: {options.config}, assuming it's a python file")
        else:
            print(f"Error: Configuration file {options.config} does not exist")
    else:
        print("Using default configuration file: config.py")

    print(config.data_dir)

    if options.run:
        run_entire_pipeline(config) 

def run_entire_pipeline(config):
    # Get the path to the tasks directory
    tasks_dir = os.path.join(os.path.dirname(__file__), 'tasks')

    # Get a list of all Python files in the tasks directory
    task_files = [f for f in os.listdir(tasks_dir) if f.endswith('.py')]

    # Sort the task files alphabetically
    task_files.sort()
    pos = 1

    # Loop through the task files and import the modules
    for task_file in task_files:
        # Remove the file extension to get the module name
        module_name = os.path.splitext(task_file)[0]

        # print the number/name of task
        print(f"Task {pos}: {module_name}".center(80, '-'))
        pos = pos+1
        
        # Import the module
        module = importlib.import_module(f'tasks.{module_name}')
        
        # Get the subclasses of PipelineElement defined in the module
        pipeline_elements = [
            cls for cls in module.__dict__.values()
            if isinstance(cls, type) and issubclass(cls, pe.PipelineElement)
        ]

        data = None
        
        # Loop through the pipeline elements and invoke them
        for pipeline_element_cls in pipeline_elements:
            elt = pipeline_element_cls()
            print(elt.description)
            data = elt.process(data, config)

    print(f"Pipeline output {data}")

main()
