import importlib


if importlib.util.find_spec('PIL') is not None:
    from PIL import __version__, Image
    PIL_version = __version__
    # self.image_open = Image.open

    def read_PIL(file_name: str) -> object:
        with open(file_name, 'rb') as file:
            img = Image.open(file)
            return img.convert('RGB')
else:
    read_PIL = None
    PIL_version = None

image_read_dict = {'PIL': {'read_func': read_PIL, 'version': PIL_version},
                   }
