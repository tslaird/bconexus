#!/usr/bin/env cwl-runner

class: CommandLineTool

id: "immcantation-4.3.0"

label: "Immcantation suite version 4.3.0"

cwlVersion: v1.0

doc: |
    A Docker container with Immcantation tools for the analysis of immune repertoires. See the [Immcantation.org](http://www.immcantation.org) website for more information.

requirements:
  - class: DockerRequirement
    dockerPull: "immcantation/suite:4.3.0"

inputs: 
  outname:
    type: string
    doc: "Output filename."
    default: immcantation-4.3.0_versions

outputs:
  imm_versions:
    type: File
    outputBinding:
        glob: "*txt"

baseCommand: [ versions, report ]
stdout: $(inputs.outname).txt

