import csv
import yaml
import os

env = "development/"

os.makedirs(env, exist_ok=True)

read=open('input_deployment.csv', mode='r', encoding='utf-8-sig')

with read as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    next(csv_reader)

    for row in csv_reader:
        name, image, version = row
        name = f'{name}'
        image = f'{image}'
        version = f'{version}'

        deployment = {
            'apiVersion': 'apps/v1',
            'kind': 'Deployment',
            'metadata': {
                'name': name,
            },
            'spec': {
                'replicas': 1,
                'selector': {
                    'matchLabels': {'app': name},
                },
                'template': {
                    'metadata': {'labels': {'app': name}},
                    'spec': {
                        'containers': [{
                            'name': name,
                            'image': f'{image}:{version}',
                        }],
                    },
                },
            },
        }

        yaml_filename = f'{env}{name}-manifest.yaml'
        with open(yaml_filename, 'w', encoding='utf-8') as yaml_file:
            yaml.dump(deployment, yaml_file)

        print(f'Created {yaml_filename}')

print('Conversion completed.')
