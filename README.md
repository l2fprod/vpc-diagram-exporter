# Generates a diagram of IBM Cloud VPC resources

[![Build Status](https://travis-ci.org/l2fprod/vpc-diagram-exporter.svg?branch=master)](https://travis-ci.org/l2fprod/vpc-diagram-exporter)

Use this tool to export a visual representation of the existing VPC resources in your IBM Cloud account.

`ibmcloud is` :arrow_right: JSON :arrow_right: [GraphViz](https://www.graphviz.org/) :arrow_right: PNG

![VPC diagram](example.png)

## Try it now with the Docker image

1. The Docker image has all required dependencies. Just run:
   ```
   docker run --rm --volume $HOME:/home -it l2fprod/vpc-diagram-exporter
   ```
1. Once the container is running, log in your IBM Cloud account inside the container:
   ```
   ibmcloud login
   ```
1. Change to a directory under the `home` volume
   ```
   cd /home/...path-to-my-project-where-files-will-be-created/
   ```
1. Run the export script, it will create an `output` folder in the current directory:
   ```
   vpc-diagram-exporter
   ```
1. Find your exported diagrams (one PNG per VPC) in the `output` folder.

## Or go manual

### Prerequisites

To use the tool and deploy the VPC examples, you will need:

* Python 2.7.1
* pip
* [graphviz](https://www.graphviz.org/) (`brew install graphviz`) on a mac
* *vpc-infrastructure* plugin for *ibmcloud* (`ibmcloud plugin install vpc-infrastructure`)

If you want to save yourself some time in the future, use [my IBM Cloud CLI docker image](https://github.com/l2fprod/bxshell) ;)

### Before you begin

The tool is written in Python with a small set of helpers to wrap the `ibmcloud` CLI so you can benefit from Python language features to interact with the VPC API.

1. Install Python requirements:

   ```sh
   pip install -r requirements.txt
   ```

1. Make sure your VPC environment is correctly configured:

   ```sh
   ibmcloud is vpcs
   ```

### Export all VPC resources into one big JSON file

`dump.py` exports all VPC resources into a big JSON files. It calls the *ibmcloud* command and requires the *is* plugin. If *ibmcloud is vpcs* works in your environment, the script should work too.

   ```sh
   ./dump.py
   ```

The script runs a few commands and produces `output/all.json`

### Convert the JSON into GraphViz

`json2gv.py` produces a [Graphviz](https://www.graphviz.org/) diagram of the elements in `output/all.json`. It uses a Jinja2 template to convert the JSON exported earlier into one Graphviz file per VPC (*vpcname.gv*) under the `output` folder.

To get the Graphviz input:

   ```sh
   ./json2gv.py
   ```

### Generate PNG images

To generate a PNG for all VPCs (all graphvizs in the folder):

   ```sh
   find output -name '*.gv' -exec dot {} -Tpng -o{}.png \;
   ```

Or to generate a PNG for a specific VPC:

   ```sh
   dot vpcname.gv -Tpng -ovpcname.png
   ```

### One liner

**PNG**

   ```sh
   ./dump.py && rm -f output/*.gv output/*.gv.png && ./json2gv.py && find output -name '*.gv' -exec dot {} -Tpng -o{}.png \;
   ```

**SVG**

   ```sh
   ./dump.py && rm -f output/*.gv output/*.gv.svg && ./json2gv.py && find output -name '*.gv' -exec dot {} -Tsvg -o{}.svg \;
   ```

## Documentation 

- [IBM Cloud Virtual Private Cloud](https://cloud.ibm.com/docs/vpc-on-classic?topic=vpc-on-classic-getting-started)

## License

This project is licensed under the Apache License Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).
