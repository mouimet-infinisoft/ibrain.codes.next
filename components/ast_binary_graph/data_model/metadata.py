class Metadata:
    def __init__(self, name, filename, path, lines, relations_count, resource_type):
        self.name = name
        self.filename = filename
        self.path = path
        self.lines = lines
        self.relations_count = relations_count
        self.resource_type = resource_type

    def __str__(self):
        return (
            f"Metadata(name={self.name}, filename={self.filename}, path={self.path}, "
            f"lines={self.lines}, relations_count={self.relations_count}, resource_type={self.resource_type})"
        )

    def __repr__(self):
        return (
            f"Metadata(name={self.name!r}, filename={self.filename!r}, path={self.path!r}, "
            f"lines={self.lines!r}, relations_count={self.relations_count!r}, resource_type={self.resource_type!r})"
        )