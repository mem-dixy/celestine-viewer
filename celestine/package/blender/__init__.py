""""""


from celestine.package import Abstract


class Package(Abstract):
    """"""

    def __init__(self, hold, /, name, **star: R):
        super().__init__(hold, name, pypi="bpy")
