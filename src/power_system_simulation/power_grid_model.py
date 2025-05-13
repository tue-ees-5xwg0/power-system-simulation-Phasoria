"""
Assignment 2 - power grid model
"""

from typing import List, Tuple
import pandas as pd
from power_grid_model.utils import self_test
from power_grid_model import(
    ComponentType,
    DatasetType,
    LoadGenType,
    PowerGridModel,
    initialize_array
)

class Powergridmodel:
    """
    General class - definition of the power grid module
    """

    def __init__(
            self,
            node: ComponentType.node,
            line: ComponentType.line,
            sym_load: ComponentType.sym_load,
            source: ComponentType.source,
    ) -> None:

        node = initialize_array(DatasetType.input, ComponentType.node, size_node)
        line = initialize_array(DatasetType.input, ComponentType.line, size_line)
        sym_load = initialize_array(DatasetType.input, ComponentType.sym_load, size_sym_load)
        source = initialize_array(DatasetType.input, ComponentType.source, size_source)

        input_data = {
            ComponentType.node: node,
            ComponentType.line: line,
            ComponentType.sym_load: sym_load,
            ComponentType.source: source
        }

        model = PowerGridModel(input_data, system_frequency = frequency)
