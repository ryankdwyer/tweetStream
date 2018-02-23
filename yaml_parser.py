import yaml

def parse(path):
    with open(path, 'rb') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as err:
            print err
            
