# %% THIS IS ONLY TEMP

import math
import os
import pandas as pd
from swarmcli.builders import ToolBuilder
from swarmcli.clients import ToolClient

tool_builder = ToolBuilder(ToolClient("http://localhost:5000"))
tool = tool_builder.from_id("674b5efa-8c42-46ea-8299-7417279359f6").product
# %%
