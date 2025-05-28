# Calculation of Maximum Allowable Current for Reconfigurable Battery Systems

[中文版本](readme.md)

This project focuses on proposing a calculation method for the Maximum Allowable Current (MAC) for any Reconfigurable Battery System (RBS). This method combines a directed graph model and a greedy algorithm, aiming to automate the calculation process to guide the design and optimization of RBS and to assess the risk of current overload in practical operation.

## Project Overview

Reconfigurable Battery Systems show great potential in the energy storage field due to their flexible topological structures. However, determining their maximum allowable current under different configurations is crucial for ensuring system safety and efficient operation. The method proposed in this project aims to solve the problem of manual MAC calculation, which is time-consuming and error-prone.

Core contributions include:
*   A directed graph-based modeling method for RBS circuit topology.
*   A MAC solving algorithm combining a greedy strategy.

Related research results have been compiled into academic papers (see the `paper/` directory) and patent applications (see the `patent/` directory).

## Directory Structure

```
.
├── code/                     # MATLAB code implementing the MAC calculation algorithm
│   └── main.m                # Main MATLAB calculation script
├── paper/                    # LaTeX manuscripts and drafts for academic papers
│   ├── main.tex              # Main paper file
│   └── SST/                  # Files related to submission to Space: Science & Technology
├── patent/                   # Markdown documents related to patent applications
│   └── main.md               # Patent specification and claims
├── topology-design-from-Xu/  # Research on topology design by Xu (Python implementation)
│   ├── README.md             # README for this subproject
│   └── LICENSE               # License for this subproject (MIT)
├── attachments/              # Image attachments used in papers and patents
└── ...                       # Other configuration files and auxiliary files
```

## Main Components

*   **Directed Graph Modeling**: Abstracting the batteries, switches, and connection relationships of an RBS into a directed graph model, where edge attributes include voltage and resistance information (see the "Invention Content" section in [patent/main.md](patent/main.md)).
*   **MAC Calculation Algorithm**:
    *   Described in detail in the "Invention Content" and "Specific Embodiments" sections of [patent/main.md](patent/main.md).
    *   The algorithm implementation is located in [code/main.m](code/main.m).
    *   The algorithm is also elaborated in the paper [paper/main.tex](paper/main.tex).

## Related Work

This project is related to the work in the `topology-design-from-Xu/` directory, which focuses on the topology design and evaluation of RBS. For more details, please refer to [topology-design-from-Xu/README.md](topology-design-from-Xu/README.md).

## Usage

The relevant calculations and algorithm implementations are mainly in the MATLAB scripts under the `code/` directory. Running the [code/main.m](code/main.m) file can execute the MAC calculation.

## License

The code in the `topology-design-from-Xu/` directory uses the MIT License, for details see [topology-design-from-Xu/LICENSE](topology-design-from-Xu/LICENSE). The license for other parts of this project is not specified.