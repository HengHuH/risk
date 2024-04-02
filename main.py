# -*- coding: utf-8 -*-

from expander import all_nodes
from expander import Expander, DAG

import curve


def main():

    dag = DAG()
    for name, nd in all_nodes().items():
        dag.add_vertex(name)
        dag.add_edge(name, *nd["deps"])

    expander = Expander(dag)
    expander.execute()

    with open("output.txt", "w") as f:
        for name, nd in all_nodes().items():
            f.write(f"{name}: {nd['curve']}\n")


if __name__ == "__main__":
    main()
