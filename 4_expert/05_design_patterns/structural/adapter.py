"""
Adapter Design Pattern

The Adapter pattern converts the interface of a class into another interface
clients expect. This lets classes work together that couldn't otherwise because
of incompatible interfaces.
"""


# Target interface that the client expects to work with
class Target:
    def request(self) -> str:
        return "Target: The default target's behavior."


# The Adaptee contains some useful behavior, but its interface is incompatible
# with the existing client code. The Adaptee needs some adaptation before the
# client code can use it.
class Adaptee:
    def specific_request(self) -> str:
        return "Special behavior of the Adaptee"


# The Adapter makes the Adaptee's interface compatible with the Target's
# interface via composition.
class Adapter(Target):
    def __init__(self, adaptee: Adaptee):
        self.adaptee = adaptee
        
    def request(self) -> str:
        return f"Adapter: (TRANSLATED) {self.adaptee.specific_request()}"


# Another example using a real-world analogy: converting between data formats
class JSONData:
    def __init__(self, data: dict):
        self.data = data
        
    def get_json(self) -> dict:
        return self.data


class XMLConverter:
    def convert_to_xml(self, json_data: dict) -> str:
        # This is a simplified conversion
        xml = "<root>\n"
        for key, value in json_data.items():
            xml += f"  <{key}>{value}</{key}>\n"
        xml += "</root>"
        return xml


class JSONToXMLAdapter:
    def __init__(self, json_data: JSONData):
        self.json_data = json_data
        self.xml_converter = XMLConverter()
        
    def get_xml(self) -> str:
        json_data = self.json_data.get_json()
        return self.xml_converter.convert_to_xml(json_data)


# Example usage
if __name__ == "__main__":
    print("Client: I can work with Target objects:")
    target = Target()
    print(target.request())
    
    print("\nClient: But I can work with Adaptee objects only through an Adapter:")
    adaptee = Adaptee()
    adapter = Adapter(adaptee)
    print(adapter.request())
    
    print("\nJSON to XML Adapter example:")
    json_data = JSONData({"name": "John", "age": 30, "city": "New York"})
    adapter = JSONToXMLAdapter(json_data)
    print(adapter.get_xml())