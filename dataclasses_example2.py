from dataclasses import dataclass, field, fields

"""In the Position example, you saw how to add simple default values by writing lat: float = 0.0. 
However, if you also want to customize the field, for instance to hide it in the repr, 
you need to use the default parameter: lat: float = field(default=0.0, repr=False). 
You may not specify both default and default_factory.

The metadata parameter is not used by the data classes themselves but is available
 for you (or third party packages) to attach information to fields. In the Position example, 
 you could for instance specify that latitude and longitude should be given in degrees:"""


@dataclass
class Position:
    name: str
    lon: float = field(default=0.0, metadata={'unit': 'degrees'})
    lat: float = field(default=0.0, metadata={'unit': 'degrees'})


print(fields(Position))
